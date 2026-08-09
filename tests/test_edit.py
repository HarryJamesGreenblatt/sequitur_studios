"""Smoke tests for the editorial model — guards the Editor's assembly logic.

Asserts against the *public* package surface (``sequitur``) so it survives
internal moves (e.g. re-seating the edit vocabulary under the Editor role).
Run directly (``python tests/test_edit.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Act,
    EditCategory,
    EditReason,
    Editor,
    Scene,
    Sequence,
    Shot,
    Transition,
)


def _seq(scene: Scene) -> Sequence:
    return Sequence(acts=[Act(scenes=[scene])])


def test_editor_owns_the_cut_vocabulary() -> None:
    assert Editor.vocabulary == (Transition, EditReason, EditCategory)
    assert Transition.DISSOLVE.needs_handles and not Transition.CUT.needs_handles


def test_timeline_overlaps_only_handle_transitions() -> None:
    scene = Scene()
    scene.add(Shot(scene="a"), duration=4.0)
    scene.add(
        Shot(scene="b"),
        transition=Transition.DISSOLVE,
        transition_duration=2.0,
        duration=4.0,
        head_handle=1.0,
    )
    tl = _seq(scene).timeline()
    # The dissolve pulls clip b's start back by the transition duration.
    assert tl[0].start == 0.0 and tl[0].end == 4.0
    assert tl[1].start == 2.0 and tl[1].end == 6.0


def test_validate_flags_missing_handles_and_reasonless_cut() -> None:
    scene = Scene()
    scene.add(Shot(scene="a"), duration=4.0)  # no tail_handle
    scene.add(Shot(scene="b"), transition=Transition.DISSOLVE, transition_duration=2.0)
    scene.add(Shot(scene="c"))  # a cut with no reason
    issues = _seq(scene).validate()
    assert any("tail handle" in i for i in issues)
    assert any("head handle" in i for i in issues)
    assert any("no reason" in i for i in issues)


def test_clean_cut_with_reason_is_silent() -> None:
    scene = Scene()
    scene.add(Shot(scene="a"))
    scene.add(Shot(scene="b"), reason=EditReason.INFORMATION)
    assert _seq(scene).validate() == []


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
