"""The cast — the diegetic people of a production (:class:`Character`) and the generated
identities that embody them (:class:`Actor`).

The **cast axis** the studio was missing (storyline 0054). The narrative aggregates
decompose the *work* — a :class:`~sequitur.shot.Shot` is a frame, a
:class:`~sequitur.edit.Sequence` the assembled whole — but nothing represented the
*people*. A character is not a node under a scene: it cuts **across** the
``Cut -> Act -> Scene -> Beat -> Shot`` structure (a protagonist appears in many scenes),
so it is a second diegetic axis orthogonal to that tree, authored in the plan phase by the
:class:`~sequitur.crew.casting.CastingDirector`.

Casting is both a **design** and a **selection** (Directing Ch. 18): the Casting Director
conceives a :class:`Character` (the role), generates several candidate :class:`Actor`
embodiments (the *audition*'s abundance), and the Producer selects one — the **cast** actor,
whose ``reference`` is the character's locked look for every downstream render. This mirrors
the one relation at the heart of casting: an *Actor plays a Character*.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .crew.casting import AgeBand, Billing


@dataclass
class Actor:
    """A generated visual identity that can embody a :class:`Character` — a casting candidate.

    In a generative studio there are no human actors; an Actor is a *look* — a described
    visual identity plus a reference image downstream renders condition on for
    consistency. Many Actors audition for one Character (Ch. 18's abundance); the one the
    Producer selects is *cast*, and its ``reference`` becomes the character's locked
    appearance. ``voice`` names the neural voice the
    :class:`~sequitur.speech.SpeechRenderer` will drive — Ch. 18's through-line that voice
    quality is cast, not just appearance.
    """

    look: str = ""                     # the visual identity — persona-authored (B)
    reference: str | None = None       # durable ref of this candidate's keyframe
    voice: str | None = None           # the neural voice ref (feeds SpeechRenderer)
    notes: str = ""


@dataclass
class Character:
    """A diegetic role — a person in the story; the cast axis orthogonal to the tree.

    Authored in the plan phase from the story/treatment, a Character carries its casting
    **design brief** — the grounded *suitability* axes it is cast *for*
    (:class:`~sequitur.crew.casting.Billing`, :class:`~sequitur.crew.casting.AgeBand`) plus
    the open look/essence/wardrobe the persona narrates — its **audition**
    (``candidates``: the abundance of :class:`Actor` embodiments), and the selected
    embodiment (``cast``). The cast Actor's ``reference`` is the character's locked look.
    """

    name: str
    billing: Billing = Billing.PRINCIPAL
    age_band: AgeBand = AgeBand.ADULT
    role: str = ""                     # dramatic function — protagonist, foil, mentor...
    essence: str = ""                  # who they are — persona-authored from the treatment
    build: str = ""                    # physical type / presence (Ch. 18) — open
    wardrobe: str = ""                 # costume register — open
    candidates: list[Actor] = field(default_factory=list)  # the audition (abundance)
    cast: Actor | None = None          # the selected embodiment — the locked look

    def select(self, actor: Actor) -> None:
        """Cast one auditioned :class:`Actor` — the Producer's verdict (storyline 0054).

        Binds the chosen embodiment as :attr:`cast`; its ``reference`` is now the
        character's locked look for every downstream render. Only an Actor that
        *auditioned* (is among :attr:`candidates`) can be cast — the abundance-then-
        selection discipline (Directing Ch. 18): you choose from the field you called.
        """
        if actor not in self.candidates:
            raise ValueError(f"{actor.look!r} did not audition for {self.name!r}.")
        self.cast = actor
