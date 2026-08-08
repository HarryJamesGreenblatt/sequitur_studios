"""The grammar of the edit — the post-production assembly engine.

Where :mod:`sequitur.grammar` gives the studio the language of a single *shot*,
this module gives it the language of the *cut*: how shots are chosen, joined, and
paced into a sequence. The vocabulary and the shots -> scenes -> acts model are
distilled from Christopher J. Bowen's *Grammar of the Edit* (4th ed.); see
``artifacts/grammar of the edit/`` for the grounding.

This is the **model-agnostic core** of the post layer — the counterpart to
``grammar.py``, not to ``studio.py``. It represents an edit decision list (an EDL)
and the reasons behind it, and it validates that list against the source's rules
(handles for dissolves, a reason for every cut). It is deliberately **free of any
rendering dependency** so this decision state can be serialised into a production
plan — a PM framework such as Planner, ADO, or GitHub Projects (storyline 0005 /
0007). Turning the EDL into a finished film — stitching the rendered clips with real
transitions — is a separate, swappable *executor* concern: :class:`sequitur.cutter.Cutter`
(MoviePy), the post layer's data-plane renderer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .grammar import Shot


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


@dataclass
class Clip:
    """A unit of coverage in the timeline: a :class:`~sequitur.grammar.Shot` with edit timing.

    ``duration`` is the visible length on screen. ``head_handle`` / ``tail_handle``
    are the spare seconds of the *same* shot beyond the visible IN/OUT — the
    material a dissolve or wipe borrows (Ch. 6). ``source`` points at the rendered
    clip once it exists.
    """

    shot: Shot
    duration: float = 4.0
    head_handle: float = 0.0
    tail_handle: float = 0.0
    source: str | None = None


@dataclass
class Edit:
    """The join that brings us *into* a clip.

    ``reason`` should always be present (Ch. 8). ``duration`` is the transition
    length in seconds — zero for a cut.
    """

    transition: Transition = Transition.CUT
    reason: EditReason | None = None
    category: EditCategory | None = None
    duration: float = 0.0


@dataclass
class Beat:
    """A clip plus the edit that introduces it."""

    clip: Clip
    edit_in: Edit = field(default_factory=Edit)


@dataclass
class Scene:
    """An ordered run of clips covering one continuous action or place."""

    beats: list[Beat] = field(default_factory=list)
    slug: str | None = None  # e.g. "INT. KITCHEN - DAY"

    def add(
        self,
        shot: Shot | Clip,
        *,
        transition: Transition = Transition.CUT,
        reason: EditReason | None = None,
        category: EditCategory | None = None,
        transition_duration: float = 0.0,
        duration: float = 4.0,
        head_handle: float = 0.0,
        tail_handle: float = 0.0,
    ) -> "Scene":
        """Append a shot (or ready-made clip) as a new beat. Chainable."""
        clip = (
            shot
            if isinstance(shot, Clip)
            else Clip(shot, duration=duration, head_handle=head_handle, tail_handle=tail_handle)
        )
        edit = Edit(transition=transition, reason=reason, category=category, duration=transition_duration)
        self.beats.append(Beat(clip, edit))
        return self


@dataclass
class Act:
    """An ordered run of scenes."""

    scenes: list[Scene] = field(default_factory=list)
    title: str | None = None


@dataclass
class TimelineEntry:
    """One placed clip in the flattened timeline, with absolute start/end seconds."""

    clip: Clip
    edit_in: Edit
    start: float
    end: float
    scene_slug: str | None = None
    act_title: str | None = None


@dataclass
class Sequence:
    """A whole assembly — the shots -> scenes -> acts hierarchy for one production."""

    acts: list[Act] = field(default_factory=list)
    title: str | None = None
    aspect_ratio: str = "16:9"

    # -- traversal ---------------------------------------------------------

    def _ordered(self):
        """Yield ``(act, scene, beat)`` in playback order."""
        for act in self.acts:
            for scene in act.scenes:
                for beat in scene.beats:
                    yield act, scene, beat

    def timeline(self) -> list[TimelineEntry]:
        """Flatten to an ordered EDL with absolute times.

        A handle-borrowing transition (dissolve/wipe) overlaps the two clips by
        its duration; a cut or fade does not shift the incoming clip.
        """
        entries: list[TimelineEntry] = []
        cursor = 0.0
        for i, (act, scene, beat) in enumerate(self._ordered()):
            edit = beat.edit_in
            if i == 0:
                start = 0.0
            elif edit.transition.needs_handles:
                start = cursor - edit.duration
            else:
                start = cursor
            end = start + beat.clip.duration
            entries.append(TimelineEntry(beat.clip, edit, start, end, scene.slug, act.title))
            cursor = end
        return entries

    @property
    def runtime(self) -> float:
        """Total screen time in seconds, accounting for transition overlaps."""
        tl = self.timeline()
        return tl[-1].end if tl else 0.0

    def validate(self) -> list[str]:
        """Lint the EDL against the source's rules; return human-readable issues.

        Errors: a dissolve/wipe without enough handle on either side, or without
        a positive duration (Ch. 6). Warnings: a cut with no stated reason
        (Ch. 8, "a reason for every edit").
        """
        issues: list[str] = []
        prev: Clip | None = None
        for i, (_act, _scene, beat) in enumerate(self._ordered()):
            edit = beat.edit_in
            where = _short(beat.clip.shot)
            if edit.transition.needs_handles:
                if edit.duration <= 0:
                    issues.append(f"error: {edit.transition.phrase} into '{where}' needs a positive duration")
                need = edit.duration / 2  # centred transition borrows half from each side
                if prev is not None and prev.tail_handle < need:
                    issues.append(
                        f"error: {edit.transition.phrase} into '{where}' needs >= {need:g}s tail handle "
                        f"on the outgoing clip, has {prev.tail_handle:g}s (Ch. 6)"
                    )
                if beat.clip.head_handle < need:
                    issues.append(
                        f"error: {edit.transition.phrase} into '{where}' needs >= {need:g}s head handle, "
                        f"has {beat.clip.head_handle:g}s (Ch. 6)"
                    )
            elif i > 0 and edit.transition is Transition.CUT and edit.reason is None:
                issues.append(f"warning: cut into '{where}' has no reason (Ch. 8: a reason for every edit)")
            prev = beat.clip
        return issues


def _short(shot: Shot, width: int = 40) -> str:
    """A short, single-line description of a shot for lint messages."""
    text = shot.scene.strip().replace("\n", " ")
    return text if len(text) <= width else text[: width - 1] + "…"
