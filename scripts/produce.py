"""Run a production **board-to-board** — the CLI for ``Engine.run_production`` (storyline 0027).

Reads a :class:`~sequitur.crew.role.Brief` from a production board, lets the crew
assemble a graded edit :class:`~sequitur.edit.Sequence`, writes the result back, and
prints the assembled timeline. The board is the ADO production by default (pointers in
``.env``), or a local-folder production for a quick offline run.

Examples
--------
Run against the configured Azure DevOps board::

    python scripts/produce.py

Against a local-folder production (a JSON file), no network::

    python scripts/produce.py --local production.json

Preview only — assemble and print, but do not write the Sequence back::

    python scripts/produce.py --no-write
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make the `sequitur` package importable when run as a bare script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import Engine  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run a production board-to-board: read a Brief, assemble a graded edit, write it back."
    )
    p.add_argument("--local", metavar="PATH", help="Use a local-folder production (JSON) instead of the ADO board.")
    p.add_argument("--scene", help="Scene label for the assembled Brief.")
    p.add_argument("--no-write", action="store_true", help="Assemble and print, but do not write the Sequence back.")
    return p.parse_args(argv)


def _provider(args: argparse.Namespace):
    """Build the production backend — a local folder, or the configured ADO board."""
    if args.local:
        from sequitur import LocalFolderProduction

        return LocalFolderProduction(args.local)
    from sequitur import AzureDevOpsProduction  # imported late so --local needs no creds

    return AzureDevOpsProduction()


def _print_sequence(sequence) -> None:
    timeline = sequence.timeline()
    if not timeline:
        print("  (no coverage on the board)")
        return
    print(f"  {'#':>2}  {'transition':<10} {'grade':<12} {'dur':>5}  shot")
    for i, entry in enumerate(timeline, 1):
        look = entry.clip.grade.name if entry.clip.grade else "-"
        transition = entry.edit_in.transition.name.lower()
        print(f"  {i:>2}  {transition:<10} {look:<12} {entry.clip.duration:>4.1f}s  {entry.clip.shot.scene}")
    print(f"\n  runtime: {sequence.runtime:.1f}s across {len(timeline)} shot(s)")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    provider = _provider(args)
    engine = Engine()

    if args.no_write:
        brief = provider.read_brief(scene=args.scene)
        sequence = engine.assemble(brief)
        print(f"Assembled '{brief.scene or '(untitled)'}' from the board (not written back):")
    else:
        sequence = engine.run_production(provider, scene=args.scene)
        print("Ran production board-to-board (Sequence written back):")

    _print_sequence(sequence)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
