"""The grip department — the **Key Grip** (Grip · Dolly Grip).

Owns the grammar of camera *movement* and playback *speed* (Grammar of the Shot
Ch. 6) — two distinct temporal axes: how the camera travels through the shot, and
whether time itself is stretched or compressed. These are the video-only faces of
the grammar; a still has neither.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from .role import Department, Phase, Role

if TYPE_CHECKING:
    from .role import Brief


class CameraMovement(Enum):
    """How the camera moves during the shot."""

    STATIC = ("locked-off static frame, no camera movement", "stillness, composure, observation")
    PAN = ("smooth horizontal pan", "reveals space or follows lateral action")
    TILT = ("vertical tilt", "reveals height or shifts attention up/down")
    DOLLY_IN = ("slow dolly in toward the subject", "growing intimacy or tension")
    DOLLY_OUT = ("slow dolly out away from the subject", "isolation, reveal, release")
    TRUCK = ("lateral tracking / trucking move alongside the subject", "travels with motion, keeps pace")
    PEDESTAL = ("vertical pedestal move", "rises or lowers the whole camera through space")
    ZOOM = ("optical zoom", "compresses space; more artificial than a dolly")
    CRANE = ("sweeping crane / jib move", "grand scale, lyrical reveals")
    HANDHELD = ("handheld camera with organic micro-movement", "immediacy, documentary energy, unease")
    STEADICAM = ("fluid gliding Steadicam move", "smooth immersive travel through a space")
    ARC = ("arcing move orbiting around the subject", "dimensionality, heightened drama")
    GIMBAL = ("smooth stabilized gimbal move", "fluid, handheld-free travel that follows action anywhere")
    DRONE = ("aerial drone move", "epic vistas and sweeping tracking from the air")
    WHIP_PAN = ("fast whip-pan", "a blurred, kinetic transition between spaces")
    PAN_TILT = ("combined diagonal pan-and-tilt", "sweeps across and up or down, revealing in one move")
    DOLLY_ZOOM = ("dolly-zoom counter-move", "the 'vertigo' effect; an unsettling warp of perspective")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class MotionSpeed(Enum):
    """Playback speed — a temporal axis, distinct from camera movement."""

    SLOW_MOTION = ("in slow motion", "dramatic, weighty, lyrical; overcranked capture")
    FAST_MOTION = ("in fast motion", "condensed, comedic, or urgent; undercranked capture")
    TIME_LAPSE = ("as a time-lapse", "long spans compressed — clouds, crowds, shifting light")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class KeyGrip(Role):
    """The grip department head — owns camera movement and playback speed."""

    title = "Key Grip"
    department = Department.GRIP
    phase = Phase.SHOOT
    vocabulary = (CameraMovement, MotionSpeed)

    def heuristic(self, brief: Brief) -> dict[str, Any]:
        h = brief.hints
        return {
            "movement": h.get("movement", CameraMovement.STATIC),
            "speed": h.get("speed"),
        }
