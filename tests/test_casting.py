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
    build_character_prompt,
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


def test_shot_carries_its_cast_and_exposes_locked_references() -> None:
    # The diegetic join (storyline 0057): a Shot knows which Characters are in frame,
    # and can surface their locked keyframes for a backend to condition on.
    from sequitur import Shot, build_image_prompt

    nora = Character(
        name="Nora",
        essence="stubborn tenderness",
        candidates=[Actor(look="weathered, grey-eyed", reference="store/nora/1.png")],
    )
    nora.select(nora.candidates[0])
    stranger = Character(name="Stranger")  # named but never cast

    shot = Shot(scene="a platform at dusk", cast=[nora, stranger])
    # Only cast Characters with a reference contribute a locked keyframe.
    assert shot.locked_references() == ["store/nora/1.png"]
    # The prompt names the cast so a conditioning reference can bind to a name.
    prompt = build_image_prompt(shot)
    assert "Featuring Nora" in prompt and "Stranger" in prompt


def test_character_prompt_composes_look_and_design_brief() -> None:
    # The audition frame reads the Actor's look through the Character's design brief.
    actor = Actor(look="weathered, grey-eyed, close-cropped silver hair")
    nora = Character(
        name="Nora",
        age_band=AgeBand.MIDDLE_AGED,
        build="lean, upright",
        wardrobe="a worn wool coat",
        essence="stubborn tenderness",
    )
    p = build_character_prompt(nora, actor)
    assert "weathered, grey-eyed" in p
    assert "a middle-aged adult" in p  # the age band constrains the look
    assert "worn wool coat" in p
    assert "character reference" in p  # asks for a consistent, lockable look


def test_selecting_an_actor_that_did_not_audition_is_refused() -> None:
    # Casting-as-selection: you choose from the field you auditioned (Ch. 18).
    a1 = Actor(look="weathered")
    a2 = Actor(look="younger")
    nora = Character(name="Nora", candidates=[a1])
    nora.select(a1)
    assert nora.cast is a1
    try:
        nora.select(a2)  # never auditioned
    except ValueError:
        pass
    else:  # pragma: no cover - the assertion is the failure signal
        raise AssertionError("casting a non-auditioning actor should raise")
    assert nora.cast is a1  # the refused verdict left the earlier cast intact


def test_audition_renders_candidates_files_them_and_locks_references() -> None:
    import tempfile

    from sequitur import (
        Director,
        Gate,
        GateStatus,
        ImageStudio,
        LocalFolderOutputStore,
        Medium,
        RenderResult,
        register,
    )

    class FakeStudio:  # a still producer needing no credentials
        medium = Medium.STILL

        def render(self, decision, *, out_path=None):
            Path(out_path).write_bytes(b"candidate-bytes")
            return RenderResult("fake-native", Path(out_path))

    register(Medium.STILL, lambda: FakeStudio())
    try:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            store = LocalFolderOutputStore(root / "store")
            gate = Gate(store, production="HeistNoir")
            nora = Character(
                name="Nora",
                candidates=[Actor(look="weathered"), Actor(look="younger")],
            )
            deliverables = Director().audition(nora, gate=gate, out_dir=root / "scratch")

            # One PENDING deliverable per candidate, each filed durably under the gate.
            assert len(deliverables) == 2
            assert all(dv.status is GateStatus.PENDING for dv in deliverables)
            assert all(Path(dv.ref).read_bytes() == b"candidate-bytes" for dv in deliverables)
            # Each candidate Actor's reference is locked to its durable keyframe.
            assert [a.reference for a in nora.candidates] == [str(dv.ref) for dv in deliverables]
            # Nothing is cast yet — selection is the Producer's separate verdict.
            assert nora.cast is None

            # The Producer's verdict binds one candidate and keeps its locked look.
            nora.select(nora.candidates[0])
            assert nora.cast is nora.candidates[0]
            assert nora.cast.reference == str(deliverables[0].ref)
    finally:
        register(Medium.STILL, ImageStudio)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
