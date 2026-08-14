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
    KeyGrip, Editor, Colorist       the roles that own the shot / edit / grade vocabulary
    Look, TonalRange, Cast          the grade vocabulary (owned by the Colorist)
    Brief, Contribution             a role's decision context and its proposed slice
    Judgment, HeuristicJudgment     the swappable reasoning strategy (heuristic A)
    Director, Engine, shoot_crew    reconcile the crew · dispatch a phase · default crew
    assemble_crew, full_crew        the post crew (Editor+Colorist) · the whole crew
    Transition, EditReason,
    EditCategory                    the grammar of the edit (owned by the Editor)
    Clip, Edit, Beat, Scene,
    Act, Sequence, TimelineEntry    the shots -> scenes -> acts assembly model
    Grade, GradeOp, Contrast,
    ColorBalance, Saturation        the reified grade decision model (a Command stack)
    register_look, named_look,
    registered_looks                a production's own named looks (Grade templates)
    Cutter                          executes an edit Sequence into a film (MoviePy)
    Grader                          executes a Grade over a rendered clip (ffmpeg)
    ProductionProvider              the production seam (board tree <-> Brief / Sequence)
    AzureDevOpsProduction,
    LocalFolderProduction           the live board backend · the local test double
    Renderer, Medium, RenderResult  the producer seam (decision -> new media artifact)
    Transform, Operation            the operator seam (artifact + decision -> same medium)
    renderer_for, register,
    registered_media                the medium-keyed producer registry
    operator_for, register_operator,
    registered_operations           the operation-keyed transform registry
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
    assemble_crew,
    full_crew,
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
from .crew.colorist import Cast, Colorist, Look, TonalRange
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
from .grade import ColorBalance, Contrast, Grade, GradeOp, Saturation, named_look, register_look, registered_looks
from .cutter import Cutter
from .grader import Grader
from .production import (
    AzureDevOpsProduction,
    LocalFolderProduction,
    ProductionProvider,
)
from .prompt import build_image_prompt, build_prompt
from .render import (
    Medium,
    Operation,
    RenderResult,
    Renderer,
    Transform,
    operator_for,
    register,
    register_operator,
    registered_media,
    registered_operations,
    renderer_for,
)
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
    "Colorist",
    "Look",
    "TonalRange",
    "Cast",
    "Brief",
    "Contribution",
    "Judgment",
    "HeuristicJudgment",
    "Director",
    "Engine",
    "shoot_crew",
    "assemble_crew",
    "full_crew",
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
    "Grade",
    "GradeOp",
    "Contrast",
    "ColorBalance",
    "Saturation",
    "register_look",
    "named_look",
    "registered_looks",
    "Cutter",
    "Grader",
    "ProductionProvider",
    "AzureDevOpsProduction",
    "LocalFolderProduction",
    "Renderer",
    "Transform",
    "Medium",
    "Operation",
    "RenderResult",
    "renderer_for",
    "operator_for",
    "register",
    "register_operator",
    "registered_media",
    "registered_operations",
]
