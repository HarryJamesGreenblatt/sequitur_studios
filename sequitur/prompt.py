"""Compose a :class:`~sequitur.shot.Shot` into a well-formed model prompt.

Two renderers, two builders sharing one grammar:

- :func:`build_prompt` targets Gemini Omni Flash **video** — lead with the
  scene, layer camera and lighting language, describe sound design explicitly,
  enforce a single continuous shot when asked, fold negatives inline.
- :func:`build_image_prompt` targets a **still-image** backend (Azure Foundry
  ``gpt-image``) — the same framing, camera, and lighting grammar, minus the
  moving parts (movement, speed, audio, scene continuity).
"""

from __future__ import annotations

from .shot import Shot


def _compose(shot: Shot, *, moving: bool) -> str:
    parts: list[str] = []

    if shot.timing and moving:
        parts.append(shot.timing)

    # Core scene, optionally prefixed with the shot size for framing.
    if shot.size:
        parts.append(f"A {shot.size.phrase} of {shot.scene.rstrip('.')}.")
    else:
        parts.append(shot.scene.rstrip(".") + ".")

    # How the subject sits in the frame.
    framing = [f.phrase for f in (shot.view, shot.style, shot.composition) if f]
    if framing:
        parts.append("Framing: " + ", ".join(framing) + ".")

    # Camera: angle, lens / focus, and (video only) movement and speed.
    camera_fields = [shot.angle]
    if moving:
        camera_fields += [shot.movement, shot.speed]
    camera_fields += [shot.focal_length, shot.depth_of_field]
    camera = [f.phrase for f in camera_fields if f]
    if shot.lens:
        camera.append(shot.lens)
    if camera:
        parts.append("Camera: " + ", ".join(camera) + ".")

    # Lighting, composed from its orthogonal axes.
    light = [
        f.phrase
        for f in (
            shot.light_scheme,
            shot.light_quality,
            shot.light_direction,
            shot.color_temp,
        )
        if f
    ]
    if shot.eye_light:
        light.append("a catch light glinting in the eyes")
    if light:
        parts.append("Lighting: " + ", ".join(light) + ".")

    if shot.mood:
        parts.append("Mood: " + shot.mood.rstrip(".") + ".")

    if moving:
        # Omni Flash generates and syncs its own audio; be explicit to control it.
        if shot.audio:
            parts.append("Sound design: " + shot.audio.rstrip(".") + ".")
        if shot.single_scene:
            parts.append("A single continuous shot, no scene cuts.")

    if shot.avoid:
        parts.append("Do not include: " + ", ".join(shot.avoid) + ".")

    return " ".join(parts)


def build_prompt(shot: Shot) -> str:
    """Compose a Shot into a Gemini Omni Flash video prompt."""
    return _compose(shot, moving=True)


def build_image_prompt(shot: Shot) -> str:
    """Compose a Shot into a still-image prompt (framing/camera/lighting only)."""
    return _compose(shot, moving=False)
