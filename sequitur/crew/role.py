"""The crew seat — the abstract :class:`Role` base and the axes that place it.

A :class:`Role` is a *chooser*: the department member that owns and wields a slice
of the studio's grammar. Roles are grouped by :class:`Department` and activated by
:class:`Phase` (which crew is on call — plan · shoot · assemble · ship). This base
is deliberately thin: in the first crew pass a role only *declares* what it owns.
The reasoning that turns owned vocabulary into choices (a swappable ``Judgment``)
and the ``Director`` that reconciles the crew are the next layer (storyline 0008).
"""

from __future__ import annotations

from enum import Enum
from typing import ClassVar


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


class Role:
    """A crew member: the chooser that owns and wields a slice of the grammar.

    Subclasses set :attr:`title`, :attr:`department`, and :attr:`phase`, and list
    the closed vocabulary (Grammar enum types) they own in :attr:`vocabulary`.
    """

    title: ClassVar[str] = "Role"
    department: ClassVar[Department]
    phase: ClassVar[Phase]
    #: The closed vocabulary this role owns — the Grammar enums it wields.
    vocabulary: ClassVar[tuple[type[Enum], ...]] = ()

    def __repr__(self) -> str:
        dept = getattr(type(self), "department", None)
        phase = getattr(type(self), "phase", None)
        return (
            f"<{type(self).__name__}"
            f"{f' · {dept.value}' if dept else ''}"
            f"{f' · {phase.value}' if phase else ''}>"
        )
