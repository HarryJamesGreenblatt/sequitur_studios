"""The plan aggregate — the reconciled story + design of a production (plan phase).

The plan-phase analogue of :mod:`sequitur.shot` (the shoot aggregate) and
:mod:`sequitur.edit` (the assemble aggregate). Where the shoot crew reconciles into a
:class:`~sequitur.shot.Shot` and the post crew into a :class:`~sequitur.edit.Sequence`,
the plan crew reconciles into a :class:`Plan`: the
:class:`~sequitur.crew.screenwriting.Screenwriter`'s **story descriptor** and the
:class:`~sequitur.crew.production_design.ProductionDesigner`'s **design descriptor**,
merged into one plan-phase decision.

Unlike a :class:`~sequitur.shot.Shot`, a :class:`Plan` is not itself renderable — it is
the *intent* the later phases realise. Its two deliverables (the dailies model, storyline
0036) are a human-readable **treatment** (from the story half) and a **poster** (the
design half as one evocative frame), produced from these descriptors and reviewed at a
:class:`~sequitur.gate.Gate`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .cast import Character


@dataclass
class Plan:
    """The reconciled plan of a production — story + design descriptors + cast (plan phase).

    The halves carry each plan seat's *owned* slice (disjoint, so the reconcile is
    loss-free): ``story`` is the Screenwriter's taxonomy layers (storyline 0035); ``design``
    is the Production Designer's visual concept + look (storyline 0046); ``cast`` is the
    Casting Director's :class:`~sequitur.cast.Character` list (storyline 0054) — the second
    diegetic axis, orthogonal to the narrative tree.
    ``scene``/``mood``/``aspect_ratio`` pass through from the :class:`~sequitur.crew.role.Brief`.
    """

    scene: str
    mood: str | None = None
    aspect_ratio: str = "16:9"
    #: The Screenwriter's story descriptor — movie type / supergenre / voice / pathway / POV.
    story: dict[str, Any] = field(default_factory=dict)
    #: The Production Designer's design descriptor — visual concept / stance / look / era / set.
    design: dict[str, Any] = field(default_factory=dict)
    #: The Casting Director's cast — the production's Characters (the cast axis).
    cast: list["Character"] = field(default_factory=list)
