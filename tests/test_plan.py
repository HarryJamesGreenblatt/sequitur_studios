"""Smoke tests for the plan-phase deliverables — treatment + poster through the Gate.

Asserts against the *public* package surface (``sequitur``). Run directly
(``python tests/test_plan.py``) or via pytest.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Brief,
    ConceptStance,
    Director,
    Engine,
    Gate,
    GateStatus,
    ImageStudio,
    LocalFolderOutputStore,
    Medium,
    Phase,
    RenderResult,
    Screenwriter,
    Supergenre,
    build_poster_prompt,
    register,
)


def _heist_plan():
    brief = Brief(
        scene="a heist in a rain-soaked city",
        mood="cold, tense",
        hints={
            "supergenre": Supergenre.CRIME,
            "visual_concept": "the city as a rain-streaked maze",
            "concept_stance": ConceptStance.CONTRAST,
            "motifs": ["venetian blinds", "neon reflections"],
        },
    )
    return Engine().plan(brief)


def test_poster_prompt_leads_with_the_visual_concept() -> None:
    prompt = build_poster_prompt(_heist_plan())
    assert "the city as a rain-streaked maze" in prompt
    assert "venetian blinds" in prompt and "neon reflections" in prompt
    assert "cold, tense" in prompt  # the mood carries through


def test_poster_prompt_falls_back_to_scene_when_concept_blank() -> None:
    # The heuristic tier leaves visual_concept blank — the poster falls back to the scene.
    plan = Engine().plan(Brief(scene="a lighthouse at dusk"))
    assert plan.design["visual_concept"] == ""
    assert "a lighthouse at dusk" in build_poster_prompt(plan)


def test_treatment_derives_from_the_story_descriptor() -> None:
    text = Screenwriter().treatment(_heist_plan())
    assert text.startswith("# Treatment")
    assert "crime" in text.lower()  # the supergenre made it into the prose
    assert "Mood:" in text


def test_deliver_plan_files_treatment_and_poster() -> None:
    class FakeStudio:
        medium = Medium.STILL

        def render(self, prompt, *, out_path=None):
            Path(out_path).write_bytes(b"poster-bytes")
            return RenderResult("fake-native", Path(out_path))

    register(Medium.STILL, lambda: FakeStudio())
    try:
        with tempfile.TemporaryDirectory() as d:
            store = LocalFolderOutputStore(Path(d) / "store")
            gate = Gate(store, production="HeistNoir")
            plan = _heist_plan()
            scratch = Path(d) / "poster.png"

            treatment, poster = Director().deliver_plan(plan, gate=gate, out_path=scratch)

            # Two PENDING plan-phase deliverables, filed under <production>/plan/.
            for deliverable in (treatment, poster):
                assert deliverable.production == "HeistNoir"
                assert deliverable.phase is Phase.PLAN
                assert deliverable.status is GateStatus.PENDING
            assert Path(treatment.ref) == Path(d) / "store" / "HeistNoir" / "plan" / "treatment.md"
            assert Path(poster.ref) == Path(d) / "store" / "HeistNoir" / "plan" / "poster.png"
            # The bytes made it durably into the store.
            assert Path(treatment.ref).read_text(encoding="utf-8").startswith("# Treatment")
            assert Path(poster.ref).read_bytes() == b"poster-bytes"
    finally:
        register(Medium.STILL, ImageStudio)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
