"""The engine — dumb dispatch over a crew (storyline 0008).

The engine holds no film logic. It filters the crew by the active :class:`Phase`,
collects each role's :class:`Contribution`, and hands them to the
:class:`~sequitur.crew.director.Director` to reconcile. Behaviour lives in the
roles; reconciliation in the Director; the engine only routes. It can take a
:class:`Brief` directly, or read one from — and write the result back to — a
:class:`~sequitur.production.ProductionProvider` (the production board), which is
the per-instance *Production* binding storyline 0005 anticipated (0025 / 0026).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .director import Director
from .role import Phase, Role

if TYPE_CHECKING:
    from ..edit import Sequence
    from ..production import ProductionProvider
    from ..shot import Shot
    from .role import Brief


def shoot_crew() -> list[Role]:
    """The default production crew: Cinematographer, Gaffer, Key Grip."""
    from .camera import Cinematographer
    from .grip import KeyGrip
    from .lighting import Gaffer

    return [Cinematographer(), Gaffer(), KeyGrip()]


def plan_crew() -> list[Role]:
    """The plan-phase crew: the Screenwriter (story descriptor) + Production Designer (design descriptor).

    Not part of :func:`full_crew` yet — each seat's :class:`Contribution` is a
    *descriptor* (a story classification / a design overlay), not a
    :class:`~sequitur.shot.Shot`, so the plan phase needs its own reconcile (a later
    pass) before the :class:`Engine` can dispatch it like the shoot and assemble crews.
    """
    from .production_design import ProductionDesigner
    from .screenwriting import Screenwriter

    return [Screenwriter(), ProductionDesigner()]


def assemble_crew() -> list[Role]:
    """The post crew: Editor (cut) and Colorist (grade)."""
    from .colorist import Colorist
    from .editorial import Editor

    return [Editor(), Colorist()]


def full_crew() -> list[Role]:
    """The whole crew across phases — the Engine's default mount."""
    return shoot_crew() + assemble_crew()


class Engine:
    """Mounts a crew and runs the active phase's roles, then reconciles."""

    def __init__(self, crew: list[Role] | None = None, director: Director | None = None) -> None:
        self.crew = list(crew) if crew is not None else full_crew()
        self.director = director or Director()

    def run(self, phase: Phase, brief: Brief) -> Shot:
        """Dispatch the phase's crew and reconcile their contributions into a Shot."""
        active = [r for r in self.crew if getattr(r, "phase", None) == phase]
        contributions = [role.propose(brief) for role in active]
        return self.director.reconcile(brief, contributions)

    def assemble(self, brief: Brief) -> Sequence:
        """Dispatch the assemble-phase crew and reconcile a graded edit Sequence."""
        active = [r for r in self.crew if getattr(r, "phase", None) == Phase.ASSEMBLE]
        contributions = [role.propose(brief) for role in active]
        return self.director.assemble(brief, contributions)

    def run_production(self, provider: ProductionProvider, *, scene: str | None = None) -> Sequence:
        """Run a production **board-to-board**: read a Brief, assemble, write it back.

        Binds the assemble phase to a
        :class:`~sequitur.production.ProductionProvider` (storyline 0025 / 0026): the
        crew reads its coverage from the production board, assembles a graded edit
        :class:`~sequitur.edit.Sequence`, and records the result back onto the board.
        The provider is duck-typed (a ``runtime_checkable`` Protocol), so the engine
        needs no import of the concrete backend — the same swappability the
        :class:`~sequitur.render.Renderer` seam gives the execution plane.
        """
        brief = provider.read_brief(scene=scene)
        sequence = self.assemble(brief)
        provider.write_sequence(sequence)
        return sequence
