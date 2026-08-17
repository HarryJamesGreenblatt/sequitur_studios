"""Provision / heal the org-level PROCESS TEMPLATE (storyline 0052).

Sibling of :mod:`provision_production`. That script stands up a per-**project** board
(areas / teams / iterations); this one ensures the shared **process** itself — the
work-item types with their icons, colours, descriptions, states, and backlog-level
mapping — matches the declared template below. This is the tier that had been hand-built
via ad-hoc REST across storylines 0024 / 0049 / 0052; codifying it makes the template
reproducible and lets a single run **heal drift** (a stale description, a wrong icon).

Idempotent and detect-then-act: ``ok`` when a type already matches, ``patch`` when it
heals drift, ``create`` when a type is missing.

**Scope** — the active narrative + review types only (the three-plane model, 0052):

* diegetic tree — ``Cut -> Act -> Scene -> Beat -> Shot``;
* production deliverables — ``Deliverable`` (the film *becoming*);
* the market-facing plane — ``Marketing Asset`` (key art / one-sheet).

It does **not** create the process, the custom ``Mood`` / ``Look`` fields, or the
portfolio-level cascade (one-time structural steps — storyline 0024 / 0025); it *does*
map each type to its backlog level by level name (skipping any level the process does
not have yet). The system Test types and the disabled Epic / Issue / Task are left alone.

Usage::

    python scripts/provision_process.py                  # heal the .env process
    python scripts/provision_process.py --dry-run        # report drift only
    python scripts/provision_process.py --process "Name" # target a specific process

Reads ``ADO_ORG_URL`` / ``ADO_PROCESS_NAME`` from ``.env``; authenticates via
``DefaultAzureCredential`` (the local ``az login`` identity).
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path

# Make the `sequitur` package + sibling scripts importable (and load `.env`).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur.config import ADO_RESOURCE_ID  # noqa: E402  (import also loads .env)

# Reuse the minimal REST client + helpers from the project provisioner.
from scripts.provision_production import API, Ado  # noqa: E402


@dataclass(frozen=True)
class Wit:
    """A declared work-item type in the process template."""

    name: str
    color: str          # ADO palette hex (no '#')
    icon: str           # inherited-process glyph name
    description: str
    level: str          # backlog-level *display* name (Cuts/Acts/.../Shots)
    is_default: bool    # is this the level's default (creating) type?


#: The active template — the three planes of storyline 0052. Colours are ADO palette
#: values; icons are inherited-process glyphs. Note ``icon_crown`` is NOT one — it
#: silently falls back to ``icon_gift`` — so the crown uses ``icon_trophy``; and ``Shot``
#: is healed back to ``icon_clipboard`` (it had drifted to ``icon_megaphone``, which now
#: belongs to the market-facing ``Marketing Asset``).
TEMPLATE = [
    Wit("Cut", "f599a2", "icon_trophy",
        "The complete assembled work — the crown of the narrative tree "
        "(Cut -> Act -> Scene -> Beat -> Shot). Editorial's landing node; the board "
        "analogue of the code's edit Sequence. State tracks assembly maturity.",
        level="Cuts", is_default=True),
    Wit("Act", "773B93", "icon_list",
        "An act - a major movement of the story, under a Cut (edit.py Act).",
        level="Acts", is_default=True),
    Wit("Scene", "FF7B00", "icon_chat_bubble",
        "A scene - narrative unit under an Act (edit.py Scene).",
        level="Scenes", is_default=True),
    Wit("Beat", "009CCC", "icon_pull_request",
        "A beat - narrative unit under a Scene (edit.py Beat).",
        level="Beats", is_default=True),
    Wit("Shot", "60AF49", "icon_clipboard",
        "A shot - the leaf; the composed Shot (shot.py).",
        level="Shots", is_default=True),
    Wit("Deliverable", "fbd144", "icon_parachute",
        "A phase's reviewable deliverable — the film becoming (treatment, storyboard, "
        "dailies, rough/final cut). Filed by the AD/PA; reviewed at the gate.",
        level="Shots", is_default=False),
    Wit("Marketing Asset", "e56910", "icon_megaphone",
        "A campaign artifact about the film, for the market — key art / one-sheet / "
        "trailer / EPK. Anchors to the film as a released title (the Cut), not to any "
        "narrative node. The market-facing plane; the KeyArtist seat's output.",
        level="Shots", is_default=False),
]

#: The three-state workflow shared by every template type.
STATES = [
    ("To do", "b2b2b2", "Proposed", 1),
    ("Doing", "007acc", "InProgress", 2),
    ("Done", "339933", "Completed", 3),
]

_NEW = "(new)"  # sentinel ref for a would-be-created type in dry-run


class ProcessProvisioner:
    def __init__(self, ado: Ado, process_name: str, *, dry_run: bool) -> None:
        self.ado = ado
        self.process_name = process_name
        self.dry = dry_run
        self._pid: str | None = None

    def log(self, action: str, detail: str) -> None:
        prefix = "would " if self.dry else ""
        print(f"  {prefix}{action:<7} {detail}")

    def resolve_process(self) -> str:
        procs = self.ado("GET", f"_apis/work/processes?{API}").get("value", [])
        match = next((p for p in procs if p.get("name") == self.process_name), None)
        if not match:
            raise SystemExit(f"Process {self.process_name!r} not found. Set ADO_PROCESS_NAME in .env.")
        return match["typeId"]

    def _wits(self) -> dict[str, dict]:
        wits = self.ado("GET", f"_apis/work/processes/{self._pid}/workitemtypes?{API}").get("value", [])
        return {w["name"]: w for w in wits}

    def _levels(self) -> dict[str, str]:
        beh = self.ado("GET", f"_apis/work/processes/{self._pid}/behaviors?{API}").get("value", [])
        return {b["name"]: b["referenceName"] for b in beh}

    def ensure_wit(self, wit: Wit, existing: dict | None) -> str:
        """Create or heal a work-item type; return its reference name (or the sentinel)."""
        if existing is None:
            self.log("create", f"type '{wit.name}'")
            if self.dry:
                return _NEW
            created = self.ado("POST", f"_apis/work/processes/{self._pid}/workitemtypes?{API}",
                               {"name": wit.name, "description": wit.description,
                                "color": wit.color, "icon": wit.icon, "inheritsFrom": None})
            return created["referenceName"]
        ref = existing["referenceName"]
        drift = [k for k in ("color", "icon", "description")
                 if (existing.get(k) or "") != getattr(wit, k)]
        if drift:
            self.log("patch", f"type '{wit.name}' ({', '.join(drift)})")
            if not self.dry:
                self.ado("PATCH", f"_apis/work/processes/{self._pid}/workitemtypes/{ref}?{API}",
                         {"color": wit.color, "icon": wit.icon, "description": wit.description})
        else:
            self.log("ok", f"type '{wit.name}'")
        return ref

    def ensure_states(self, wit: Wit, ref: str) -> None:
        if ref == _NEW:  # created in dry-run; states would follow
            for name, *_ in STATES:
                self.log("state", f"'{wit.name}' + '{name}'")
            return
        have = {s["name"] for s in
                self.ado("GET", f"_apis/work/processes/{self._pid}/workitemtypes/{ref}/states?{API}").get("value", [])}
        for name, color, category, order in STATES:
            if name in have:
                continue
            self.log("state", f"'{wit.name}' + '{name}'")
            if not self.dry:
                self.ado("POST", f"_apis/work/processes/{self._pid}/workitemtypes/{ref}/states?{API}",
                         {"name": name, "color": color, "stateCategory": category, "order": order})

    def ensure_level(self, wit: Wit, ref: str, levels: dict[str, str]) -> None:
        level_ref = levels.get(wit.level)
        if not level_ref:
            self.log("skip", f"'{wit.name}' -> level '{wit.level}' (level absent)")
            return
        if ref == _NEW:  # created in dry-run; mapping would follow
            self.log("map", f"'{wit.name}' -> '{wit.level}' (default={wit.is_default})")
            return
        current = {b["behavior"]["id"] for b in
                   self.ado("GET", f"_apis/work/processes/{self._pid}/workItemTypesBehaviors/{ref}/behaviors?{API}").get("value", [])}
        if level_ref in current:
            self.log("ok", f"'{wit.name}' on '{wit.level}'")
            return
        self.log("map", f"'{wit.name}' -> '{wit.level}' (default={wit.is_default})")
        if not self.dry:
            self.ado("POST", f"_apis/work/processes/{self._pid}/workItemTypesBehaviors/{ref}/behaviors?{API}",
                     {"behavior": {"id": level_ref}, "isDefault": wit.is_default})

    def run(self) -> None:
        self._pid = self.resolve_process()
        print(f"Ensuring process template '{self.process_name}'"
              + (" [DRY RUN]" if self.dry else "") + " ...")
        existing = self._wits()   # read live even in dry-run, to report real drift
        levels = self._levels()
        for wit in TEMPLATE:
            ref = self.ensure_wit(wit, existing.get(wit.name))
            self.ensure_states(wit, ref)
            self.ensure_level(wit, ref, levels)
        print("Done." if not self.dry else "Dry run complete (no changes made).")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ensure the Sequitur process template (work-item types, icons, colours, states, levels).")
    parser.add_argument("--process", help="Process name (default: ADO_PROCESS_NAME from .env).")
    parser.add_argument("--dry-run", action="store_true", help="Report drift without making changes.")
    args = parser.parse_args()

    org_url = os.environ.get("ADO_ORG_URL")
    process_name = args.process or os.environ.get("ADO_PROCESS_NAME")
    if not org_url or not process_name:
        raise SystemExit("Set ADO_ORG_URL and ADO_PROCESS_NAME in .env (or pass --process).")

    ado = Ado(org_url, os.environ.get("ADO_RESOURCE_ID", ADO_RESOURCE_ID))
    ProcessProvisioner(ado, process_name, dry_run=args.dry_run).run()


if __name__ == "__main__":
    main()
