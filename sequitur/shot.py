"""The shot — the aggregate spec the camera, electric, and grip crews compose.

A :class:`Shot` is the collective *output* of the shoot-phase crew: the
Cinematographer's framing and lens/focus, the Gaffer's lighting, the Key Grip's
movement and speed, plus the scene and delivery direction. It is the unit the
renderers consume (:class:`~sequitur.studio.Studio`,
:class:`~sequitur.image.ImageStudio`) and what :func:`~sequitur.prompt.build_prompt`
turns into a model prompt. It stays a single flat aggregate on purpose — the
crew's shared canvas, not one fragment per department.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .crew.camera import (
    CameraAngle,
    Composition,
    DepthOfField,
    FocalLength,
    ShootingStyle,
    ShotSize,
    SubjectView,
)
from .crew.grip import CameraMovement, MotionSpeed
from .crew.lighting import (
    ColorTemperature,
    LightDirection,
    LightQuality,
    LightScheme,
)

if TYPE_CHECKING:
    from .cast import Character


@dataclass
class Shot:
    """A single shot specification.

    `scene` is the essential description — subject, action and setting. Every
    other field is an optional layer of cinematographic grammar composed on top.
    """

    scene: str

    # Framing (Ch. 1–2) — Cinematographer
    size: ShotSize | None = None
    view: SubjectView | None = None            # horizontal angle on the subject
    angle: CameraAngle | None = None           # vertical angle / canting
    style: ShootingStyle | None = None         # objective vs direct-address
    composition: Composition | None = None

    # Lens & focus (Ch. 3) — Cinematographer
    focal_length: FocalLength | None = None
    depth_of_field: DepthOfField | None = None
    lens: str | None = None                    # free-text extras, e.g. "35mm anamorphic"

    # Lighting (Ch. 4) — Gaffer; orthogonal axes
    light_scheme: LightScheme | None = None
    light_quality: LightQuality | None = None
    light_direction: LightDirection | None = None
    color_temp: ColorTemperature | None = None
    eye_light: bool = False                    # catch light glint in the eyes

    # Motion (Ch. 6) — Key Grip
    movement: CameraMovement | None = None
    speed: MotionSpeed | None = None           # slow / fast / time-lapse

    # Delivery & direction
    mood: str | None = None                    # e.g. "melancholy, contemplative"
    audio: str | None = None                   # diegetic sound + music direction
    timing: str | None = None                  # e.g. "[0-8s]" or beat-by-beat timecodes
    single_scene: bool = True                  # one continuous shot, no cuts (Ch. 5)
    avoid: list[str] = field(default_factory=list)  # negative prompts, spoken inline
    aspect_ratio: str = "16:9"                 # "16:9" (landscape) or "9:16" (portrait)

    # The cast in frame (storyline 0057) — the diegetic join to the cast axis. Which
    # Characters this shot features; the prompt names them and a backend conditions on
    # their locked references for consistency. Empty for shots with no principals.
    cast: list["Character"] = field(default_factory=list)

    def locked_references(self) -> list[str]:
        """The locked reference of each cast Character with a selected embodiment.

        A backend uses these to *condition* the render on the cast's identities (the
        gpt-image edits array, or Omni's multimodal input). Characters not yet cast, or
        cast to an Actor without a reference, contribute nothing.
        """
        refs: list[str] = []
        for character in self.cast:
            actor = getattr(character, "cast", None)
            reference = getattr(actor, "reference", None) if actor else None
            if reference:
                refs.append(str(reference))
        return refs
