"""The engine — dumb dispatch over a crew (storyline 0008).

The engine holds no film logic. It filters the crew by the active :class:`Phase`,
collects each role's :class:`Contribution`, and hands them to the
:class:`~sequitur.crew.director.Director` to reconcile. Behaviour lives in the
roles; reconciliation in the Director; the engine only routes. (The per-instance
*Production* that will bind role state to this driver — storyline 0005 — is not
wired yet; ``run`` takes a :class:`Brief` directly for now.)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .director import Director
from .role import Phase, Role

if TYPE_CHECKING:
    from ..shot import Shot
    from .role import Brief


def shoot_crew() -> list[Role]:
    """The default production crew: Cinematographer, Gaffer, Key Grip."""
    from .camera import Cinematographer
    from .grip import KeyGrip
    from .lighting import Gaffer

    return [Cinematographer(), Gaffer(), KeyGrip()]


class Engine:
    """Mounts a crew and runs the active phase's roles, then reconciles."""

    def __init__(self, crew: list[Role] | None = None, director: Director | None = None) -> None:
        self.crew = list(crew) if crew is not None else shoot_crew()
        self.director = director or Director()

    def run(self, phase: Phase, brief: Brief) -> Shot:
        """Dispatch the phase's crew and reconcile their contributions into a Shot."""
        active = [r for r in self.crew if getattr(r, "phase", None) == phase]
        contributions = [role.propose(brief) for role in active]
        return self.director.reconcile(brief, contributions)
