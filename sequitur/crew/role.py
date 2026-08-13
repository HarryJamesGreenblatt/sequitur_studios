"""The crew seat — the abstract :class:`Role` base and the axes that place it.

A :class:`Role` is a *chooser*: the department member that owns and wields a slice
of the studio's grammar. Roles are grouped by :class:`Department` and activated by
:class:`Phase` (which crew is on call — plan · shoot · assemble · ship). A role
holds a swappable :class:`~sequitur.crew.judgment.Judgment` (heuristic **A** /
persona **B** / human) and turns a :class:`Brief` into a :class:`Contribution` —
its proposed slice of the decision. The :class:`~sequitur.crew.director.Director`
reconciles the crew's contributions; the :class:`~sequitur.crew.engine.Engine`
dispatches them (storyline 0008).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from ..shot import Shot
    from .judgment import Judgment


class Phase(Enum):
    """A production phase — which crew is on call."""

    PLAN = "plan"
    SHOOT = "shoot"
    ASSEMBLE = "assemble"
    SHIP = "ship"


class Department(Enum):
    """A crew department — the group a role belongs to (Appendix D)."""

    CAMERA = "camera"
    ELECTRIC = "electric"
    GRIP = "grip"
    EDITORIAL = "editorial"
    SOUND = "sound"
    COLOR = "color"
    DIRECTION = "direction"


@dataclass
class Brief:
    """The producer's context for a decision: what to make, plus optional nudges.

    ``hints`` maps a :class:`~sequitur.shot.Shot` field name to a chosen value
    (usually a grammar enum member) — the producer overriding a role's default.
    ``scene``/``mood``/``audio`` pass straight through to the assembled shot.
    """

    scene: str
    hints: dict[str, Any] = field(default_factory=dict)
    mood: str | None = None
    audio: str | None = None
    aspect_ratio: str = "16:9"
    #: The coverage to assemble — populated for the assemble phase, empty for shoot.
    shots: list["Shot"] = field(default_factory=list)


@dataclass
class Contribution:
    """One role's proposed slice of a decision — the fields it chose to fill."""

    role: str
    fields: dict[str, Any] = field(default_factory=dict)
    notes: str = ""


class Role:
    """A crew member: the chooser that owns and wields a slice of the grammar.

    Subclasses set :attr:`title`, :attr:`department`, and :attr:`phase`, and list
    the closed vocabulary (Grammar enum types) they own in :attr:`vocabulary`. A
    role delegates *how* it reasons to a swappable :class:`~sequitur.crew.judgment.Judgment`
    (heuristic **A** / persona **B** / human); :meth:`heuristic` is the role's own
    deterministic default (the **A** the default judgment uses).
    """

    title: ClassVar[str] = "Role"
    department: ClassVar[Department]
    phase: ClassVar[Phase]
    #: The closed vocabulary this role owns — the Grammar enums it wields.
    vocabulary: ClassVar[tuple[type[Enum], ...]] = ()

    def __init__(self, judgment: Judgment | None = None) -> None:
        if judgment is None:
            from .judgment import HeuristicJudgment

            judgment = HeuristicJudgment()
        self.judgment = judgment

    def propose(self, brief: Brief) -> Contribution:
        """Propose this role's slice of the decision, via its :attr:`judgment`."""
        return self.judgment.decide(self, brief)

    def heuristic(self, brief: Brief) -> dict[str, Any]:
        """The role's deterministic default choices — the **A** in the A->B seam.

        Base roles contribute nothing; department roles override to choose their
        owned fields (reading :attr:`Brief.hints` for producer overrides). A
        ``PersonaJudgment`` (**B**) ignores this and reasons with an LLM instead.
        """
        return {}

    def __repr__(self) -> str:
        dept = getattr(type(self), "department", None)
        phase = getattr(type(self), "phase", None)
        return (
            f"<{type(self).__name__}"
            f"{f' · {dept.value}' if dept else ''}"
            f"{f' · {phase.value}' if phase else ''}>"
        )
