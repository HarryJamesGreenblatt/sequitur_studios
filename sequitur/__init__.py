"""Sequitur Studios — a film studio grounded in the grammar of the shot.

Public surface:
    Studio                          the video render/edit client (Gemini Omni Flash)
    ImageStudio                     the still-image client (Azure Foundry gpt-image)
    Shot                            a structured shot specification
    build_prompt                    turn a Shot into a well-formed video prompt
    build_image_prompt              turn a Shot into a still-image prompt
    ShotSize, CameraAngle,
    SubjectView, ShootingStyle,
    Composition, FocalLength,
    DepthOfField, CameraMovement,
    MotionSpeed, LightQuality,
    LightScheme, LightDirection,
    ColorTemperature                the grammar vocabulary (orthogonal layers)
    Transition, EditReason,
    EditCategory                    the grammar of the edit (post layer)
    Clip, Edit, Beat, Scene,
    Act, Sequence, TimelineEntry    the shots -> scenes -> acts assembly model
    Cutter                          executes an edit Sequence into a film (MoviePy)
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
from .image import ImageStudio
from .edit import (
    Act,
    Beat,
    Clip,
    Edit,
    EditCategory,
    EditReason,
    Scene,
    Sequence,
    TimelineEntry,
    Transition,
)
from .cutter import Cutter
from .prompt import build_image_prompt, build_prompt
from .studio import Studio

__all__ = [
    "Studio",
    "ImageStudio",
    "Shot",
    "build_prompt",
    "build_image_prompt",
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
    "Transition",
    "EditReason",
    "EditCategory",
    "Clip",
    "Edit",
    "Beat",
    "Scene",
    "Act",
    "Sequence",
    "TimelineEntry",
    "Cutter",
]
