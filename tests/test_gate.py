"""Smoke tests for the gate — a phase's Producer-reviewable deliverable and its verdict.

Exercises the ``Gate`` / ``Deliverable`` model offline against a ``LocalFolderOutputStore``
in a temp root (never the real OneDrive store): submitting files the artifact durably and
returns a pending deliverable; approve/revise are immutable transitions. Asserts against the
public package surface. Run directly (``python tests/test_gate.py``) or via pytest.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Deliverable,
    Gate,
    GateStatus,
    LocalFolderOutputStore,
    Phase,
)


def test_submit_files_the_artifact_and_returns_a_pending_deliverable() -> None:
    with tempfile.TemporaryDirectory() as d:
        gate = Gate(LocalFolderOutputStore(d), production="HeistNoir")
        deliverable = gate.submit(b"# treatment\n...", phase=Phase.PLAN, name="treatment.md")

        assert isinstance(deliverable, Deliverable)
        assert deliverable.production == "HeistNoir"
        assert deliverable.phase is Phase.PLAN
        assert deliverable.name == "treatment.md"
        assert deliverable.status is GateStatus.PENDING
        # The artifact was filed durably under <production>/<phase>/, and the bytes made it there.
        assert Path(deliverable.ref) == Path(d) / "HeistNoir" / "plan" / "treatment.md"
        assert Path(deliverable.ref).read_bytes() == b"# treatment\n..."


def test_approve_is_an_immutable_transition() -> None:
    with tempfile.TemporaryDirectory() as d:
        gate = Gate(LocalFolderOutputStore(d), production="P")
        pending = gate.submit(b"x", phase=Phase.PLAN, name="poster.png")
        approved = pending.approve()

    assert approved.status is GateStatus.APPROVED
    assert approved.notes is None
    # The original record is untouched — history is a chain, not a mutated cell.
    assert pending.status is GateStatus.PENDING
    assert approved.ref == pending.ref


def test_revise_carries_the_producer_notes() -> None:
    with tempfile.TemporaryDirectory() as d:
        gate = Gate(LocalFolderOutputStore(d), production="P")
        pending = gate.submit(b"x", phase=Phase.SHOOT, name="shot_001.png")
        revised = pending.revise("push in tighter on the reveal")

    assert revised.status is GateStatus.REVISE
    assert revised.notes == "push in tighter on the reveal"
    assert pending.status is GateStatus.PENDING


def test_submit_a_produced_path_defaults_the_name() -> None:
    with tempfile.TemporaryDirectory() as d:
        scratch = Path(d) / "render.mp4"
        scratch.write_bytes(b"daily")
        gate = Gate(LocalFolderOutputStore(Path(d) / "store"), production="P")
        deliverable = gate.submit(scratch, phase=Phase.SHOOT)

        # Name falls back to the source filename; the artifact is filed under the phase.
        assert deliverable.name == "render.mp4"
        assert Path(deliverable.ref) == Path(d) / "store" / "P" / "shoot" / "render.mp4"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all gate tests passed")
