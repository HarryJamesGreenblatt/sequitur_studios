"""Smoke tests for the production seam — the board <-> Brief / Sequence bridge.

Exercises the ``LocalFolderProduction`` test double end-to-end through the *real*
crew ``Engine`` — no network, no Azure DevOps — so the round-trip (board tree ->
``Brief`` -> assembled ``Sequence`` -> board) is covered offline. Asserts against
the public package surface. Run directly (``python tests/test_production.py``) or
via pytest.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    AzureDevOpsProduction,
    Engine,
    LocalFolderProduction,
    Look,
    ProductionProvider,
)


def _fixture(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "scene": "Scene 1 - The Platform",
                "shots": [
                    {"scene": "Wide: empty platform", "mood": "stillness", "look": "Cool"},
                    {"scene": "CU: her face", "mood": "quiet hope", "look": "Golden Hour"},
                ],
            }
        ),
        encoding="utf-8",
    )


def test_providers_satisfy_the_protocol() -> None:
    # runtime_checkable: the concrete backends structurally implement the seam.
    with tempfile.TemporaryDirectory() as d:
        assert isinstance(LocalFolderProduction(Path(d) / "p.json"), ProductionProvider)
    assert hasattr(AzureDevOpsProduction, "read_brief")
    assert hasattr(AzureDevOpsProduction, "write_sequence")


def test_read_brief_reads_the_board_tree() -> None:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "p.json"
        _fixture(path)
        brief = LocalFolderProduction(path).read_brief()
    assert brief.scene == "Scene 1 - The Platform"
    assert [s.scene for s in brief.shots] == ["Wide: empty platform", "CU: her face"]
    assert brief.shots[0].mood == "stillness"
    # Per-shot look aggregates to the first shot's look (v1 limitation).
    assert brief.hints["look"] is Look.COOL


def test_scene_argument_overrides_the_board_label() -> None:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "p.json"
        _fixture(path)
        brief = LocalFolderProduction(path).read_brief(scene="A different label")
    assert brief.scene == "A different label"


def test_round_trip_writes_the_applied_grade_back() -> None:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "p.json"
        _fixture(path)
        provider = LocalFolderProduction(path)

        brief = provider.read_brief()
        sequence = Engine().assemble(brief)  # the real crew assembles a graded edit
        provider.write_sequence(sequence)

        written = json.loads(path.read_text(encoding="utf-8"))
    # The engine applies the brief's (aggregated) look as a uniform base grade,
    # so every shot records that applied look on write.
    assert [s["look"] for s in written["shots"]] == ["Cool", "Cool"]


def test_write_appends_when_sequence_is_longer_than_the_board() -> None:
    from sequitur import Brief, Shot

    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "p.json"
        path.write_text(json.dumps({"scene": "s", "shots": []}), encoding="utf-8")
        provider = LocalFolderProduction(path)

        brief = Brief(scene="s", shots=[Shot(scene="a"), Shot(scene="b")], hints={"look": Look.NOIR})
        provider.write_sequence(Engine().assemble(brief))

        written = json.loads(path.read_text(encoding="utf-8"))
    assert [s["scene"] for s in written["shots"]] == ["a", "b"]
    assert all(s["look"] == "Noir" for s in written["shots"])


def test_engine_runs_a_production_board_to_board() -> None:
    # The Engine reads the Brief from the provider, assembles, and writes back — in one call.
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "p.json"
        _fixture(path)
        provider = LocalFolderProduction(path)

        sequence = Engine().run_production(provider)

        written = json.loads(path.read_text(encoding="utf-8"))
    # A graded edit came back, and its look was recorded onto every board shot.
    assert len(sequence.timeline()) == 2
    assert all(entry.clip.grade is not None for entry in sequence.timeline())
    assert [s["look"] for s in written["shots"]] == ["Cool", "Cool"]


def test_ado_production_is_parameterized_by_project() -> None:
    # One ADO project = one Production. The project is a parameter (explicit ->
    # env default); constructing the provider builds config but hits no network.
    import os

    from sequitur.config import get_ado_config

    saved = {k: os.environ.get(k) for k in ("ADO_ORG_URL", "ADO_PROJECT")}
    try:
        os.environ["ADO_ORG_URL"] = "https://dev.azure.com/testorg"
        os.environ["ADO_PROJECT"] = "DefaultProduction"
        # Absent an argument, the .env pointer is the default active production.
        assert get_ado_config().project == "DefaultProduction"
        assert AzureDevOpsProduction().config.project == "DefaultProduction"
        # An explicit project overrides the default — the multi-production selector.
        assert get_ado_config(project="HeistNoir").project == "HeistNoir"
        assert AzureDevOpsProduction(project="HeistNoir").config.project == "HeistNoir"
        # The org stays the studio-wide constant regardless of the production.
        assert AzureDevOpsProduction(project="HeistNoir").config.org_url == "https://dev.azure.com/testorg"
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
