"""The output-store seam — where a production's rendered bytes durably live (storyline 0005).

A renderer (:mod:`sequitur.render`) writes an artifact's bytes to a *scratch* path;
that path is ephemeral and workstation-local. The **output store** is the data-plane
seam that takes those bytes and files them under a stable ``production / layer / name``
key in a **durable** store, returning a ``ref`` the board can link to and that
survives across iterations of a production (the 0036 dailies model reviews each
phase's deliverable at a gate and compares it across revisions).

It is the third seam of the studio — one per plane:

* :class:`~sequitur.render.Renderer` — the *execution* plane (a decision -> new bytes);
* :class:`~sequitur.production.ProductionProvider` — the *control* plane (board tree
  <-> ``Brief`` / ``Sequence``);
* :class:`OutputStore` — the *data* plane (produced bytes -> a durable reference).

One backend exists today: :class:`LocalFolderOutputStore`, which files artifacts
under a root directory. Point that root (``OUTPUT_STORE_ROOT``) at a OneDrive-synced
folder and "local disk" already buys **tenant durability** for free — storyline
0005's local-folder provider #1 and its Option-A OneDrive bridge, in one. A
:class:`GraphOutputStore` (SharePoint uploads via Microsoft Graph) swaps in behind the
same protocol; its ``ref`` is a URL string, which is why the seam's return type
is ``Path | str`` (mirroring :class:`~sequitur.render.RenderResult`). The Graph
backend uploads bytes directly and returns an **authoritative** share URL only after
the upload completes, closing the "publish race" of storyline 0051 (the local backend
depends on the OneDrive sync client to publish the file, so its https link is
*eventually* consistent — the URL is correct before the bytes have synced).
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class OutputStore(Protocol):
    """The data-plane seam: produced bytes in, a durable reference out.

    ``artifact`` is either raw ``bytes`` or a path to a freshly rendered file (what a
    :class:`~sequitur.render.RenderResult` carries in ``ref``). It is filed under a
    ``production / layer / name`` key and a ``ref`` is returned — a local
    :class:`~pathlib.Path` today, a share-URL ``str`` once a Graph backend lands.
    """

    def put(
        self,
        artifact: bytes | str | Path,
        *,
        production: str,
        layer: str,
        name: str | None = None,
    ) -> Path | str: ...


class LocalFolderOutputStore:
    """A directory-backed output store (storyline 0005's provider #1).

    Files each artifact at ``<root>/<production>/<layer>/<name>`` and returns that
    path. With ``root`` pointed at a OneDrive-synced folder (``OUTPUT_STORE_ROOT`` in
    ``.env``), the write lands in the tenant's SharePoint/OneDrive capacity, so this
    single backend also serves as the durability bridge — no API code and no new
    dependency, just :mod:`shutil` and :mod:`pathlib`.
    """

    def __init__(self, root: str | Path | None = None) -> None:
        if root is None:
            from .config import get_output_store_root

            root = get_output_store_root()
        self.root = Path(root)

    def put(
        self,
        artifact: bytes | str | Path,
        *,
        production: str,
        layer: str,
        name: str | None = None,
    ) -> Path:
        dest_dir = self.root / production / layer
        if isinstance(artifact, (bytes, bytearray)):
            if not name:
                raise ValueError("A name is required when storing raw bytes.")
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / name
            dest.write_bytes(artifact)
            return dest
        source = Path(artifact)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / (name or source.name)
        shutil.copyfile(source, dest)
        return dest


class GraphOutputStore:
    """A SharePoint/OneDrive output store backed by the Microsoft Graph API.

    Where :class:`LocalFolderOutputStore` writes bytes into a OneDrive-synced folder
    and leans on the *desktop sync client* to publish them — so its https link is
    only *eventually* consistent (the "publish race" of storyline 0051: the URL is
    right the moment it is minted, but briefly serves the stale blob until the client
    uploads the overwrite) — this backend uploads the bytes to the drive **directly**
    over Graph and returns an **authoritative** ``webUrl`` only after the upload has
    completed. That URL string is the ``ref`` (storyline 0038's deferred "URL later").

    Auth is the caller's Entra identity (``DefaultAzureCredential`` on the Graph
    scope) — no key, no new dependency beyond the ``azure-identity`` already used for
    Key Vault; the transport is stdlib :mod:`urllib`. ``__init__`` touches no network
    (the token and every request are lazy), so it is safe to construct offline.
    """

    _GRAPH = "https://graph.microsoft.com/v1.0"
    _SCOPE = "https://graph.microsoft.com/.default"

    def __init__(
        self,
        drive_id: str | None = None,
        root_path: str | None = None,
        *,
        credential=None,
    ) -> None:
        if drive_id is None or root_path is None:
            from .config import get_graph_store_config

            cfg = get_graph_store_config()
            drive_id = drive_id or cfg.drive_id
            root_path = cfg.root_path if root_path is None else root_path
        self.drive_id = drive_id
        self.root_path = root_path.strip("/")
        self._credential = credential

    def _token(self) -> str:
        if self._credential is None:
            from azure.identity import DefaultAzureCredential

            self._credential = DefaultAzureCredential()
        return self._credential.get_token(self._SCOPE).token

    def _upload(self, item_path: str, data: bytes) -> dict:
        """Simple upload of ``data`` to ``drive/root:/<item_path>`` (Graph creates parents)."""
        import json
        import urllib.parse
        import urllib.request

        encoded = "/".join(urllib.parse.quote(part) for part in item_path.split("/"))
        url = f"{self._GRAPH}/drives/{self.drive_id}/root:/{encoded}:/content"
        req = urllib.request.Request(
            url,
            data=data,
            method="PUT",
            headers={
                "Authorization": f"Bearer {self._token()}",
                "Content-Type": "application/octet-stream",
            },
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def put(
        self,
        artifact: bytes | str | Path,
        *,
        production: str,
        layer: str,
        name: str | None = None,
    ) -> str:
        if isinstance(artifact, (bytes, bytearray)):
            if not name:
                raise ValueError("A name is required when storing raw bytes.")
            data, filename = bytes(artifact), name
        else:
            source = Path(artifact)
            data, filename = source.read_bytes(), name or source.name
        item_path = "/".join(
            part for part in (self.root_path, production, layer, filename) if part
        )
        item = self._upload(item_path, data)
        # ``webUrl`` is authoritative the instant the upload returns — the whole point.
        return item["webUrl"]

