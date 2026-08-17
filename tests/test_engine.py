"""Smoke tests for the crew engine — the heuristic behaviour layer.

Asserts against the *public* package surface (``sequitur``). Run directly
(``python tests/test_engine.py``) or via pytest.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Brief,
    CameraAngle,
    CameraMovement,
    Cinematographer,
    ConceptStance,
    Director,
    Engine,
    HeuristicJudgment,
    ImageStudio,
    LightScheme,
    LocalFolderOutputStore,
    Look,
    Medium,
    MediumLook,
    Phase,
    Plan,
    RenderResult,
    Shot,
    ShotSize,
    Supergenre,
    Transition,
    build_prompt,
    register,
    shoot_crew,
)


def test_engine_assembles_a_default_shot() -> None:
    shot = Engine().run(Phase.SHOOT, Brief(scene="a fox crossing a frozen field"))
    # Each department contributed its default slice of the shot.
    assert shot.scene == "a fox crossing a frozen field"
    assert shot.size is ShotSize.MEDIUM  # Cinematographer default
    assert shot.angle is CameraAngle.EYE_LEVEL  # Cinematographer default
    assert shot.light_scheme is LightScheme.THREE_POINT  # Gaffer default
    assert shot.movement is CameraMovement.STATIC  # Key Grip default
    # The assembled shot renders through the existing prompt builder.
    assert "medium shot" in build_prompt(shot)


def test_producer_hints_override_role_defaults() -> None:
    brief = Brief(
        scene="a lone astronaut",
        hints={"size": ShotSize.CLOSE_UP, "movement": CameraMovement.DOLLY_OUT},
        mood="awe, isolation",
    )
    shot = Engine().run(Phase.SHOOT, brief)
    assert shot.size is ShotSize.CLOSE_UP
    assert shot.movement is CameraMovement.DOLLY_OUT
    assert shot.mood == "awe, isolation"  # passes straight through the Director


def test_departments_contribute_disjoint_slices() -> None:
    brief = Brief(scene="x")
    fields = {
        c.role: set(k for k, v in c.fields.items() if v is not None)
        for role in shoot_crew()
        for c in [role.propose(brief)]
    }
    # The Cinematographer owns framing, never lighting or movement.
    assert "size" in fields["Cinematographer"]
    assert "light_scheme" not in fields["Cinematographer"]
    assert "movement" not in fields["Cinematographer"]


def test_judgment_is_swappable() -> None:
    class SilentJudgment(HeuristicJudgment):
        def decide(self, role, brief):
            c = super().decide(role, brief)
            c.fields.clear()  # a judgment that proposes nothing
            return c

    dp = Cinematographer(judgment=SilentJudgment())
    assert dp.propose(Brief(scene="x")).fields == {}


def test_engine_reconciles_a_plan() -> None:
    plan = Engine().plan(Brief(scene="a fox crossing a frozen field", mood="still, cold"))
    assert isinstance(plan, Plan)
    assert plan.scene == "a fox crossing a frozen field"
    assert plan.mood == "still, cold"
    # The Screenwriter's story descriptor and the Production Designer's design
    # descriptor land in disjoint halves of the plan.
    assert plan.story["supergenre"] is Supergenre.LIFE  # Screenwriter default
    assert plan.design["medium_look"] is MediumLook.DIGITAL  # Production Designer default
    # The halves stay disjoint — a story key never leaks into the design descriptor.
    assert "visual_concept" in plan.design and "supergenre" not in plan.design


def test_plan_hints_route_to_the_right_half() -> None:
    brief = Brief(
        scene="a heist in a rain-soaked city",
        hints={
            "supergenre": Supergenre.CRIME,
            "visual_concept": "the city as a rain-streaked maze",
            "concept_stance": ConceptStance.CONTRAST,
        },
    )
    plan = Engine().plan(brief)
    assert plan.story["supergenre"] is Supergenre.CRIME
    assert plan.design["visual_concept"] == "the city as a rain-streaked maze"
    assert plan.design["concept_stance"] is ConceptStance.CONTRAST


def test_engine_assembles_a_graded_sequence() -> None:
    brief = Brief(
        scene="",
        shots=[Shot(scene="a"), Shot(scene="b"), Shot(scene="c")],
        hints={"look": Look.TEAL_ORANGE},
    )
    seq = Engine().assemble(brief)
    tl = seq.timeline()
    assert len(tl) == 3
    # Editor: opens on a fade in, then straight cuts.
    assert tl[0].edit_in.transition is Transition.FADE_IN
    assert all(e.edit_in.transition is Transition.CUT for e in tl[1:])
    # Colorist: every clip carries the base grade (the sequence's look).
    assert all(e.clip.grade is not None and e.clip.grade.name == "teal_orange" for e in tl)
    # The grade is a copy per clip, not a shared instance.
    assert tl[0].clip.grade is not tl[1].clip.grade


def test_director_execute_hook_renders_a_greenlit_shot() -> None:
    captured: dict = {}

    class FakeStudio:
        medium = Medium.STILL

        def render(self, shot, *, out_path=None):
            captured["shot"] = shot
            captured["out_path"] = out_path
            return RenderResult("fake-native", "out.png")

    register(Medium.STILL, lambda: FakeStudio())  # a producer needing no credentials
    try:
        shot = Engine().run(Phase.SHOOT, Brief(scene="a lighthouse in a storm"))
        result = Director().execute(shot, medium=Medium.STILL, out_path="out.png")
        # The greenlit Shot flowed decision -> execution untouched.
        assert captured["shot"] is shot
        assert captured["out_path"] == "out.png"
        assert result.ref == "out.png"
    finally:
        register(Medium.STILL, ImageStudio)  # restore the default factory


def test_execute_files_the_render_into_the_output_store() -> None:
    class FakeStudio:
        medium = Medium.STILL

        def render(self, shot, *, out_path=None):
            Path(out_path).write_bytes(b"daily-bytes")
            return RenderResult("fake-native", Path(out_path))

    register(Medium.STILL, lambda: FakeStudio())
    try:
        with tempfile.TemporaryDirectory() as d:
            scratch = Path(d) / "scratch.png"
            store = LocalFolderOutputStore(Path(d) / "store")
            shot = Engine().run(Phase.SHOOT, Brief(scene="a lighthouse in a storm"))
            result = Director().execute(
                shot,
                medium=Medium.STILL,
                out_path=scratch,
                store=store,
                production="HeistNoir",
                phase="shoot",
                name="shot_001.png",
            )
            # The ref is now the DURABLE store location, and the bytes made it there.
            assert Path(result.ref) == Path(d) / "store" / "HeistNoir" / "shoot" / "shot_001.png"
            assert Path(result.ref).read_bytes() == b"daily-bytes"
    finally:
        register(Medium.STILL, ImageStudio)


def test_execute_with_a_store_requires_a_production() -> None:
    class FakeStudio:
        medium = Medium.STILL

        def render(self, shot, *, out_path=None):
            Path(out_path).write_bytes(b"x")
            return RenderResult("fake-native", Path(out_path))

    register(Medium.STILL, lambda: FakeStudio())
    try:
        with tempfile.TemporaryDirectory() as d:
            store = LocalFolderOutputStore(d)
            shot = Engine().run(Phase.SHOOT, Brief(scene="a"))
            try:
                Director().execute(
                    shot, medium=Medium.STILL, out_path=Path(d) / "s.png", store=store
                )
            except ValueError:
                pass
            else:  # pragma: no cover - the assertion is the failure signal
                raise AssertionError("a store without a production should raise")
    finally:
        register(Medium.STILL, ImageStudio)


def test_execute_forwards_cast_references_to_the_renderer() -> None:
    seen: dict = {}

    class FakeStudio:  # a still backend that accepts conditioning references
        medium = Medium.STILL

        def render(self, shot, *, out_path=None, references=None):
            Path(out_path).write_bytes(b"conditioned")
            seen["references"] = references
            return RenderResult("fake-native", Path(out_path))

    register(Medium.STILL, lambda: FakeStudio())
    try:
        with tempfile.TemporaryDirectory() as d:
            shot = Engine().run(Phase.SHOOT, Brief(scene="Nora on the platform"))
            # The locked cast reference threads through to the backend (storyline 0055).
            Director().execute(
                shot,
                medium=Medium.STILL,
                out_path=Path(d) / "s.png",
                references=["store/Nora/plan/Nora-candidate-1.png"],
            )
            assert seen["references"] == ["store/Nora/plan/Nora-candidate-1.png"]
    finally:
        register(Medium.STILL, ImageStudio)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
