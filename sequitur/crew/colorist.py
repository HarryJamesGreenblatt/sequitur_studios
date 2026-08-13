"""The color department — the **Colorist** (post / finishing phase).

Owns the grammar of the *grade*: the named creative **looks** the Colorist reasons
over, the three **tonal ranges** (the lift/gamma/gain zones, Color Correction
Handbook Ch. 3), and the grade-side **cast** re-balance vocabulary (Ch. 4). The
tonal ranges and casts are closed axes; the looks are an *open, extensible preset
library* (no completeness claim) that compiles into the comprehensive op basis in
:mod:`sequitur.grade`. Together they are the colour counterpart to the
camera/electric/grip vocabulary — the language the Colorist wields to grade a
rendered clip.

The reified, executable form those choices compile into (an ordered stack of
color-correction ops) lives in :mod:`sequitur.grade` — the color analogue of
:mod:`sequitur.edit`; the executor that turns a grade into pixels is
:class:`sequitur.grader.Grader`.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from .role import Department, Phase, Role

if TYPE_CHECKING:
    from ..grade import Grade
    from .role import Brief


class TonalRange(Enum):
    """A tonal zone of the image — the three lift/gamma/gain bands (Ch. 3)."""

    SHADOWS = ("the darkest values — the black point (lift)", "deepen or lift the floor for snap or a soft look")
    MIDTONES = ("the middle values — the gamma band", "the 'steak': subject, time-of-day, and mood live here")
    HIGHLIGHTS = ("the brightest values — the white point (gain)", "set peak brightness; keep it broadcast-legal")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Look(Enum):
    """A named creative grade — a *preset*, not a closed taxonomy (Ch. 3-4).

    Unlike the DP's genuinely closed axes (``ShotSize``, ``Transition``), creative
    looks are unbounded, so this set makes **no completeness claim** — it is the
    colour analogue of the taxonomy's open-tag ``Microgenre`` (storyline 0016), a
    curated, extensible library of common starting points that seeds the judgment
    layer. The comprehensive vocabulary is the reified op basis in
    :mod:`sequitur.grade` (``Contrast`` / ``ColorBalance`` / ``Saturation``, with
    HSL/Shape secondaries to come); any look outside this library is authored
    directly as a :class:`~sequitur.grade.Grade` stack — the colour analogue of
    building a :class:`~sequitur.edit.Sequence` by hand — and a production can name
    and reuse one via :func:`sequitur.grade.register_look`. Each member compiles
    into such a stack via :meth:`Colorist.grade`.
    """

    NEUTRAL = ("a clean, natural grade", "a gentle contrast expand, colour left true")
    WARM = ("a warm grade", "amber highlights; cozy, inviting, nostalgic")
    COOL = ("a cool grade", "blue highlights; calm, clinical, distant")
    GOLDEN_HOUR = ("a golden-hour grade", "orange gain countered in the mids so faces don't over-tan")
    TEAL_ORANGE = ("a teal-and-orange grade", "warm skin against teal shadows; the blockbuster look")
    NOIR = ("a low-key noir grade", "crushed blacks, high contrast, near-desaturated")
    BLEACH_BYPASS = ("a bleach-bypass grade", "high contrast, low saturation; gritty, silvery")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Cast(Enum):
    """A grade-side white-balance re-balance direction (Ch. 4).

    Distinct from the Gaffer's capture-time
    :class:`~sequitur.crew.lighting.ColorTemperature`: that sets white balance
    *under the lights*; this *corrects or re-casts* it in the grade. The two seats
    speak the same "warm/cool" language at different pipeline stages — the
    capture-vs-grade overlap flagged in storyline 0020.
    """

    NEUTRAL = ("neutralize the cast", "push toward the complement to restore true grays")
    WARM = ("re-cast warm", "shift toward orange for warmth or magic hour")
    COOL = ("re-cast cool", "shift toward blue for night or a clinical feel")
    GREEN = ("a green cast", "fluorescent unease — counter with magenta in the mids")
    MAGENTA = ("a magenta cast", "rarely wanted; the trap when over-correcting a green cast")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Colorist(Role):
    """The color department head — owns the grade grammar (post / finishing).

    Composes an ordered :class:`~sequitur.grade.Grade` from a :class:`Look`; the
    executor that renders that grade over a clip is :class:`sequitur.grader.Grader`.
    """

    title = "Colorist"
    department = Department.COLOR
    phase = Phase.ASSEMBLE
    vocabulary = (Look, TonalRange, Cast)

    def heuristic(self, brief: Brief) -> dict[str, Any]:
        # The assemble-phase contribution is the base grade for the sequence's look.
        return {"grade": self.grade(brief.hints.get("look", Look.NEUTRAL))}

    def grade(self, look: Look | str | None = None, *, source: str | None = None) -> Grade:
        """Compile a :class:`Look` preset — or a production's registered look name —
        into a reified :class:`~sequitur.grade.Grade` stack bound to ``source``.

        A ``str`` resolves a production-defined look via
        :func:`~sequitur.grade.register_look`; a :class:`Look` compiles a built-in
        preset. Contrast ops precede colour ops precede saturation, honouring the
        book's "grade contrast first, colour second" rule (Ch. 3-4) so the stack
        passes :meth:`~sequitur.grade.Grade.validate`.
        """
        from ..grade import ColorBalance, Contrast, Grade, Saturation, named_look

        if isinstance(look, str):
            return named_look(look, source=source)

        look = look or Look.NEUTRAL
        g = Grade(source=source, name=look.name.lower())

        if look is Look.NEUTRAL:
            g.add(Contrast(gain=1.05))
        elif look is Look.WARM:
            g.add(Contrast(gain=1.05))
            g.add(ColorBalance(TonalRange.HIGHLIGHTS, r=0.12, b=-0.08))
            g.add(Saturation(1.08))
        elif look is Look.COOL:
            g.add(Contrast(gain=1.03))
            g.add(ColorBalance(TonalRange.HIGHLIGHTS, b=0.12, r=-0.06))
        elif look is Look.GOLDEN_HOUR:
            g.add(Contrast(lift=0.02, gain=1.05))
            g.add(ColorBalance(TonalRange.HIGHLIGHTS, r=0.18, g=0.06, b=-0.12))
            g.add(ColorBalance(TonalRange.MIDTONES, b=0.06))  # counter so faces don't over-tan (Ch. 4)
            g.add(Saturation(1.10))
        elif look is Look.TEAL_ORANGE:
            g.add(Contrast(gamma=0.95, gain=1.08))
            g.add(ColorBalance(TonalRange.HIGHLIGHTS, r=0.15, b=-0.06))
            g.add(ColorBalance(TonalRange.SHADOWS, b=0.15, r=-0.10))
            g.add(Saturation(1.12))
        elif look is Look.NOIR:
            g.add(Contrast(lift=-0.04, gamma=0.90, gain=1.15))
            g.add(Saturation(0.35))
        elif look is Look.BLEACH_BYPASS:
            g.add(Contrast(gamma=0.92, gain=1.20))
            g.add(Saturation(0.50))

        return g
