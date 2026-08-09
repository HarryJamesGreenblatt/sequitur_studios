"""Smoke tests for the crew engine — the heuristic behaviour layer.

Asserts against the *public* package surface (``sequitur``). Run directly
(``python tests/test_engine.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Brief,
    CameraAngle,
    CameraMovement,
    Cinematographer,
    Engine,
    HeuristicJudgment,
    LightScheme,
    Phase,
    ShotSize,
    build_prompt,
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


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
