"""The crew — roles as first-class code.

Where the studio's *grammar* is the closed vocabulary of choices (typed enums),
a **role** is the *chooser* that owns and wields a slice of that vocabulary. This
package re-seats the vocabulary that used to live flat in ``grammar.py`` (a
*flattened crew* — camera, electric, and grip fused into one module) under the
department roles that actually own it, per storyline 0008.

Beyond ownership, a role turns a :class:`Brief` into a :class:`Contribution` via a
swappable :class:`Judgment` (heuristic **A** now; persona **B** / human later); the
:class:`Director` reconciles the crew's contributions and the :class:`Engine`
dispatches them.
"""

from __future__ import annotations

from .director import Director
from .engine import Engine, assemble_crew, full_crew, plan_crew, shoot_crew
from .judgment import HeuristicJudgment, Judgment
from .role import Brief, Contribution, Department, Phase, Role

__all__ = [
    "Role",
    "Department",
    "Phase",
    "Brief",
    "Contribution",
    "Judgment",
    "HeuristicJudgment",
    "Director",
    "Engine",
    "shoot_crew",
    "plan_crew",
    "assemble_crew",
    "full_crew",
]
