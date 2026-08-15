"""Smoke tests for the Screenwriter — the plan-phase story vocabulary.

Asserts against the *public* package surface (``sequitur``). Run directly
(``python tests/test_screenwriting.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Audience,
    Brief,
    DialogueMode,
    Department,
    FilmmakingStyle,
    Focus,
    FourthWall,
    Linearity,
    Macrogenre,
    MovieType,
    Pathway,
    Performer,
    Phase,
    Scope,
    Screenwriter,
    Stance,
    Supergenre,
    Voice,
)


def test_screenwriter_is_a_plan_phase_story_seat() -> None:
    assert Screenwriter.department is Department.STORY
    assert Screenwriter.phase is Phase.PLAN
    # It owns the taxonomy vocabulary — the closed enums are in its declared slice.
    for enum_type in (MovieType, Supergenre, Macrogenre, Pathway, Scope, Focus, Stance):
        assert enum_type in Screenwriter.vocabulary


def test_the_closed_layers_have_their_full_membership() -> None:
    assert len(MovieType) == 2
    assert len(Supergenre) == 11  # the eleven umbrellas (Ch. 2)
    assert len(Pathway) == 20  # the traditional baseline + 19 divergences (Ch. 6)
    assert len(Macrogenre) == 50  # the curated modifier list (Ch. 3)


def test_voice_defaults_to_the_traditional_voice() -> None:
    v = Voice()
    assert v.linearity is Linearity.LINEAR
    assert v.style is FilmmakingStyle.MODERN
    assert v.audience is Audience.BROAD
    assert v.performer is Performer.LIVE_ACTION
    assert v.dialogue_mode is DialogueMode.SPOKEN
    assert v.fourth_wall is FourthWall.INTACT


def test_heuristic_descriptor_is_the_neutral_slice_of_life() -> None:
    c = Screenwriter().propose(Brief(scene="a fox crossing a frozen field"))
    assert c.role == "Screenwriter"
    f = c.fields
    assert f["movie_type"] is MovieType.DRAMA
    assert f["supergenre"] is Supergenre.LIFE
    assert f["pathway"] is Pathway.TRADITIONAL
    assert (f["scope"], f["focus"], f["stance"]) == (Scope.LIMITED, Focus.PRIMARY, Stance.OBJECTIVE)
    assert f["macrogenres"] == [] and f["microgenres"] == []
    assert isinstance(f["voice"], Voice)


def test_producer_hints_override_the_descriptor() -> None:
    brief = Brief(
        scene="a heist in a rain-soaked city",
        hints={
            "supergenre": Supergenre.CRIME,
            "macrogenres": [Macrogenre.HEIST_CAPER, Macrogenre.GANGSTER],
            "microgenres": ["diamond vault"],
            "pathway": Pathway.NOIR,
            "scope": Scope.OMNISCIENT,
            "voice": Voice(dialogue_mode=DialogueMode.VOICEOVER),
        },
    )
    f = Screenwriter().propose(brief).fields
    assert f["supergenre"] is Supergenre.CRIME
    assert f["macrogenres"] == [Macrogenre.HEIST_CAPER, Macrogenre.GANGSTER]
    assert f["microgenres"] == ["diamond vault"]
    assert f["pathway"] is Pathway.NOIR
    assert f["scope"] is Scope.OMNISCIENT
    assert f["voice"].dialogue_mode is DialogueMode.VOICEOVER


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
