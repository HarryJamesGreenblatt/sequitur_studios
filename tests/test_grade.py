"""Smoke tests for the colour-grade layer — the Colorist, the reified Grade model,
and the operator plane of the renderer registry (storyline 0022).

Asserts against the *public* package surface (``sequitur``). Constructs only
dependency-free objects; the ffmpeg execution path is never invoked, so this test
needs no ffmpeg binary. Run directly (``python tests/test_grade.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Cast,
    ColorBalance,
    Colorist,
    Contrast,
    Grade,
    Grader,
    Look,
    Operation,
    Saturation,
    TonalRange,
    Transform,
    named_look,
    operator_for,
    register_look,
    register_operator,
    registered_looks,
    registered_operations,
)


def test_colorist_owns_the_grade_vocabulary() -> None:
    assert Colorist.vocabulary == (Look, TonalRange, Cast)
    assert Colorist.phase.value == "assemble"
    assert Colorist.department.value == "color"


def test_look_compiles_to_a_valid_ordered_grade() -> None:
    grade = Colorist().grade(Look.GOLDEN_HOUR, source="clip.mp4")
    assert grade.source == "clip.mp4" and grade.name == "golden_hour"
    assert grade.ops and not grade.is_identity
    # Contrast-first, colour-second ordering must lint clean (Ch. 3-4).
    assert grade.validate() == []


def test_grade_validate_flags_bad_params_and_order() -> None:
    bad = Grade(ops=[Contrast(gamma=0.0), Saturation(-1.0)])
    errs = bad.validate()
    assert any("gamma" in e for e in errs) and any("saturation" in e for e in errs)

    out_of_order = Grade(ops=[ColorBalance(TonalRange.SHADOWS, b=0.2), Contrast(gain=1.1)])
    assert any(w.startswith("warning") and "contrast first" in w for w in out_of_order.validate())


def test_grade_round_trips_through_a_plain_dict() -> None:
    grade = Colorist().grade(Look.TEAL_ORANGE, source="s.mp4")
    restored = Grade.from_dict(grade.to_dict())
    assert restored.to_dict() == grade.to_dict()
    assert restored.ops == grade.ops  # reified ops survive serialisation


def test_filtergraph_compiles_the_stack_to_ffmpeg_filters() -> None:
    grade = Grade(
        ops=[
            Contrast(lift=0.02, gamma=0.9, gain=1.1),
            ColorBalance(TonalRange.HIGHLIGHTS, r=0.15, b=-0.06),
            Saturation(1.2),
        ]
    )
    graph = Grader.filtergraph(grade)
    assert "eq=brightness=0.02:gamma=0.9:contrast=1.1" in graph
    assert "colorbalance=rh=0.15:bh=-0.06" in graph
    assert "eq=saturation=1.2" in graph
    assert Grader.filtergraph(Grade()) == ""  # an identity grade compiles to nothing


def test_operator_plane_registers_the_grader() -> None:
    assert Operation.GRADE in registered_operations()
    grader = operator_for(Operation.GRADE)
    assert isinstance(grader, Grader)
    assert isinstance(grader, Transform)  # runtime_checkable structural match
    assert grader.operation is Operation.GRADE


def test_operator_registry_is_overridable() -> None:
    sentinel = object()
    register_operator(Operation.GRADE, lambda: sentinel)
    try:
        assert operator_for(Operation.GRADE) is sentinel
    finally:
        register_operator(Operation.GRADE, Grader)  # restore the default factory


def test_production_can_register_and_resolve_its_own_look() -> None:
    template = (
        Grade(name="cyberpunk")
        .add(Contrast(gamma=0.9, gain=1.15))
        .add(ColorBalance(TonalRange.SHADOWS, b=0.2, g=0.05))
        .add(Saturation(1.2))
    )
    register_look("cyberpunk", template)
    assert "cyberpunk" in registered_looks()

    # The Colorist resolves a registered name to a fresh Grade bound to the source.
    out = Colorist().grade("cyberpunk", source="clip.mp4")
    assert out.source == "clip.mp4" and out.name == "cyberpunk"
    assert out.ops == template.ops and out.validate() == []

    # Resolution is a copy: the stored template is never mutated by a caller.
    assert out is not template and out.ops is not template.ops
    assert template.source is None

    # Direct resolution mirrors the Colorist path.
    assert named_look("cyberpunk").ops == template.ops


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
