"""Run an existing production arm inside one explicit project boundary."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

_ENGINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ENGINE_ROOT))

from sequitur.workspace import ProductionWorkspace  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=os.environ.get("SEQUITUR_PROJECT_ROOT"))
    parser.add_argument("--print-command", action="store_true", help="Resolve identity and paths without running the arm.")
    parser.add_argument("action", choices=("plan", "audition", "assemble", "key-art", "report"))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if not args.project_root:
        parser.error("--project-root is required outside a project-scoped session.")
    try:
        workspace = ProductionWorkspace.load(args.project_root)
        command = workspace.command(args.action, args.arguments, engine_root=_ENGINE_ROOT)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if args.print_command:
        print(json.dumps({
            "project": workspace.project_name, "projectId": workspace.project_id,
            "cwd": str(workspace.root), "scratch": str(workspace.scratch),
            "artifactNamespace": workspace.artifact_namespace, "command": command,
        }, indent=2))
        return 0
    (workspace.root / "state").mkdir(parents=True, exist_ok=True)
    workspace.scratch.mkdir(parents=True, exist_ok=True)
    return subprocess.run(command, cwd=workspace.root, env=workspace.environment(), check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
