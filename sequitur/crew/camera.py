"""The camera department — the **Cinematographer** (DP · Camera Operator · AC).

Owns the grammar of *framing* (how much of the subject fills the frame, and the
angles on it — Grammar of the Shot Ch. 1–2) and *lens & focus* (perspective and
depth — Ch. 3). This role composes the visible geometry of the shot; it wields
the video/still renderers to realise it.
"""

from __future__ import annotations

from enum import Enum

from .role import Department, Phase, Role


class ShotSize(Enum):
    """How much of the subject fills the frame, measured against the human figure."""

    EXTREME_LONG = ("extreme long shot", "ELS", "subject tiny in a vast space; establishes geography and scale")
    VERY_LONG = ("very long shot", "VLS", "full figure small in a prominent environment; the rung between extreme long and long")
    LONG = ("long shot", "LS", "full figure head-to-toe with surrounding context; classic establishing size")
    MEDIUM_LONG = ("medium long shot", "MLS", "framed roughly knees-up; the American / cowboy shot")
    MEDIUM = ("medium shot", "MS", "waist-up; the conversational workhorse")
    MEDIUM_CLOSE_UP = ("medium close-up", "MCU", "mid-chest up; intimate but still shows shoulders and gesture")
    CLOSE_UP = ("close-up", "CU", "head and shoulders; reads emotion on the face")
    BIG_CLOSE_UP = ("big close-up", "BCU", "the whole face fills the frame; heightened intensity")
    EXTREME_CLOSE_UP = ("extreme close-up", "ECU", "an isolated detail — the eyes, hands, an object")

    def __init__(self, phrase: str, code: str, intent: str) -> None:
        self.phrase = phrase
        self.code = code
        self.intent = intent


class CameraAngle(Enum):
    """Vertical relationship between lens and subject — shapes power and mood."""

    EYE_LEVEL = ("shot at eye level", "neutral, natural, equal footing with the subject")
    HIGH = ("high angle looking down on the subject", "makes the subject smaller, vulnerable, or observed")
    LOW = ("low angle looking up at the subject", "makes the subject dominant, heroic, or threatening")
    OVERHEAD = ("overhead bird's-eye angle straight down", "abstract, god's-eye, maps the geography of action")
    WORMS_EYE = ("extreme worm's-eye angle from the ground", "monumental, disorienting scale")
    DUTCH = ("canted Dutch angle with a tilted horizon", "unease, tension, a world knocked off balance")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class SubjectView(Enum):
    """Horizontal angle on the subject — orthogonal to the vertical CameraAngle."""

    FRONTAL = ("framed from the front", "full face and both eyes; factual but can feel flat")
    THREE_QUARTER_FRONT = ("framed from a three-quarter front angle", "the fiction default; dimensional, both eyes, contoured face")
    PROFILE = ("framed in profile", "side view, half the face; aloof, secretive, guarded")
    THREE_QUARTER_BACK = ("framed from a three-quarter back angle", "shades toward an over-the-shoulder; shares the subject's POV")
    REVERSE = ("framed from behind, a full-back reverse", "face hidden; mystery, suspense, leads into a reveal")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class ShootingStyle(Enum):
    """Whether the subject acknowledges the lens."""

    OBJECTIVE = ("the subject never looks at the lens, observed objectively", "the fiction default; the camera as an unseen observer")
    SUBJECTIVE = ("the subject looks directly into the lens, addressing the viewer", "direct address — news, hosts, vlogs; breaks the fourth wall")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Composition(Enum):
    """Placement of the subject within the frame."""

    CENTERED = ("centered composition", "symmetrical and neutral; portraiture, news, direct address")
    RULE_OF_THIRDS = ("composed on the rule-of-thirds lines with look room across the frame", "balanced mass and void; the objective-style default")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class FocalLength(Enum):
    """Lens focal length — sets perspective and how space reads."""

    FISHEYE = ("shot on an ultra-wide fisheye lens", "warped, surreal distortion; 'not normal'")
    WIDE = ("shot on a wide-angle lens", "expands depth, exaggerates space; roomy and energetic")
    NORMAL = ("shot on a normal lens", "natural human perspective, no distortion")
    LONG = ("shot on a long telephoto lens", "compresses and flattens space; isolating")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class DepthOfField(Enum):
    """How much of the depth is held in acceptable focus."""

    SHALLOW = ("shallow depth of field, the background thrown soft", "isolates the subject; the cinematic look")
    DEEP = ("deep depth of field, foreground to background sharp", "keeps the whole frame in focus")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Cinematographer(Role):
    """The camera department head — owns framing and lens/focus."""

    title = "Cinematographer"
    department = Department.CAMERA
    phase = Phase.SHOOT
    vocabulary = (
        ShotSize,
        SubjectView,
        CameraAngle,
        ShootingStyle,
        Composition,
        FocalLength,
        DepthOfField,
    )
