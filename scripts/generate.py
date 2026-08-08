"""Sequitur Studios command-line renderer.

Examples
--------
Free-form prompt:
    python scripts/generate.py "A lighthouse in a storm, waves crashing"

Grammar-driven (Bowen vocabulary):
    python scripts/generate.py "an old fisherman mending nets on a dock" \
        --size mcu --view three-quarter-front --angle low --move dolly-in \
        --scheme low-key --quality soft --color-temp golden-hour \
        --mood "weathered, resolute" --audio "gulls, distant surf, no dialogue"

Dry run (compose and print the prompt, no API call):
    python scripts/generate.py "..." --size cu --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make the `sequitur` package importable when run as a bare script.
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
    build_prompt,
)


def _by_name(enum) -> dict:
    """Map a hyphenated lower-case member name to the enum member."""
    return {m.name.lower().replace("_", "-"): m for m in enum}


SIZES = {s.code.lower(): s for s in ShotSize} | _by_name(ShotSize)
VIEWS = _by_name(SubjectView)
ANGLES = _by_name(CameraAngle)
STYLES = _by_name(ShootingStyle)
COMPS = _by_name(Composition)
FOCALS = _by_name(FocalLength)
DOFS = _by_name(DepthOfField)
MOVES = _by_name(CameraMovement)
SPEEDS = _by_name(MotionSpeed)
QUALITIES = _by_name(LightQuality)
SCHEMES = _by_name(LightScheme)
DIRECTIONS = _by_name(LightDirection)
COLOR_TEMPS = _by_name(ColorTemperature)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render a shot with Sequitur Studios.")
    p.add_argument("scene", help="What happens: subject, action, setting.")
    p.add_argument("--size", choices=sorted(SIZES), help="Shot size (e.g. mcu, cu, ls).")
    p.add_argument("--view", choices=sorted(VIEWS), help="Horizontal angle on the subject.")
    p.add_argument("--angle", choices=sorted(ANGLES), help="Vertical camera angle / canting.")
    p.add_argument("--style", choices=sorted(STYLES), help="objective or subjective (direct address).")
    p.add_argument("--composition", choices=sorted(COMPS), help="Subject placement in frame.")
    p.add_argument("--focal", choices=sorted(FOCALS), help="Lens focal length / perspective.")
    p.add_argument("--dof", choices=sorted(DOFS), help="Depth of field (shallow / deep).")
    p.add_argument("--move", choices=sorted(MOVES), help="Camera movement.")
    p.add_argument("--speed", choices=sorted(SPEEDS), help="Playback speed (slow / fast / time-lapse).")
    p.add_argument("--quality", choices=sorted(QUALITIES), help="Light quality (hard / soft).")
    p.add_argument("--scheme", choices=sorted(SCHEMES), help="Lighting scheme (low-key, three-point, ...).")
    p.add_argument("--direction", choices=sorted(DIRECTIONS), help="Light direction (front, side, back, ...).")
    p.add_argument("--color-temp", choices=sorted(COLOR_TEMPS), help="Colour temperature (warm, cool, ...).")
    p.add_argument("--eye-light", action="store_true", help="Add a catch light in the eyes.")
    p.add_argument("--lens", help="Free-form lens/DoF note.")
    p.add_argument("--mood", help="Emotional tone.")
    p.add_argument("--audio", help="Sound design and music direction.")
    p.add_argument("--timing", help="Timecode direction, e.g. '[0-8s]'.")
    p.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    p.add_argument("--avoid", nargs="*", default=[], help="Things to exclude.")
    p.add_argument("--multi-scene", action="store_true", help="Allow scene cuts.")
    p.add_argument("--image", action="store_true", help="Render a still image (Azure Foundry gpt-image) instead of video.")
    p.add_argument("--out", help="Output file path (.mp4 for video, .png for image).")
    p.add_argument("--dry-run", action="store_true", help="Print the prompt; do not call the API.")
    return p.parse_args(argv)


def shot_from_args(args: argparse.Namespace) -> Shot:
    return Shot(
        scene=args.scene,
        size=SIZES.get(args.size) if args.size else None,
        view=VIEWS.get(args.view) if args.view else None,
        angle=ANGLES.get(args.angle) if args.angle else None,
        style=STYLES.get(args.style) if args.style else None,
        composition=COMPS.get(args.composition) if args.composition else None,
        focal_length=FOCALS.get(args.focal) if args.focal else None,
        depth_of_field=DOFS.get(args.dof) if args.dof else None,
        movement=MOVES.get(args.move) if args.move else None,
        speed=SPEEDS.get(args.speed) if args.speed else None,
        light_quality=QUALITIES.get(args.quality) if args.quality else None,
        light_scheme=SCHEMES.get(args.scheme) if args.scheme else None,
        light_direction=DIRECTIONS.get(args.direction) if args.direction else None,
        color_temp=COLOR_TEMPS.get(args.color_temp) if args.color_temp else None,
        eye_light=args.eye_light,
        lens=args.lens,
        mood=args.mood,
        audio=args.audio,
        timing=args.timing,
        single_scene=not args.multi_scene,
        avoid=args.avoid,
        aspect_ratio=args.aspect,
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    shot = shot_from_args(args)

    from sequitur import build_image_prompt  # noqa: E402

    prompt = build_image_prompt(shot) if args.image else build_prompt(shot)

    print("Prompt:\n" + prompt + "\n")
    if args.dry_run:
        return 0

    if args.image:
        from sequitur import ImageStudio  # imported late so --dry-run needs no deps

        print("Rendering still image...")
        _, path = ImageStudio().render(shot, out_path=args.out)
        print(f"Saved: {path}")
        return 0

    from sequitur import Studio  # imported late so --dry-run needs no API key

    studio = Studio()
    print("Rendering (this can take a while)...")
    _, path = studio.render(shot, out_path=args.out)
    print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
