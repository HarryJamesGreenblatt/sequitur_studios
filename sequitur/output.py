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
``GraphOutputStore`` (SharePoint share URLs via Microsoft Graph) swaps in behind the
same protocol later; its ``ref`` is a URL string, which is why the seam's return type
is ``Path | str`` (mirroring :class:`~sequitur.render.RenderResult`).
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
