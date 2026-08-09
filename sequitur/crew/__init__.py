"""The crew — roles as first-class code.

Where the studio's *grammar* is the closed vocabulary of choices (typed enums),
a **role** is the *chooser* that owns and wields a slice of that vocabulary. This
package re-seats the vocabulary that used to live flat in ``grammar.py`` (a
*flattened crew* — camera, electric, and grip fused into one module) under the
department roles that actually own it, per storyline 0008.

This first pass establishes the seat and the ownership only: a role *declares*
its department, phase, and vocabulary. The reasoning layer (a swappable
``Judgment``) and the ``Director`` reconciler are the next step.
"""

from __future__ import annotations

from .role import Department, Phase, Role

__all__ = ["Role", "Department", "Phase"]
