"""Bind shared production commands to one private production workspace."""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass(frozen=True)
class ProductionWorkspace:
    """Local identity and paths; the ADO board remains the production's control plane."""

    root: Path
    organization: str
    project_name: str
    project_id: str
    process: str
    artifact_namespace: str

    @classmethod
    def load(cls, root: str | Path) -> ProductionWorkspace:
        """Read an explicit manifest without network calls or environment fallbacks."""
        root = Path(root).resolve()
        data = json.loads((root / "production.json").read_text(encoding="utf-8"))
        if not isinstance(data, dict) or type(data.get("schemaVersion")) is not int or data["schemaVersion"] != 1:
            raise ValueError("production.json must use schemaVersion 1.")
        values = {}
        for field in ("organization", "projectName", "projectId", "process", "artifactNamespace"):
            value = data.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"production.json requires a non-empty {field}.")
            values[field] = value.strip()
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", values["organization"]):
            raise ValueError("production.json contains an invalid organization.")
        try:
            UUID(values["projectId"])
        except ValueError as exc:
            raise ValueError("production.json requires the ADO project GUID.") from exc
        namespace = values["artifactNamespace"]
        if namespace in {".", ".."} or any(c in namespace for c in '<>:"/\\|?*'):
            raise ValueError("artifactNamespace must be one output-store path segment.")
        return cls(
            root, values["organization"], values["projectName"], values["projectId"],
            values["process"], namespace,
        )

    @property
    def scratch(self) -> Path:
        """The selected project's disposable render workspace."""
        return self.root / ".local" / "scratch"

    def local_path(self, value: str | Path) -> Path:
        """Resolve a project-owned input/state path, rejecting another project's path."""
        path = (self.root / value).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError(f"Project-owned path is outside {self.root}: {value}")
        return path

    def environment(self, base: dict[str, str] | None = None) -> dict[str, str]:
        """Return child-only settings; never rewrite the shared engine's .env."""
        environment = dict(os.environ if base is None else base)
        environment.update({
            "ADO_ORG_URL": f"https://dev.azure.com/{self.organization}",
            "ADO_PROJECT": self.project_name,
            "ADO_PROCESS_NAME": self.process,
            "SEQUITUR_PROJECT_ID": self.project_id,
            "SEQUITUR_ARTIFACT_NAMESPACE": self.artifact_namespace,
            "SEQUITUR_PROJECT_ROOT": str(self.root),
            "SEQUITUR_OUTPUT_DIR": str(self.scratch),
            "TMP": str(self.scratch),
            "TEMP": str(self.scratch),
        })
        return environment

    def command(self, action: str, arguments: list[str], *, engine_root: Path) -> list[str]:
        """Compose existing arms with one binding, rather than duplicating film behavior."""
        scripts = {
            "plan": "scripts/deliver_plan.py",
            "audition": "scripts/audition.py",
            "assemble": "scripts/produce.py",
            "key-art": ".github/skills/keyartist/compose_key_art.py",
            "report": ".github/skills/assistant_director/report_to_board.py",
        }
        if action not in scripts:
            raise ValueError(f"Unknown production action: {action}")
        args = list(arguments)
        if any(arg.split("=", 1)[0] in {"--production", "--project-root", "--list-productions"} for arg in args):
            raise ValueError("The workspace manifest owns the production selection.")
        path_options = {"--state", "--cast", "--cast-state", "--treatment", "--board", "--local", "--out"}
        supplied = set()
        index = 0
        while index < len(args):
            option, separator, value = args[index].partition("=")
            if option in path_options:
                supplied.add(option)
                if separator:
                    args[index] = option + "=" + str(self.local_path(value))
                else:
                    if index + 1 == len(args) or args[index + 1].startswith("--"):
                        raise ValueError(f"{option} requires a project-local path.")
                    index += 1
                    args[index] = str(self.local_path(args[index]))
            index += 1
        if action == "audition" and "--state" not in supplied:
            args += ["--state", str(self.root / "state" / "cast.json")]
        if action == "key-art" and "--out" not in supplied:
            args += ["--out", str(self.scratch / "key_art.png")]
        selection = (
            [self.artifact_namespace] if action == "audition"
            else ["--production", self.project_name if action == "assemble" else self.artifact_namespace]
        )
        return [sys.executable, str(engine_root / scripts[action]), *selection, *args]
