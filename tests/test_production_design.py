"""Smoke tests for the Production Designer — the plan-phase design vocabulary.

Asserts against the *public* package surface (``sequitur``). Run directly
(``python tests/test_production_design.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Brief,
    ConceptStance,
    Department,
    EraMarker,
    MediumLook,
    Phase,
    ProductionDesigner,
    SetKind,
)


def test_production_designer_is_a_plan_phase_art_seat() -> None:
    assert ProductionDesigner.department is Department.ART
    assert ProductionDesigner.phase is Phase.PLAN
    # It owns the design vocabulary — the closed enums are in its declared slice.
    for enum_type in (ConceptStance, MediumLook, EraMarker, SetKind):
        assert enum_type in ProductionDesigner.vocabulary


def test_the_closed_axes_have_their_full_membership() -> None:
    assert len(ConceptStance) == 2  # underscore vs. contrast (Ch. 4)
    assert len(MediumLook) == 3  # film / video / digital (Ch. 3)
    assert len(SetKind) == 2  # interior / exterior (Ch. 5)
    assert EraMarker.CONTEMPORARY in EraMarker  # the unmarked default (Ch. 3)


def test_heuristic_descriptor_is_the_neutral_contemporary_design() -> None:
    c = ProductionDesigner().propose(Brief(scene="a lighthouse at dusk"))
    assert c.role == "Production Designer"
    f = c.fields
    # The central concept is left blank for the persona (B) — A lands only the axes.
    assert f["visual_concept"] == ""
    assert f["concept_stance"] is ConceptStance.UNDERSCORE
    assert f["medium_look"] is MediumLook.DIGITAL
    assert f["era"] is EraMarker.CONTEMPORARY
    assert f["set_kind"] is SetKind.INTERIOR
    assert f["motifs"] == []


def test_producer_hints_override_the_descriptor() -> None:
    brief = Brief(
        scene="a detective's office, rain on the glass",
        hints={
            "visual_concept": "the city as a rain-streaked maze",
            "concept_stance": ConceptStance.CONTRAST,
            "medium_look": MediumLook.FILM,
            "era": EraMarker.NTSC_COLOR,
            "set_kind": SetKind.EXTERIOR,
            "motifs": ["venetian blinds", "neon reflections"],
        },
    )
    f = ProductionDesigner().propose(brief).fields
    assert f["visual_concept"] == "the city as a rain-streaked maze"
    assert f["concept_stance"] is ConceptStance.CONTRAST
    assert f["medium_look"] is MediumLook.FILM
    assert f["era"] is EraMarker.NTSC_COLOR
    assert f["set_kind"] is SetKind.EXTERIOR
    assert f["motifs"] == ["venetian blinds", "neon reflections"]


def test_plan_crew_now_seats_both_story_and_design() -> None:
    from sequitur import plan_crew

    titles = {type(r).__name__ for r in plan_crew()}
    assert {"Screenwriter", "ProductionDesigner"} <= titles


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
