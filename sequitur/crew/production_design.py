"""The art department — the **Production Designer** (plan phase).

Owns the studio's *design* vocabulary: Michael Rizzo's *The Art Direction Handbook*
(storyline 0044/0045) reduced to the axes that survive the jump to a generative image
backend. Where the :class:`~sequitur.crew.screenwriting.Screenwriter` classifies the
*story*, the Production Designer lands the *world's look* — the single central visual
concept the image backend serves, plus the closed axes that place that concept in a
medium and an era.

Rizzo's split (Ch. 1): the **Production Designer owns the visual concept**; the Art
Director owns its *realisation*. In the studio the realisation half is code —
:func:`~sequitur.prompt.build_image_prompt` and
:class:`~sequitur.image.ImageStudio` — so this seat owns only the *concept*: the
plan-phase intent fed into the image backend, a peer of the Director's
:class:`~sequitur.crew.role.Brief` rather than a layer above it.

Like ``crew/screenwriting.py`` (storyline 0012 / 0035) this is **vocabulary + a
heuristic default**: the Production Designer's :class:`~sequitur.crew.role.Contribution`
is a *design descriptor*, not a :class:`~sequitur.shot.Shot`. The central concept is an
open ``str`` the heuristic leaves blank — the deterministic **A** lands the structural
axes; the persona **B** narrates the central image, the way a treatment narrates what
the Screenwriter descriptor can only tag.

Only **design intent** transfers: a generative backend has no location scout, no
construction budget, no wild walls (Ch. 5). What survives is the concept (Ch. 4), the
medium/era *look* (Ch. 3), the underscore-vs-contrast stance (Ch. 4), and the
interior/exterior division (Ch. 5).
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from .role import Department, Phase, Role

if TYPE_CHECKING:
    from .role import Brief


class ConceptStance(Enum):
    """Does the design *echo* the scene's emotion or *push against* it (Ch. 4)?

    Rizzo's underscore-vs-contrast choice — one of the four paths to a visual
    concept. Underscoring reinforces the scene's feeling; contrasting sets the
    design at odds with it (a cheerful nursery staging a horror beat).
    """

    UNDERSCORE = ("underscores the scene", "the design echoes and reinforces the scene's emotion")
    CONTRAST = ("contrasts the scene", "the design pushes against the scene's emotion for tension")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class MediumLook(Enum):
    """The physical image the frame imitates — film and video are different images (Ch. 3).

    Rizzo's clearest closed distinction: a "1970s TV drama" asks for the *video*
    column (interlaced, CRT-soft), a "70mm epic" for the *film* column (grain, wide,
    projected). ``DIGITAL`` is the modern clean sensor look, the neutral default.
    """

    FILM = ("a film look", "grain, wide gauge, projected cadence, exposure latitude")
    VIDEO = ("a video look", "interlaced fields, CRT phosphor glow, scanlines, telecine judder")
    DIGITAL = ("a clean digital look", "modern sensor clarity, no grain or scanline artefact")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class EraMarker(Enum):
    """A recognizable medium-era look — one token carries a whole learned image (Ch. 3).

    Rizzo's "Visual History" is a history of the *medium*, not of art movements, so
    these are technology/era markers (optical toy -> CRT -> web), not period palettes.
    Palette/period *execution* belongs to the
    :class:`~sequitur.crew.colorist.Colorist`'s grade; this names the era the concept
    evokes. ``CONTEMPORARY`` is the unmarked, present-day default.
    """

    OPTICAL_TOY = ("optical-toy animation", "hand-cranked, looping, illustrated parlor-novelty")
    SILENT_ERA = ("silent-era cinema", "sepia/tinted, flicker, black-flocked studio")
    MECHANICAL_TV = ("mechanical-TV broadcast", "crude low-line raster, monochrome, ghosting")
    BROADCAST_BW = ("broadcast black-and-white", "electronic-TV scanlines, monochrome")
    NTSC_COLOR = ("NTSC-color television", "4:3, CRT color, interlaced broadcast")
    DIGITAL_WEB = ("web / short-form digital", "small-screen, compressed, handheld")
    CONTEMPORARY = ("contemporary / timeless", "no era marker — present-day, unmarked")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class SetKind(Enum):
    """The fundamental division of a set — designed *for the camera*, not literal reality (Ch. 5)."""

    INTERIOR = "an interior set"
    EXTERIOR = "an exterior set"

    @property
    def phrase(self) -> str:
        return self.value


class ProductionDesigner(Role):
    """The art department head — owns the visual-concept vocabulary (plan phase).

    Its :class:`~sequitur.crew.role.Contribution` is a *design descriptor* — the
    world's look — not a :class:`~sequitur.shot.Shot`. Rizzo places the Production
    Designer level with the Director (Ch. 1); in code it is a peer plan-phase
    :class:`Role` whose descriptor overlays the Director's
    :class:`~sequitur.crew.role.Brief` (scene + mood) with the art department's
    central image before :func:`~sequitur.prompt.build_image_prompt` renders a shot
    for :class:`~sequitur.image.ImageStudio`.
    """

    title = "Production Designer"
    department = Department.ART
    phase = Phase.PLAN
    vocabulary = (ConceptStance, MediumLook, EraMarker, SetKind)

    def heuristic(self, brief: Brief) -> dict[str, Any]:
        # The neutral design: a clean, contemporary interior that underscores the
        # scene. The central `visual_concept` is left blank for the persona (B) — the
        # heuristic (A) lands only the structural axes; hints override any field.
        h = brief.hints
        return {
            "visual_concept": h.get("visual_concept", ""),
            "concept_stance": h.get("concept_stance", ConceptStance.UNDERSCORE),
            "medium_look": h.get("medium_look", MediumLook.DIGITAL),
            "era": h.get("era", EraMarker.CONTEMPORARY),
            "set_kind": h.get("set_kind", SetKind.INTERIOR),
            "motifs": list(h.get("motifs", [])),
        }
