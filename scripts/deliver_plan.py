"""Run the plan phase and file its two dailies deliverables (storyline 0036/0048).

The plan-phase analogue of ``produce.py``: reconcile a :class:`~sequitur.plan.Plan`
from a scene brief, then produce the two Producer-reviewable deliverables — a
**treatment** (from the story descriptor) and a **poster** (the design concept rendered
as one evocative frame via ``ImageStudio``) — and file them through a
:class:`~sequitur.gate.Gate` for review.

Examples
--------
Offline preview — compose and print the treatment + poster prompt, no render, no store::

    python scripts/deliver_plan.py "a heist in a rain-soaked city" --mood "cold, tense" \
        --supergenre CRIME --concept "the city as a rain-streaked maze" --dry-run

Full run — render the poster and file both deliverables into the output store::

    python scripts/deliver_plan.py "a lighthouse keeper's last night" --production Lighthouse
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make the `sequitur` package importable when run as a bare script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import Brief, Director, Engine, Screenwriter, build_poster_prompt  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run the plan phase: reconcile a Plan, produce a treatment + poster, file them at a gate."
    )
    p.add_argument("scene", help="The scene / premise to plan.")
    p.add_argument("--mood", help="Mood for the plan (carries into the poster).")
    p.add_argument("--supergenre", help="A story supergenre hint (e.g. CRIME, HORROR, LIFE).")
    p.add_argument("--concept", help="A visual-concept hint — the poster's central image.")
    p.add_argument("--treatment", metavar="PATH", help="A persona-authored treatment file (the Screenwriter B agent's narration); overrides the tier-A skeleton.")
    p.add_argument("--production", default="Untitled", help="The production name (the output-store key). Default: Untitled.")
    p.add_argument("--store", metavar="PATH", help="Output-store root; defaults to OUTPUT_STORE_ROOT in .env.")
    p.add_argument("--report", action="store_true", help="Stream each deliverable to the board as it lands (report-after-each; board writes are non-fatal).")
    p.add_argument("--board", metavar="PATH", help="Report into a local JSON board double instead of ADO (implies --report).")
    p.add_argument("--dry-run", action="store_true", help="Compose and print the treatment + poster prompt only — no render, no store.")
    return p.parse_args(argv)


def _brief(args: argparse.Namespace) -> Brief:
    hints: dict = {}
    if args.supergenre:
        from sequitur import Supergenre

        hints["supergenre"] = Supergenre[args.supergenre.upper()]
    if args.concept:
        hints["visual_concept"] = args.concept
    return Brief(scene=args.scene, mood=args.mood, hints=hints)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    plan = Engine().plan(_brief(args))

    # The Screenwriter persona (B) narrates the real treatment; the tier-A skeleton is the offline fallback.
    treatment_text = Path(args.treatment).read_text(encoding="utf-8") if args.treatment else None

    if args.dry_run:
        print(treatment_text if treatment_text is not None else Screenwriter().treatment(plan))
        print("\n--- poster prompt ---")
        print(build_poster_prompt(plan))
        return 0

    from sequitur import Gate

    if args.store:
        from sequitur import LocalFolderOutputStore

        store = LocalFolderOutputStore(args.store)  # explicit local root
    else:
        from sequitur.config import get_output_store

        store = get_output_store()  # configured backend (Graph share links when selected)
    gate = Gate(store, production=args.production)
    treatment, poster = Director().deliver_plan(plan, gate=gate, treatment=treatment_text)

    # Report-after-each policy: the store is the durable log; a board write streams the
    # deliverable the instant it lands and is NON-FATAL — if it fails, the artifact is
    # already in the store and a later `report_to_board.py --phase plan` reconciles it.
    provider = _provider(args)
    routed = (
        _route(treatment, "Screenwriter", "Story"),
        _route(poster, "Production Designer", "Art"),
    )

    print(f"Filed plan deliverables for '{args.production}':")
    for deliverable in routed:
        print(f"  [{deliverable.status.value:>8}] {deliverable.name:<14} -> {deliverable.ref}")
        _report(provider, deliverable)
    return 0


def _provider(args: argparse.Namespace):
    """The board to stream to, or None when reporting is off."""
    if not (args.report or args.board):
        return None
    if args.board:
        from sequitur import LocalFolderProduction

        return LocalFolderProduction(args.board)
    from sequitur import AzureDevOpsProduction

    return AzureDevOpsProduction(project=args.production)


def _route(deliverable, author: str, department: str):
    """Attach the authoring seat + department so the board files it in the right place."""
    from dataclasses import replace

    return replace(deliverable, author=author, department=department)


def _report(provider, deliverable) -> None:
    """Stream one deliverable to the board — non-fatal; the store remains the source of truth."""
    if provider is None:
        return
    body = None
    if str(deliverable.name).lower().endswith((".md", ".txt")):
        try:
            body = Path(str(deliverable.ref)).read_text(encoding="utf-8")
        except OSError:
            body = None
    try:
        wid = provider.report(deliverable, body=body)
        print(f"    -> board {wid}")
    except Exception as exc:  # noqa: BLE001 - board write is non-fatal by policy
        print(f"    ! board write failed ({type(exc).__name__}): left in store to reconcile")


if __name__ == "__main__":
    raise SystemExit(main())
