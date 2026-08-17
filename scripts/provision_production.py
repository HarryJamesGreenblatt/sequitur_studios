"""Provision a new Production instance's board on Azure DevOps (storyline 0025).

The inherited **process** (``SequiturProductionProcess``) is the org-level *template*
for the board's structure — the Act/Scene/Beat/Shot work-item types, the ``Mood`` /
``Look`` fields, and the backlog-level cascade that puts ``Shot`` on the Requirement
tier. A production *instance* is one **project** on that process, plus the per-project
scaffolding a fresh project does **not** inherit, which this script stands up
idempotently:

* the department **Area Paths** (Direction, Story, Art, Camera, Lighting, Grip,
  Editorial, Color, Sound) plus **Marketing** (the market-facing area, not a production
  craft — mirrors the KeyArtist seat that sits outside the crew, storyline 0052);
* the default team set to include child areas (so its board shows the whole tree);
* a **team per department**, each scoped to its Area Path (the per-crew bucket);
* each team's **backlog iteration** (else the board errors ``TF400509``) and
  **backlog-level visibilities** (else the custom Acts/Scenes levels stay hidden);
* the three **phase iterations** -- ``1 🎬 Pre-Production``, ``2 🎥 Production``,
  ``3 ✂️ Post-Production`` -- demonstrably-named (dateless) sprints that realise the
  phase axis, with every team subscribed to all three so each crew gets a Pre/Prod/Post
  switcher over its bucket. The leading digit forces ADO's alphabetical "current" pick
  onto Pre-Production (the emoji is decoration). These are the board side of the code's
  :class:`~sequitur.crew.role.Phase` (``plan``/``shoot``/``assemble``); the provider
  seam maps between them.

This is the infrastructure sibling of :class:`sequitur.production.AzureDevOpsProduction`
(that seam *reads/writes* an existing board; this script *stands one up*). It reproduces
"where we are now" for a new production — **no sample items** unless ``--with-example``.

Usage::

    python scripts/provision_production.py "My New Film"
    python scripts/provision_production.py "My New Film" --with-example
    python scripts/provision_production.py "ASequiturProduction" --dry-run   # detect-only

Reads non-secret pointers from ``.env`` (``ADO_ORG_URL``, ``ADO_PROCESS_NAME``);
authenticates with ``DefaultAzureCredential`` (the local ``az login`` identity).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Make the `sequitur` package importable (and load `.env`) when run as a bare script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur.config import ADO_RESOURCE_ID  # noqa: E402  (import also loads .env)

API = "api-version=7.1"

#: The department Area-Path / Team names. Most mirror the code's ``Department`` enum:
#: **Story** (Screenwriter), **Art** (Production Designer / KeyArtist) are the plan-phase
#: seats; note the lighting department's board name is "Lighting" (the code's
#: ``Department.ELECTRIC`` — Appendix D — surfaces as "Lighting" on the board).
#: **Marketing** is not a production craft: it's the home of the market-facing plane
#: (the ``Marketing Asset`` WIT — key art / one-sheet), whose seat (KeyArtist) sits
#: outside the crew by design (storyline 0052).
DEPARTMENTS = ["Direction", "Story", "Art", "Camera", "Lighting", "Grip", "Editorial", "Color", "Sound", "Marketing"]

#: The three production phases, as named (dateless) iteration nodes. This is the board
#: side of the code's ``Phase`` enum (``plan`` -> Pre-Production, ``shoot`` -> Production,
#: ``assemble`` -> Post-Production); delivery is out of scope. Every team subscribes to
#: all three, so the Sprints switcher reads the phase names rather than "Sprint 1/2/3".
#: The leading digit is load-bearing, not cosmetic: with no dates, ADO marks the
#: *alphabetically-first* iteration "current", so the number forces sort order and pins a
#: fresh production to open on Pre-Production (verified empirically). The emoji is pure
#: decoration -- it sorts high (well above ASCII), so it can't carry the ordering itself.
PHASES = [
    "1 \U0001F3AC Pre-Production",   # clapperboard
    "2 \U0001F3A5 Production",       # movie camera
    "3 \u2702\uFE0F Post-Production",  # scissors
]


class Ado:
    """A minimal Azure DevOps REST client (stdlib urllib + DefaultAzureCredential)."""

    def __init__(self, org_url: str, resource_id: str) -> None:
        self.org_url = org_url.rstrip("/")
        self.resource_id = resource_id
        self._cred = None

    def _token(self) -> str:
        if self._cred is None:
            from azure.identity import DefaultAzureCredential

            self._cred = DefaultAzureCredential()
        return self._cred.get_token(f"{self.resource_id}/.default").token

    def __call__(self, method: str, path: str, body=None, *, patch: bool = False):
        url = f"{self.org_url}/{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Authorization": f"Bearer {self._token()}", "Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json-patch+json" if patch else "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                text = resp.read().decode("utf-8")
                return json.loads(text) if text else {}
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"{method} {url} -> {exc.code}: {exc.read().decode('utf-8')}") from None


def _q(segment: str) -> str:
    """URL-encode a single path segment (team names contain spaces)."""
    return urllib.parse.quote(segment, safe="")


class Provisioner:
    def __init__(self, ado: Ado, project: str, *, dry_run: bool) -> None:
        self.ado = ado
        self.project = project
        self.dry = dry_run
        self._project_id: str | None = None

    def log(self, action: str, detail: str) -> None:
        prefix = "would " if self.dry else ""
        print(f"  {prefix}{action:<8} {detail}")

    # -- process + project -------------------------------------------------

    def resolve_process(self, name: str) -> str:
        procs = self.ado("GET", f"_apis/work/processes?{API}").get("value", [])
        match = next((p for p in procs if p.get("name") == name), None)
        if not match:
            raise SystemExit(f"Process {name!r} not found in the org. Set ADO_PROCESS_NAME in .env.")
        return match["typeId"]

    def ensure_project(self, process_type_id: str) -> None:
        try:
            proj = self.ado("GET", f"_apis/projects/{_q(self.project)}?{API}")
            self._project_id = proj["id"]
            self.log("exists", f"project '{self.project}'")
            return
        except RuntimeError:
            pass  # 404 -> create it
        self.log("create", f"project '{self.project}' (on the process)")
        if self.dry:
            return
        op = self.ado(
            "POST",
            f"_apis/projects?{API}",
            {
                "name": self.project,
                "description": "A Sequitur Studios production instance.",
                "capabilities": {
                    "versioncontrol": {"sourceControlType": "Git"},
                    "processTemplate": {"templateTypeId": process_type_id},
                },
            },
        )
        self._wait_operation(op.get("id"))
        proj = self.ado("GET", f"_apis/projects/{_q(self.project)}?{API}")
        self._project_id = proj["id"]

    def _wait_operation(self, op_id: str, *, tries: int = 30) -> None:
        for _ in range(tries):
            status = self.ado("GET", f"_apis/operations/{op_id}?{API}").get("status")
            if status == "succeeded":
                return
            if status in ("failed", "cancelled"):
                raise SystemExit(f"Project creation {status}.")
            time.sleep(2)
        raise SystemExit("Project creation timed out.")

    @property
    def project_id(self) -> str:
        if self._project_id is None:  # dry-run on a not-yet-existing project
            return self.project
        return self._project_id

    # -- areas -------------------------------------------------------------

    def ensure_areas(self) -> None:
        existing = set()
        try:
            root = self.ado("GET", f"{_q(self.project)}/_apis/wit/classificationnodes/areas?{API}&$depth=1")
            existing = {c["name"] for c in root.get("children", [])}
        except RuntimeError:
            pass  # project may not exist yet (dry-run)
        for dept in DEPARTMENTS:
            if dept in existing:
                self.log("exists", f"area '{dept}'")
            else:
                self.log("create", f"area '{dept}'")
                if not self.dry:
                    self.ado("POST", f"{_q(self.project)}/_apis/wit/classificationnodes/areas?{API}", {"name": dept})

    # -- teams -------------------------------------------------------------

    def _teams(self) -> dict[str, str]:
        try:
            vals = self.ado("GET", f"_apis/projects/{self.project_id}/teams?{API}").get("value", [])
            return {t["name"]: t["id"] for t in vals}
        except RuntimeError:
            return {}

    def ensure_teams(self) -> None:
        teams = self._teams()
        for dept in DEPARTMENTS:
            if dept in teams:
                self.log("exists", f"team '{dept}'")
            else:
                self.log("create", f"team '{dept}'")
                if not self.dry:
                    self.ado("POST", f"_apis/projects/{self.project_id}/teams?{API}",
                             {"name": dept, "description": f"{dept} department bucket - Area Path {self.project}\\{dept}."})
            # Point the team at its department Area Path.
            area = f"{self.project}\\{dept}"
            self.log("scope", f"team '{dept}' -> area '{area}'")
            if not self.dry:
                self._set_area(dept, area, include_children=False)

    def _set_area(self, team: str, area: str, *, include_children: bool) -> None:
        self.ado("PATCH", f"{_q(self.project)}/{_q(team)}/_apis/work/teamsettings/teamfieldvalues?{API}",
                 {"defaultValue": area, "values": [{"value": area, "includeChildren": include_children}]})

    def default_team_includes_children(self) -> None:
        team = f"{self.project} Team"
        self.log("config", f"default team '{team}' includeChildren=true")
        if not self.dry:
            self._set_area(team, self.project, include_children=True)

    # -- team settings: iteration + backlog visibilities -------------------

    def configure_team_settings(self) -> None:
        # Root iteration id (the backlog iteration every team needs).
        try:
            root_iter = self.ado("GET", f"{_q(self.project)}/_apis/wit/classificationnodes/iterations?{API}")["identifier"]
        except (RuntimeError, KeyError):
            self.log("skip", "team settings (project/iteration not resolvable in dry-run)")
            return
        # The custom portfolio levels (Acts/Scenes) that new teams hide by default.
        behaviors = self.ado("GET", f"_apis/work/processes/{self._process_type_id}/behaviors?{API}").get("value", [])
        custom = [b["referenceName"] for b in behaviors if b.get("referenceName", "").startswith("Custom.")]
        visibilities = {ref: True for ref in custom}

        teams = [f"{self.project} Team", *DEPARTMENTS]
        for team in teams:
            self.log("config", f"team '{team}' backlog iteration + visibilities")
            if not self.dry:
                self.ado("PATCH", f"{_q(self.project)}/{_q(team)}/_apis/work/teamsettings?{API}",
                         {"backlogIteration": root_iter, "defaultIteration": root_iter, "backlogVisibilities": visibilities})

    # -- phase iterations (the named Pre/Prod/Post sprints) ----------------

    def ensure_iterations(self) -> dict[str, str]:
        """Create the three named phase iterations; return ``{name: identifier}``.

        Idempotent and non-destructive: existing nodes are reused and the project's
        default ``Sprint N`` iterations are left untouched (department teams start with
        no subscriptions, so their switcher shows only the phases regardless).
        """
        existing: dict[str, str] = {}
        try:
            root = self.ado("GET", f"{_q(self.project)}/_apis/wit/classificationnodes/iterations?{API}&$depth=1")
            existing = {c["name"]: c["identifier"] for c in root.get("children", [])}
        except RuntimeError:
            pass  # project may not exist yet (dry-run)
        phase_ids: dict[str, str] = {}
        for phase in PHASES:
            if phase in existing:
                self.log("exists", f"iteration '{phase}'")
                phase_ids[phase] = existing[phase]
            else:
                self.log("create", f"iteration '{phase}' (dateless)")
                if not self.dry:
                    node = self.ado("POST", f"{_q(self.project)}/_apis/wit/classificationnodes/iterations?{API}", {"name": phase})
                    phase_ids[phase] = node["identifier"]
        return phase_ids

    def subscribe_teams_to_phases(self, phase_ids: dict[str, str]) -> None:
        """Subscribe every team to the three phase iterations (the Sprints switcher)."""
        teams = [f"{self.project} Team", *DEPARTMENTS]
        for team in teams:
            current: set[str] = set()
            if not self.dry:
                try:
                    subs = self.ado("GET", f"{_q(self.project)}/{_q(team)}/_apis/work/teamsettings/iterations?{API}").get("value", [])
                    current = {s["id"] for s in subs}
                except RuntimeError:
                    pass
            for phase in PHASES:
                ident = phase_ids.get(phase)
                if not self.dry and ident in current:
                    self.log("exists", f"team '{team}' subscribed to '{phase}'")
                    continue
                self.log("sub", f"team '{team}' -> iteration '{phase}'")
                if not self.dry and ident:
                    self.ado("POST", f"{_q(self.project)}/{_q(team)}/_apis/work/teamsettings/iterations?{API}", {"id": ident})

    # -- optional example tree --------------------------------------------

    def create_example(self) -> None:
        self.log("example", "Cut -> Act -> Scene -> Beat -> Shot x2 (with Mood/Look)")
        if self.dry:
            return
        cut = self._wi("Cut", "Rough Cut", "Editorial")
        act = self._wi("Act", "Act I - Arrival", "Direction", parent=cut)
        scene = self._wi("Scene", "Scene 1 - The Platform", "Direction", parent=act)
        beat = self._wi("Beat", "Beat 1 - The train pulls in", "Editorial", parent=scene)
        self._wi("Shot", "Shot 1 - Wide: empty platform", "Camera", parent=beat,
                 fields={"Custom.Mood": "anticipation, stillness", "Custom.Look": "Cool"})
        self._wi("Shot", "Shot 2 - CU: her face at the window", "Camera", parent=beat,
                 fields={"Custom.Mood": "quiet hope", "Custom.Look": "Golden Hour"})

    def _wi(self, wit: str, title: str, area: str, *, parent: dict | None = None, fields: dict | None = None) -> dict:
        ops = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
            {"op": "add", "path": "/fields/System.AreaPath", "value": f"{self.project}\\{area}"},
        ]
        for name, value in (fields or {}).items():
            ops.append({"op": "add", "path": f"/fields/{name}", "value": value})
        if parent is not None:
            ops.append({"op": "add", "path": "/relations/-",
                        "value": {"rel": "System.LinkTypes.Hierarchy-Reverse", "url": parent["url"]}})
        created = self.ado("POST", f"{_q(self.project)}/_apis/wit/workitems/{_q('$' + wit)}?{API}", ops, patch=True)
        print(f"    {wit:<6} #{created['id']}  {title}")
        return created

    # -- orchestration -----------------------------------------------------

    def run(self, process_name: str, *, with_example: bool) -> None:
        self._process_type_id = self.resolve_process(process_name)
        print(f"Provisioning production '{self.project}' on process '{process_name}'"
              + (" [DRY RUN]" if self.dry else "") + " ...")
        self.ensure_project(self._process_type_id)
        self.ensure_areas()
        self.default_team_includes_children()
        self.ensure_teams()
        self.configure_team_settings()
        self.subscribe_teams_to_phases(self.ensure_iterations())
        if with_example:
            self.create_example()
        print("Done." if not self.dry else "Dry run complete (no changes made).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stand up a new Sequitur production board on Azure DevOps.")
    parser.add_argument("project", help="The new production's project name.")
    parser.add_argument("--with-example", action="store_true", help="Also seed a small Act->Scene->Beat->Shot example tree.")
    parser.add_argument("--dry-run", action="store_true", help="Report intended actions without making any changes.")
    args = parser.parse_args()

    org_url = os.environ.get("ADO_ORG_URL")
    process_name = os.environ.get("ADO_PROCESS_NAME")
    if not org_url or not process_name:
        raise SystemExit("Set ADO_ORG_URL and ADO_PROCESS_NAME in .env.")

    ado = Ado(org_url, os.environ.get("ADO_RESOURCE_ID", ADO_RESOURCE_ID))
    Provisioner(ado, args.project, dry_run=args.dry_run).run(process_name, with_example=args.with_example)


if __name__ == "__main__":
    main()
