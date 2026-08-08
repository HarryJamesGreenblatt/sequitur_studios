"""The grammar of the shot.

Structured cinematographic vocabulary distilled from Christopher J. Bowen's
*Grammar of the Shot* (4th ed.). Each enum member carries a human-readable
phrase (for prompts) and its narrative intent — plus, for shot sizes, the
industry short code — so the studio speaks proper film language when it talks to
the model, and the reasoning behind each choice stays legible in code.

The layers are deliberately *orthogonal*, mirroring the source: Ch. 2 splits the
horizontal angle on the subject from the vertical camera angle; Ch. 4 splits
lighting into quality, scheme, direction and colour; Ch. 6 separates playback
speed from camera movement. They compose freely on a single :class:`Shot`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


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


@dataclass
class Shot:
    """A single shot specification.

    `scene` is the essential description — subject, action and setting. Every
    other field is an optional layer of cinematographic grammar composed on top.
    """

    scene: str

    # Framing (Ch. 1–2)
    size: ShotSize | None = None
    view: SubjectView | None = None            # horizontal angle on the subject
    angle: CameraAngle | None = None           # vertical angle / canting
    style: ShootingStyle | None = None         # objective vs direct-address
    composition: Composition | None = None

    # Lens & focus (Ch. 3)
    focal_length: FocalLength | None = None
    depth_of_field: DepthOfField | None = None
    lens: str | None = None                    # free-text extras, e.g. "35mm anamorphic"

    # Lighting (Ch. 4) — orthogonal axes
    light_scheme: LightScheme | None = None
    light_quality: LightQuality | None = None
    light_direction: LightDirection | None = None
    color_temp: ColorTemperature | None = None
    eye_light: bool = False                    # catch light glint in the eyes

    # Motion (Ch. 6)
    movement: CameraMovement | None = None
    speed: MotionSpeed | None = None           # slow / fast / time-lapse

    # Delivery & direction
    mood: str | None = None                    # e.g. "melancholy, contemplative"
    audio: str | None = None                   # diegetic sound + music direction
    timing: str | None = None                  # e.g. "[0-8s]" or beat-by-beat timecodes
    single_scene: bool = True                  # one continuous shot, no cuts (Ch. 5)
    avoid: list[str] = field(default_factory=list)  # negative prompts, spoken inline
    aspect_ratio: str = "16:9"                 # "16:9" (landscape) or "9:16" (portrait)
