"""Compose a :class:`~sequitur.grammar.Shot` into a well-formed model prompt.

Follows the Gemini Omni Flash prompt guidance: lead with the scene, layer
camera and lighting language, describe sound design explicitly, enforce a
single continuous shot when asked, and fold negatives inline (the model does
not accept a separate negative-prompt field).
"""

from __future__ import annotations

from .grammar import Shot


def build_prompt(shot: Shot) -> str:
    parts: list[str] = []

    if shot.timing:
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

    # Camera: angle, movement, speed, and lens / focus.
    camera = [
        f.phrase
        for f in (
            shot.angle,
            shot.movement,
            shot.speed,
            shot.focal_length,
            shot.depth_of_field,
        )
        if f
    ]
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

    # Omni Flash generates and syncs its own audio; be explicit to control it.
    if shot.audio:
        parts.append("Sound design: " + shot.audio.rstrip(".") + ".")

    if shot.single_scene:
        parts.append("A single continuous shot, no scene cuts.")

    if shot.avoid:
        parts.append("Do not include: " + ", ".join(shot.avoid) + ".")

    return " ".join(parts)
