"""Sequitur Studios — a film studio grounded in the grammar of the shot.

Public surface:
    Studio                          the video render/edit client (Gemini Omni Flash)
    ImageStudio                     the still-image client (Azure Foundry gpt-image)
    SpeechRenderer                  the text-to-speech client (Azure AI Speech)
    Shot                            a structured shot specification
    build_prompt                    turn a Shot into a well-formed video prompt
    build_image_prompt              turn a Shot into a still-image prompt
    ShotSize, CameraAngle,
    SubjectView, ShootingStyle,
    Composition, FocalLength,
    DepthOfField, CameraMovement,
    MotionSpeed, LightQuality,
    LightScheme, LightDirection,
    ColorTemperature                the grammar vocabulary (owned by crew roles)
    Role, Department, Phase         the crew seat and the axes that place a role
    Cinematographer, Gaffer,
    KeyGrip, Editor                 the roles that own the shot / edit vocabulary
    Brief, Contribution             a role's decision context and its proposed slice
    Judgment, HeuristicJudgment     the swappable reasoning strategy (heuristic A)
    Director, Engine, shoot_crew    reconcile the crew · dispatch a phase · default crew
    Transition, EditReason,
    EditCategory                    the grammar of the edit (owned by the Editor)
    Clip, Edit, Beat, Scene,
    Act, Sequence, TimelineEntry    the shots -> scenes -> acts assembly model
    Cutter                          executes an edit Sequence into a film (MoviePy)
"""

from .crew import (
    Brief,
    Contribution,
    Department,
    Director,
    Engine,
    HeuristicJudgment,
    Judgment,
    Phase,
    Role,
    shoot_crew,
)
from .crew.camera import (
    CameraAngle,
    Cinematographer,
    Composition,
    DepthOfField,
    FocalLength,
    ShootingStyle,
    ShotSize,
    SubjectView,
)
from .crew.editorial import EditCategory, EditReason, Editor, Transition
from .crew.grip import CameraMovement, KeyGrip, MotionSpeed
from .crew.lighting import (
    ColorTemperature,
    Gaffer,
    LightDirection,
    LightQuality,
    LightScheme,
)
from .image import ImageStudio
from .shot import Shot
from .edit import (
    Act,
    Beat,
    Clip,
    Edit,
    Scene,
    Sequence,
    TimelineEntry,
)
from .cutter import Cutter
from .prompt import build_image_prompt, build_prompt
from .speech import SpeechRenderer
from .studio import Studio

__all__ = [
    "Studio",
    "ImageStudio",
    "SpeechRenderer",
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
    "Role",
    "Department",
    "Phase",
    "Cinematographer",
    "Gaffer",
    "KeyGrip",
    "Editor",
    "Brief",
    "Contribution",
    "Judgment",
    "HeuristicJudgment",
    "Director",
    "Engine",
    "shoot_crew",
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
