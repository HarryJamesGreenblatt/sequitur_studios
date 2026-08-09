"""Judgment — the swappable strategy for *how* a role reasons (the A->B seam).

A :class:`~sequitur.crew.role.Role` never hard-codes its reasoning; it delegates to
a :class:`Judgment`. Three strategies share one ``decide`` signature so any single
role can be upgraded — or hand-driven — individually (storyline 0008):

- :class:`HeuristicJudgment` (**A**) — deterministic; uses the role's own
  ``heuristic`` default. Built first; no LLM.
- ``PersonaJudgment`` (**B**, later) — an LLM persona reasoning over the role's
  *scoped* grounding.
- ``HumanJudgment`` (HITL, later) — defers the choice to the producer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .role import Contribution

if TYPE_CHECKING:
    from .role import Brief, Role


class Judgment(ABC):
    """A strategy for turning a :class:`Brief` into a role's :class:`Contribution`."""

    @abstractmethod
    def decide(self, role: Role, brief: Brief) -> Contribution:
        """Choose this role's slice of the decision for ``brief``."""


class HeuristicJudgment(Judgment):
    """Deterministic **A**: use the role's own ``heuristic`` default choices."""

    def decide(self, role: Role, brief: Brief) -> Contribution:
        return Contribution(role=role.title, fields=role.heuristic(brief))
