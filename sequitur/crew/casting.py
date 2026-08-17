"""The casting department — the **Casting Director** (plan phase).

Owns the studio's *casting* vocabulary: Rabiger & Hurbis-Cherrier's *Directing* Ch. 18
(storyline 0017), the performance layer no earlier source or code modelled. Where the
:class:`~sequitur.crew.screenwriting.Screenwriter` classifies the *story* and the
:class:`~sequitur.crew.production_design.ProductionDesigner` lands the *world's look*,
the Casting Director casts the *people* — the human beings who embody the characters.

In a generative studio there are no human actors, so "casting" is both a **design** and
a **selection** (Ch. 18's *"what would this actor* give *the film?"* + its **abundance**
principle): the seat conceives a character's look, generates several candidate
embodiments — the audition — and the Producer selects one. The selected embodiment's
reference is the character's *locked* appearance, which every downstream render
(key art, storyboard, shots) conditions on for consistency — the generative analogue of
"an actor who can re-enter the same state across many takes."

Like ``crew/screenwriting.py`` (0035) and ``crew/production_design.py`` (0046) this is
**vocabulary + a heuristic default**: the seat owns the closed axes a role is cast *for*
(:class:`AgeBand`, :class:`Billing`, from Ch. 18's *suitability* / *billing*
distinctions); the specific look, essence, and wardrobe are open ``str`` the deterministic
**A** leaves blank for the persona **B** to narrate from the treatment — the same
descriptor-vs-narration split the Production Designer draws. The cast itself lives in the
:mod:`sequitur.cast` entities (:class:`~sequitur.cast.Character` / :class:`~sequitur.cast.Actor`),
not a :class:`~sequitur.shot.Shot`: casting produces the *cast list*, a second diegetic axis
orthogonal to the ``Cut -> Act -> Scene -> Beat -> Shot`` structure.

Only what *transfers* to a generated identity is modelled: the *suitability* axes (age,
billing) and the open look/essence/wardrobe/voice. The actor-as-person axes Ch. 18 tests —
directability, commitment, grasp of acting — have no generative analogue (there is no
person to direct), just as the Production Designer drops the location scout and the wild
walls (Rizzo Ch. 5).
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from .role import Department, Phase, Role

if TYPE_CHECKING:
    from .role import Brief


class AgeBand(Enum):
    """The age register a role is cast for — the first *suitability* axis (Ch. 18).

    Ch. 18 lists *suitability* as age / gender / physical type / ethnicity. Age is the
    one cleanly closed axis (the others are open look narration); ``ADULT`` is the
    unmarked default.
    """

    CHILD = "a child"
    TEEN = "a teenager"
    YOUNG_ADULT = "a young adult"
    ADULT = "an adult"
    MIDDLE_AGED = "a middle-aged adult"
    SENIOR = "an older adult"

    @property
    def phrase(self) -> str:
        return self.value


class Billing(Enum):
    """Principal vs background casting (Ch. 18) — a lead the audience tracks, or texture.

    Ch. 18's *principal casting* (main speaking parts, auditioned for interpretive fit)
    vs *background casting* (clerks, diners — chosen for appearance, often without
    audition). In the studio it sets how much a character's look is *locked*: a principal
    gets a consistent cast reference threaded downstream; background is ambient.
    """

    PRINCIPAL = ("a principal role", "a lead the audience tracks — cast and locked to a reference")
    BACKGROUND = ("a background role", "texture chosen for appearance — no locked reference")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class CastingDirector(Role):
    """The casting department head — owns the casting vocabulary (plan phase).

    Its :class:`~sequitur.crew.role.Contribution` is the production's **cast** — a list of
    :class:`~sequitur.cast.Character` (the roles), not a :class:`~sequitur.shot.Shot`. The
    heuristic **A** cannot read the treatment (that is the persona **B**'s job), so it
    passes any producer-supplied cast through and otherwise leaves the cast empty for the
    persona to populate from the story — the same way the Production Designer leaves its
    central ``visual_concept`` blank. The :class:`~sequitur.crew.director.Director`'s
    plan reconcile routes this contribution into :attr:`sequitur.plan.Plan.cast`.
    """

    title = "Casting Director"
    department = Department.CASTING
    phase = Phase.PLAN
    vocabulary = (AgeBand, Billing)

    def heuristic(self, brief: Brief) -> dict[str, Any]:
        # A has no treatment to read characters from; the persona (B) designs the cast.
        # Pass a producer-supplied cast through (tests / HITL), else leave it empty.
        return {"cast": list(brief.hints.get("cast", []))}
