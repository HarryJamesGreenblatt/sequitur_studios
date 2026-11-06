"""Focused guards for explicit production identity and project-owned paths."""

import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur.config import get_ado_config
from sequitur.crew.role import Phase
from sequitur.gate import Deliverable
from sequitur.production import AzureDevOpsProduction
from sequitur.workspace import ProductionWorkspace


def _fixture(root: Path, **overrides) -> ProductionWorkspace:
    data = {
        "schemaVersion": 1, "organization": "example-org",
        "projectName": "Film", "projectId": "11111111-1111-4111-8111-111111111111",
        "process": "FilmProcess", "artifactNamespace": "OriginalFilmKey",
    }
    data.update(overrides)
    (root / "production.json").write_text(json.dumps(data), encoding="utf-8")
    return ProductionWorkspace.load(root)


def test_workspace_binds_id_namespace_and_paths_without_changing_parent_environment():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory).resolve()
        workspace = _fixture(root)
        base = {"ADO_PROJECT": "AnotherFilm"}
        environment = workspace.environment(base)
        assert base == {"ADO_PROJECT": "AnotherFilm"}
        assert environment["ADO_PROJECT"] == "Film"
        assert environment["SEQUITUR_ARTIFACT_NAMESPACE"] == "OriginalFilmKey"
        assert environment["SEQUITUR_OUTPUT_DIR"] == str(root / ".local" / "scratch")
        command = workspace.command("audition", ["--cast", "inputs/spec.json"], engine_root=root)
        assert "OriginalFilmKey" in command
        assert command[command.index("--cast") + 1] == str(root / "inputs" / "spec.json")
        assert command[command.index("--state") + 1] == str(root / "state" / "cast.json")


def test_workspace_rejects_another_projects_state_and_selector_overrides():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory).resolve()
        workspace = _fixture(root)
        for arguments in [
            ["--state", "../OtherFilm/cast.json"],
            ["--production", "OtherFilm"],
            ["--production=OtherFilm"],
        ]:
            try:
                workspace.command("audition", arguments, engine_root=root)
            except ValueError:
                pass
            else:
                raise AssertionError(f"Accepted a foreign project override: {arguments}")


def test_workspace_rejects_unresolved_or_unsafe_manifest_identity():
    with tempfile.TemporaryDirectory() as directory:
        for invalid in [{"projectId": "not-a-guid"}, {"artifactNamespace": "../OtherFilm"}]:
            try:
                _fixture(Path(directory), **invalid)
            except ValueError:
                pass
            else:
                raise AssertionError("Invalid production identity was accepted")


def test_bound_config_keeps_board_guid_and_artifact_namespace_separate():
    with tempfile.TemporaryDirectory() as directory:
        workspace = _fixture(Path(directory))
        with patch.dict(os.environ, workspace.environment({}), clear=True):
            config = get_ado_config(project="OriginalFilmKey")
            provider = AzureDevOpsProduction(config=config)
            assert config.project == "Film"
            assert workspace.project_id in provider._project_url("wit/wiql")
            try:
                get_ado_config(project="AnotherFilm")
            except ValueError:
                pass
            else:
                raise AssertionError("Bound config selected another production")


def test_bound_provider_rejects_foreign_reports_and_verdicts_before_transport():
    with tempfile.TemporaryDirectory() as directory:
        workspace = _fixture(Path(directory))
        with patch.dict(os.environ, workspace.environment({}), clear=True):
            provider = AzureDevOpsProduction()
        foreign = Deliverable(production="AnotherFilm", phase=Phase.PLAN, name="treatment.md", ref="")
        with patch.object(provider, "_request", side_effect=AssertionError("Unexpected network call")):
            for operation in (provider.report, provider.record_verdict):
                try:
                    operation(foreign)
                except ValueError:
                    pass
                else:
                    raise AssertionError("A foreign production was accepted")


def test_fetched_reports_keep_the_bound_artifact_namespace_after_a_display_name_change():
    with tempfile.TemporaryDirectory() as directory:
        workspace = _fixture(Path(directory))
        with patch.dict(os.environ, workspace.environment({}), clear=True):
            provider = AzureDevOpsProduction()
        responses = [
            {"workItems": [{"id": 1}]},
            {"value": [{"fields": {"System.Title": "[plan] treatment.md", "System.State": "To do"}}]},
        ]
        with patch.object(provider, "_request", side_effect=responses):
            report, = provider.fetch_reports()
        assert report.production == "OriginalFilmKey"


def test_unbound_explicit_project_selection_remains_supported():
    with patch.dict(os.environ, {"ADO_ORG_URL": "https://dev.azure.com/example", "ADO_PROJECT": "Default"}, clear=True):
        config = get_ado_config(project="Explicit")
        assert config.project == "Explicit"
        assert config.project_id is None and config.production_key is None


if __name__ == "__main__":
    tests = [value for key, value in sorted(globals().items()) if key.startswith("test_")]
    for run in tests:
        run()
        print(f"ok {run.__name__}")
