"""The production seam — the board ↔ ``Brief`` / ``Sequence`` bridge (storyline 0005/0024).

Storyline 0008 decided that a *production* is not a repo fork but external
**content**, modelled as a project-management board whose narrative tree is the
studio's work list; 0024 stood that board up on **Azure DevOps** (a custom
Act → Scene → Beat → Shot process, crew departments as Area Paths). This module is
the *code* seam over it — the analogue of the :mod:`sequitur.render` renderer seam,
but for the *decision* plane instead of the execution plane:

* :meth:`ProductionProvider.read_brief` reads the board's narrative tree into a
  :class:`~sequitur.crew.role.Brief` — the coverage (``shots``) plus the producer's
  look/mood nudges — which the crew :class:`~sequitur.crew.engine.Engine` then
  assembles into a graded edit :class:`~sequitur.edit.Sequence`;
* :meth:`ProductionProvider.write_sequence` records that assembled result back onto
  the board (each Shot's applied grade).

Two backends sit behind the one :class:`ProductionProvider` protocol
(backend-swappable, per 0024): :class:`AzureDevOpsProduction` (the live board, over
the ADO REST API via ``DefaultAzureCredential`` — no new dependency, just stdlib
:mod:`urllib`) and :class:`LocalFolderProduction` (a file-backed test double that
needs no network, the "local folder" the 0005 design always reserved).

**v1 scope.** The read is *flat* — every Shot in the project becomes one unit of
coverage, in work-item-id order; scene-scoped reads (a WIQL tree query) are a later
refinement. A shot's board ``Look`` is a *per-shot* field, but a :class:`Brief`
carries a single look nudge, so the read *aggregates* to the first shot's look
(per-shot grade matching — Color Correction Handbook Ch. 9 — is a named next step).
Read and write correlate **positionally**: both walk Shots in id order, and
:meth:`~sequitur.crew.director.Director.assemble` preserves that order, so the
i-th timeline clip maps to the i-th Shot work item.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Protocol, runtime_checkable

from .crew.colorist import Look
from .crew.role import Brief
from .shot import Shot

if TYPE_CHECKING:
    from .edit import Clip, Sequence


# -- Look <-> board picklist display -------------------------------------------
#
# The board's ``Custom.Look`` picklist stores the display label ("Golden Hour");
# the code speaks the :class:`Look` enum and a grade's lower-snake ``name``
# ("golden_hour"). These helpers translate between the three forms.

_LOOK_DISPLAY: dict[Look, str] = {
    Look.NEUTRAL: "Neutral",
    Look.WARM: "Warm",
    Look.COOL: "Cool",
    Look.GOLDEN_HOUR: "Golden Hour",
    Look.TEAL_ORANGE: "Teal-Orange",
    Look.NOIR: "Noir",
    Look.BLEACH_BYPASS: "Bleach-Bypass",
}


def _look_from_str(value: str | None) -> Look | None:
    """Parse a board label ("Golden Hour") or a grade name ("golden_hour") to a :class:`Look`."""
    if not value:
        return None
    for look, display in _LOOK_DISPLAY.items():
        if display == value:
            return look
    try:
        return Look[value.strip().upper().replace(" ", "_").replace("-", "_")]
    except KeyError:
        return None


def _look_display(value: Look | str | None) -> str | None:
    """Render a :class:`Look` (or a grade name) as its board picklist label.

    A production's *custom* registered look (a name outside the :class:`Look`
    enum) falls through to its raw name — the picklist allows custom values.
    """
    if value is None:
        return None
    if isinstance(value, Look):
        return _LOOK_DISPLAY[value]
    look = _look_from_str(value)
    return _LOOK_DISPLAY[look] if look is not None else value


def _clips(sequence: "Sequence") -> Iterable["Clip"]:
    """The sequence's clips in playback order (the write side's positional key)."""
    return [entry.clip for entry in sequence.timeline()]


def _clip_look(clip: "Clip") -> str | None:
    """The grade applied to a clip, as a board look label (or ``None`` if ungraded)."""
    grade = getattr(clip, "grade", None)
    return _look_display(getattr(grade, "name", None)) if grade is not None else None


@runtime_checkable
class ProductionProvider(Protocol):
    """The production seam: a board tree in as a :class:`Brief`, an assembly out.

    The mirror of :class:`sequitur.render.Renderer` for the decision plane. A
    caller (the CLI, or a future phase-aware ``Engine`` binding) reads a brief,
    hands it to the crew, and writes the assembled sequence back — never touching
    the concrete backend.
    """

    def read_brief(self, *, scene: str | None = None) -> Brief: ...

    def write_sequence(self, sequence: "Sequence") -> None: ...


class LocalFolderProduction:
    """A file-backed provider — the test double for the board (no network).

    Reads/writes a single JSON document shaped like a flattened board:
    ``{"scene": "...", "shots": [{"scene": "...", "mood": "...", "look": "..."}]}``.
    It honours the same :class:`ProductionProvider` contract as the live ADO
    backend, so the crew engine can be exercised end-to-end offline (storyline
    0005's "local folder" provider #1).
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _load(self) -> dict:
        if not self.path.exists():
            return {"shots": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def read_brief(self, *, scene: str | None = None) -> Brief:
        data = self._load()
        shots: list[Shot] = []
        look: Look | None = None
        for entry in data.get("shots", []):
            shots.append(Shot(scene=entry["scene"], mood=entry.get("mood")))
            if look is None:
                look = _look_from_str(entry.get("look"))
        hints = {"look": look} if look is not None else {}
        return Brief(scene=scene or data.get("scene", ""), hints=hints, shots=shots)

    def write_sequence(self, sequence: "Sequence") -> None:
        data = self._load()
        shots = data.setdefault("shots", [])
        for i, clip in enumerate(_clips(sequence)):
            label = _clip_look(clip)
            if i < len(shots):
                if label is not None:
                    shots[i]["look"] = label
            else:
                shots.append(
                    {"scene": clip.shot.scene, "mood": clip.shot.mood, "look": label}
                )
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class AzureDevOpsProduction:
    """The live board provider — reads/writes Azure DevOps work items over REST.

    Authenticates with ``DefaultAzureCredential`` (the same local ``az login``
    identity that mints the ADO token), so it needs **no new dependency** — just
    stdlib :mod:`urllib` and the ``azure-identity`` already used for Key Vault.
    Only non-secret pointers (org URL, project) are read from config; the ADO
    resource id is the public, first-party constant.
    """

    _SHOT_FIELDS = (
        "System.Id",
        "System.Title",
        "System.AreaPath",
        "Custom.Mood",
        "Custom.Look",
    )

    def __init__(self, config=None, credential=None, *, project=None) -> None:
        from .config import get_ado_config

        # ``project`` selects the Production (one ADO project = one Production);
        # None falls back to the ADO_PROJECT default in .env (see get_ado_config).
        self.config = config or get_ado_config(project=project)
        self._credential = credential

    @classmethod
    def list_productions(cls, *, org_url=None, credential=None) -> list[str]:
        """List the org's **productions** — one ADO project is one Production.

        The enumerate step for the multi-production world: it needs *no* project
        selected (that is what it is for). Reads ``ADO_ORG_URL`` from ``.env`` unless
        given, authenticates with the caller's Entra identity, and returns the
        project names sorted — the ``.env`` ``ADO_PROJECT`` is only the default pick.
        """
        import os as _os

        from .config import ADO_RESOURCE_ID

        org_url = (org_url or _os.environ.get("ADO_ORG_URL") or "").rstrip("/")
        if not org_url:
            raise RuntimeError(
                "No ADO_ORG_URL configured. Set it in .env "
                "(https://dev.azure.com/<org>) or pass org_url."
            )
        if credential is None:
            from azure.identity import DefaultAzureCredential

            credential = DefaultAzureCredential()
        token = credential.get_token(f"{ADO_RESOURCE_ID}/.default").token
        req = urllib.request.Request(
            f"{org_url}/_apis/projects?api-version=7.1",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return sorted(p["name"] for p in result.get("value", []))

    # -- transport ---------------------------------------------------------

    def _token(self) -> str:
        if self._credential is None:
            from azure.identity import DefaultAzureCredential

            self._credential = DefaultAzureCredential()
        return self._credential.get_token(f"{self.config.resource_id}/.default").token

    def _request(self, method: str, url: str, body=None, *, patch: bool = False):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {
            "Authorization": f"Bearer {self._token()}",
            "Accept": "application/json",
        }
        if data is not None:
            headers["Content-Type"] = (
                "application/json-patch+json" if patch else "application/json"
            )
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _project_url(self, path: str) -> str:
        return f"{self.config.org_url}/{self.config.project}/_apis/{path}"

    def _org_url(self, path: str) -> str:
        return f"{self.config.org_url}/_apis/{path}"

    # -- board queries -----------------------------------------------------

    def _shot_ids(self) -> list[int]:
        """Every Shot work item in the project, in id order (the positional key)."""
        query = (
            "SELECT [System.Id] FROM workitems "
            "WHERE [System.TeamProject] = @project "
            "AND [System.WorkItemType] = 'Shot' "
            "ORDER BY [System.Id] ASC"
        )
        result = self._request(
            "POST", self._project_url("wit/wiql?api-version=7.1"), {"query": query}
        )
        return [item["id"] for item in result.get("workItems", [])]

    def _first_scene_title(self) -> str:
        query = (
            "SELECT [System.Id] FROM workitems "
            "WHERE [System.TeamProject] = @project "
            "AND [System.WorkItemType] = 'Scene' "
            "ORDER BY [System.Id] ASC"
        )
        result = self._request(
            "POST", self._project_url("wit/wiql?api-version=7.1"), {"query": query}
        )
        items = result.get("workItems", [])
        if not items:
            return ""
        batch = self._request(
            "POST",
            self._org_url("wit/workitemsbatch?api-version=7.1"),
            {"ids": [items[0]["id"]], "fields": ["System.Title"]},
        )
        return batch["value"][0]["fields"].get("System.Title", "")

    def _shots_batch(self, ids: list[int]) -> list[dict]:
        if not ids:
            return []
        result = self._request(
            "POST",
            self._org_url("wit/workitemsbatch?api-version=7.1"),
            {"ids": ids, "fields": list(self._SHOT_FIELDS)},
        )
        return result.get("value", [])

    # -- the seam ----------------------------------------------------------

    def read_brief(self, *, scene: str | None = None) -> Brief:
        ids = self._shot_ids()
        shots: list[Shot] = []
        look: Look | None = None
        for item in self._shots_batch(ids):
            fields = item.get("fields", {})
            shots.append(
                Shot(scene=fields.get("System.Title", ""), mood=fields.get("Custom.Mood"))
            )
            if look is None:
                look = _look_from_str(fields.get("Custom.Look"))
        hints = {"look": look} if look is not None else {}
        label = scene if scene is not None else self._first_scene_title()
        return Brief(scene=label, hints=hints, shots=shots)

    def write_sequence(self, sequence: "Sequence") -> None:
        ids = self._shot_ids()
        for wid, clip in zip(ids, _clips(sequence)):
            label = _clip_look(clip)
            if label is None:
                continue
            self._request(
                "PATCH",
                self._project_url(f"wit/workitems/{wid}?api-version=7.1"),
                [{"op": "add", "path": "/fields/Custom.Look", "value": label}],
                patch=True,
            )
