"""Smoke tests for the Casting Director — the plan-phase casting seat and the cast entities.

Asserts against the *public* package surface (``sequitur``). Run directly
(``python tests/test_casting.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Actor,
    AgeBand,
    Billing,
    Brief,
    CastingDirector,
    Character,
    Department,
    Phase,
)


def test_casting_director_is_a_plan_phase_casting_seat() -> None:
    assert CastingDirector.department is Department.CASTING
    assert CastingDirector.phase is Phase.PLAN
    # It owns the casting vocabulary — the closed axes are in its declared slice.
    for enum_type in (AgeBand, Billing):
        assert enum_type in CastingDirector.vocabulary


def test_the_closed_axes_have_their_full_membership() -> None:
    assert len(AgeBand) == 6  # child / teen / young-adult / adult / middle-aged / senior
    assert AgeBand.ADULT in AgeBand  # the unmarked default (Ch. 18 suitability)
    assert len(Billing) == 2  # principal vs. background (Ch. 18)


def test_heuristic_leaves_the_cast_empty_for_the_persona() -> None:
    # A cannot read the treatment; the cast is the persona (B)'s to design from the story.
    c = CastingDirector().propose(Brief(scene="a lighthouse at dusk"))
    assert c.role == "Casting Director"
    assert c.fields["cast"] == []


def test_producer_hints_can_supply_a_cast() -> None:
    nora = Character(name="Nora", role="protagonist", age_band=AgeBand.YOUNG_ADULT)
    f = CastingDirector().propose(Brief(scene="the platform", hints={"cast": [nora]})).fields
    assert f["cast"] == [nora]


def test_a_character_holds_its_audition_and_its_cast_actor() -> None:
    # An Actor plays a Character: candidates audition, one is cast, its reference is the look.
    a1 = Actor(look="weathered, grey-eyed", reference="store/nora/cand-1.png")
    a2 = Actor(look="younger, softer", reference="store/nora/cand-2.png")
    nora = Character(name="Nora", billing=Billing.PRINCIPAL, candidates=[a1, a2], cast=a1)
    assert nora.cast is a1
    assert len(nora.candidates) == 2
    assert nora.cast.reference == "store/nora/cand-1.png"


def test_the_plan_carries_the_cast_as_a_third_axis() -> None:
    from sequitur import Engine

    nora = Character(name="Nora")
    plan = Engine().plan(Brief(scene="the platform", hints={"cast": [nora]}))
    assert plan.cast == [nora]  # routed into the plan's cast axis, disjoint from story/design


def test_plan_crew_now_seats_story_design_and_casting() -> None:
    from sequitur import plan_crew

    titles = {type(r).__name__ for r in plan_crew()}
    assert {"Screenwriter", "ProductionDesigner", "CastingDirector"} <= titles


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
