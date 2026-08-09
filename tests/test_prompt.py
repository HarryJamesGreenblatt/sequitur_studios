"""Smoke tests for the prompt builders — a behavior guard for the grammar.

These assert against the *public* package surface (``sequitur``), so they keep
passing across internal module moves (e.g. re-seating the grammar under crew
roles). Run directly (``python tests/test_prompt.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    CameraAngle,
    CameraMovement,
    ColorTemperature,
    Composition,
    DepthOfField,
    FocalLength,
    LightDirection,
    LightQuality,
    LightScheme,
    MotionSpeed,
    Shot,
    ShootingStyle,
    ShotSize,
    SubjectView,
    build_image_prompt,
    build_prompt,
)


def _full_shot() -> Shot:
    """A shot exercising every grammar layer."""
    return Shot(
        scene="an old fisherman mending nets on a dock",
        size=ShotSize.MEDIUM_CLOSE_UP,
        view=SubjectView.THREE_QUARTER_FRONT,
        angle=CameraAngle.LOW,
        style=ShootingStyle.OBJECTIVE,
        composition=Composition.RULE_OF_THIRDS,
        focal_length=FocalLength.LONG,
        depth_of_field=DepthOfField.SHALLOW,
        lens="35mm anamorphic",
        light_scheme=LightScheme.LOW_KEY,
        light_quality=LightQuality.HARD,
        light_direction=LightDirection.SIDE,
        color_temp=ColorTemperature.GOLDEN_HOUR,
        eye_light=True,
        movement=CameraMovement.DOLLY_IN,
        speed=MotionSpeed.SLOW_MOTION,
        mood="weathered, resolute",
        audio="gulls, distant surf, no dialogue",
        timing="[0-8s]",
        avoid=["text", "watermark"],
    )


def test_video_prompt_includes_every_layer() -> None:
    p = build_prompt(_full_shot())
    assert p.startswith("[0-8s] A medium close-up of an old fisherman")
    for fragment in (
        "Framing:",
        "Camera:",
        "slow dolly in toward the subject",  # movement (video only)
        "in slow motion",                    # speed (video only)
        "Lighting:",
        "a catch light glinting in the eyes",
        "Mood: weathered, resolute.",
        "Sound design: gulls, distant surf, no dialogue.",
        "A single continuous shot, no scene cuts.",
        "Do not include: text, watermark.",
    ):
        assert fragment in p, f"missing {fragment!r}"


def test_image_prompt_drops_the_moving_parts() -> None:
    p = build_image_prompt(_full_shot())
    # Shares framing/camera/lighting grammar...
    assert "Framing:" in p and "Camera:" in p and "Lighting:" in p
    # ...but never the video-only faces: movement, speed, audio, timing, cut note.
    for absent in (
        "[0-8s]",
        "slow dolly in toward the subject",
        "in slow motion",
        "Sound design:",
        "A single continuous shot",
    ):
        assert absent not in p, f"unexpected {absent!r}"


def test_size_code_and_minimal_shot() -> None:
    assert ShotSize.MEDIUM_CLOSE_UP.code == "MCU"
    # A bare video shot still declares its single continuous take (single_scene default).
    bare = build_prompt(Shot(scene="a lighthouse in a storm"))
    assert bare == "a lighthouse in a storm. A single continuous shot, no scene cuts."
    assert build_image_prompt(Shot(scene="a lighthouse in a storm")) == "a lighthouse in a storm."


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
