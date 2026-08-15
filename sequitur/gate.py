"""The gate — a phase's Producer-reviewable deliverable and its verdict (storyline 0036).

The dailies model makes the studio *interactive and phase-gated*: each phase emits a
**deliverable** (a treatment, a poster, a board, dailies, a cut) that the Producer
reviews at a **gate** — approve to advance, or send back to revise *that phase only*,
before spend flows downstream. This module is the small code model of that ritual:

* :class:`Deliverable` — an artifact produced for review: which ``production`` and
  :class:`~sequitur.crew.role.Phase` it belongs to, a durable ``ref`` (the location
  the :class:`~sequitur.output.OutputStore` filed its bytes at — storyline 0038), and
  the Producer's :class:`GateStatus`. It is **immutable**: :meth:`Deliverable.approve`
  and :meth:`Deliverable.revise` return a *new* record, so a deliverable's history is
  a chain of versions, not a mutated cell.
* :class:`Gate` — bound to one ``production`` and an :class:`~sequitur.output.OutputStore`,
  it :meth:`~Gate.submit`\\ s an artifact: files it durably under its phase and returns a
  **pending** :class:`Deliverable` ready to present to the Producer.

The gate's *live* experience is the conversational Director agent presenting the
deliverable in chat; the durable record (linking the ``ref`` onto the board and moving
the phase's State) rides the :class:`~sequitur.production.ProductionProvider` — a next
step. This module is the tier-agnostic core both share.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from .crew.role import Phase

if TYPE_CHECKING:
    from .output import OutputStore


class GateStatus(Enum):
    """A deliverable's standing at its gate — the Producer's verdict."""

    PENDING = "pending"  # produced, awaiting the Producer's review
    APPROVED = "approved"  # the Producer accepted it; the phase may advance
    REVISE = "revise"  # sent back to be re-run, optionally with notes


@dataclass(frozen=True)
class Deliverable:
    """A phase's reviewable output — the unit a Producer approves at a gate.

    ``ref`` is the durable :class:`~sequitur.output.OutputStore` location of the
    artifact's bytes (a local :class:`~pathlib.Path` today, a share URL later). The
    record is immutable; :meth:`approve` and :meth:`revise` return new versions.
    """

    production: str
    phase: Phase
    name: str
    ref: Path | str
    status: GateStatus = GateStatus.PENDING
    notes: str | None = None

    def approve(self) -> "Deliverable":
        """Return an approved copy — the Producer accepted it; the phase may advance."""
        return replace(self, status=GateStatus.APPROVED, notes=None)

    def revise(self, notes: str | None = None) -> "Deliverable":
        """Return a revise copy carrying the Producer's notes — re-run this phase."""
        return replace(self, status=GateStatus.REVISE, notes=notes)


class Gate:
    """A phase review checkpoint for one production (storyline 0036).

    Binds a production to an :class:`~sequitur.output.OutputStore`; :meth:`submit`
    files an artifact durably under its phase and returns a *pending*
    :class:`Deliverable` — the thing the Director agent presents to the Producer.
    """

    def __init__(self, store: OutputStore, production: str) -> None:
        self.store = store
        self.production = production

    def submit(self, artifact: bytes | str | Path, *, phase: Phase, name: str | None = None) -> Deliverable:
        """File an artifact durably and return a pending :class:`Deliverable`.

        ``artifact`` is raw ``bytes`` or a path to a produced file (a rendered shot,
        a poster image, an encoded treatment) — the store's contract. The phase maps
        to the store's ``layer`` (``phase.value``), so a production's deliverables sit
        under ``<production>/<phase>/`` in the store.
        """
        ref = self.store.put(artifact, production=self.production, layer=phase.value, name=name)
        return Deliverable(
            production=self.production,
            phase=phase,
            name=Path(ref).name,
            ref=ref,
            status=GateStatus.PENDING,
        )
