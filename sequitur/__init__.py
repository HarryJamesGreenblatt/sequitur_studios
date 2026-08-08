"""Sequitur Studios — a film studio grounded in the grammar of the shot.

Public surface:
    Studio                          the render/edit client (Gemini Omni Flash)
    Shot                            a structured shot specification
    build_prompt                    turn a Shot into a well-formed prompt
    ShotSize, CameraAngle,
    SubjectView, ShootingStyle,
    Composition, FocalLength,
    DepthOfField, CameraMovement,
    MotionSpeed, LightQuality,
    LightScheme, LightDirection,
    ColorTemperature                the grammar vocabulary (orthogonal layers)
"""

from .grammar import (
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
)
from .prompt import build_prompt
from .studio import Studio

__all__ = [
    "Studio",
    "Shot",
    "build_prompt",
    "ShotSize",
    "CameraAngle",
    "SubjectView",
    "ShootingStyle",
    "Composition",
    "FocalLength",
    "DepthOfField",
    "CameraMovement",
    "MotionSpeed",
    "LightQuality",
    "LightScheme",
    "LightDirection",
    "ColorTemperature",
]
