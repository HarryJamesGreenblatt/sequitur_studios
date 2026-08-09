"""The electric department — the **Gaffer** (Electric · Lighting Tech).

Owns the grammar of *lighting* (Grammar of the Shot Ch. 4), split into its
orthogonal axes: scheme and contrast, hardness, direction, and colour
temperature — plus the eye catch light. The lighting shapes mood and dimension
independently of what the camera frames.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from .role import Department, Phase, Role

if TYPE_CHECKING:
    from .role import Brief


class LightQuality(Enum):
    """The hardness of the light — the edge quality of its shadows."""

    HARD = ("hard, directional light with crisp-edged shadows", "tension, drama, sculpted 'pop'")
    SOFT = ("soft, diffused light that wraps the subject", "flattering, gentle, natural")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class LightScheme(Enum):
    """The overall lighting approach and contrast."""

    HIGH_KEY = ("high-key lighting, bright and low-contrast", "cheerful, clean, even; commercial and TV")
    LOW_KEY = ("low-key lighting with deep shadows and strong contrast", "noir, suspense, moody, dimensional")
    THREE_POINT = ("classic three-point lighting (key, fill, back)", "balanced, professional standard")
    NATURAL = ("naturalistic motivated lighting from practical sources", "realism, documentary honesty")
    SILHOUETTE = ("backlit silhouette against a bright background", "mystery, graphic drama")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class LightDirection(Enum):
    """Where the key light comes from — the angle of incidence."""

    FRONT = ("lit from the front", "even and flat; hides texture, minimizes the nose")
    SIDE = ("lit from the side", "splits the face bright and dark; mystery, duality")
    BACK = ("backlit and rim-lit from behind", "separates the subject from the background, halos the edge")
    TOP = ("lit from above", "eyes fall into shadow; distrust, 'butterfly' nose shadow")
    UNDER = ("lit from below", "unnatural and ghoulish; horror, or screen-glow")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class ColorTemperature(Enum):
    """The colour of the light, on the warm-to-cool axis."""

    WARM = ("warm amber light (tungsten, ~3200K)", "firelight and interiors; cozy, advancing")
    NEUTRAL = ("neutral, colour-balanced light", "true-to-life colour")
    COOL = ("cool blue light (daylight, ~5600K)", "moonlight and overcast; calm, receding")
    MIXED = ("mixed warm and cool light (warm practicals, cool moonlight)", "layered, filmic colour contrast")
    GOLDEN_HOUR = ("warm golden-hour light with long, soft shadows", "nostalgia, warmth, romance")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Gaffer(Role):
    """The electric department head — owns the lighting grammar.

    Also wields the ``eye_light`` catch-light flag on a :class:`~sequitur.shot.Shot`
    (a boolean, not an enum, so it is not part of :attr:`vocabulary`).
    """

    title = "Gaffer"
    department = Department.ELECTRIC
    phase = Phase.SHOOT
    vocabulary = (LightScheme, LightQuality, LightDirection, ColorTemperature)

    def heuristic(self, brief: Brief) -> dict[str, Any]:
        h = brief.hints
        return {
            "light_scheme": h.get("light_scheme", LightScheme.THREE_POINT),
            "light_quality": h.get("light_quality", LightQuality.SOFT),
            "light_direction": h.get("light_direction"),
            "color_temp": h.get("color_temp", ColorTemperature.NEUTRAL),
            "eye_light": h.get("eye_light", False),
        }
