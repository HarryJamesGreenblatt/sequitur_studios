"""The editorial department — the **Editor** (assemble phase).

Owns the grammar of the *cut*: how one shot gives way to the next (`Transition`,
Ch. 6), *why* we cut here (`EditReason` — the six motivators, Ch. 5), and what
*kind* of edit it is (`EditCategory`, Ch. 6). This is the editorial counterpart to
the camera/electric/grip vocabulary — the closed language the Editor wields to
assemble shots into a sequence.

The assembly *model* the Editor composes with this vocabulary (the
shots -> scenes -> acts EDL, plus its `timeline()`/`validate()` logic) lives in
:mod:`sequitur.edit` — the editorial analogue of :mod:`sequitur.shot`.
"""

from __future__ import annotations

from enum import Enum

from .role import Department, Phase, Role


class Transition(Enum):
    """How one shot gives way to the next (Grammar of the Edit, Ch. 6).

    ``needs_handles`` marks transitions that borrow frames from *beyond* the
    visible clip — a hard constraint on fixed-length generated coverage, which
    must be produced with handle padding for those transitions to be possible.
    """

    CUT = ("a straight cut", "instantaneous; continuous action or a clean change of information", False)
    DISSOLVE = ("a dissolve", "gradual blend; a change of time or place, or a softer, somber link", True)
    WIPE = ("a wipe", "a shape or line pushes the old shot off; fanciful, a bold change of place", True)
    FADE_IN = ("a fade in from black", "opens a program, act, or scene out of black", False)
    FADE_OUT = ("a fade out to black", "closes a program, act, or scene into black", False)
    DIP_TO_BLACK = ("a dip to black", "a fade out straight into a fade in; a long, slow blink between segments", False)

    def __init__(self, phrase: str, intent: str, needs_handles: bool) -> None:
        self.phrase = phrase
        self.intent = intent
        self.needs_handles = needs_handles


class EditReason(Enum):
    """Why cut here — the six motivators for an edit (Ch. 5).

    Every edit should name at least one: "there should be a reason for every
    edit" (Ch. 8).
    """

    INFORMATION = ("new information", "the incoming shot delivers something new to see, hear, or feel")
    MOTIVATION = ("motivation", "a movement, look, or sound in the outgoing shot prompts the leave")
    COMPOSITION = ("composition", "eye-line and eye-trace carry the viewer across the cut")
    CAMERA_ANGLE = ("camera angle", "a sufficiently different angle (>30 deg) avoids a jump cut")
    CONTINUITY = ("continuity", "matched action, screen direction, and position keep the flow invisible")
    SOUND = ("sound", "a sound in or under the shot motivates or bridges the cut")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class EditCategory(Enum):
    """The kind of edit — why it works (Ch. 6)."""

    ACTION = ("action edit", "a cut on continuous, matched movement (the match cut)")
    SCREEN_POSITION = ("screen-position edit", "subject placement directs the eye across the frame; shot/reverse dialogue")
    FORM = ("form edit", "matched shape, colour, or composition across the cut (often a match dissolve)")
    CONCEPT = ("concept edit", "juxtaposition creates implied meaning not stated in the story")
    COMBINED = ("combined edit", "two or more of the above satisfied in one edit")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Editor(Role):
    """The editorial department head — owns the grammar of the cut.

    Composes the shots -> scenes -> acts model in :mod:`sequitur.edit` with this
    vocabulary; the executor that renders the EDL into a film is
    :class:`sequitur.cutter.Cutter`.
    """

    title = "Editor"
    department = Department.EDITORIAL
    phase = Phase.ASSEMBLE
    vocabulary = (Transition, EditReason, EditCategory)
