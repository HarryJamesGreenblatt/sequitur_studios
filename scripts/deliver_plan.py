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
    p.add_argument("--production", default="Untitled", help="The production name (the output-store key). Default: Untitled.")
    p.add_argument("--store", metavar="PATH", help="Output-store root; defaults to OUTPUT_STORE_ROOT in .env.")
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

    if args.dry_run:
        print(Screenwriter().treatment(plan))
        print("\n--- poster prompt ---")
        print(build_poster_prompt(plan))
        return 0

    from sequitur import Gate, LocalFolderOutputStore

    store = LocalFolderOutputStore(args.store)  # None -> OUTPUT_STORE_ROOT from .env
    gate = Gate(store, production=args.production)
    treatment, poster = Director().deliver_plan(plan, gate=gate)

    print(f"Filed plan deliverables for '{args.production}':")
    for deliverable in (treatment, poster):
        print(f"  [{deliverable.status.value:>8}] {deliverable.name:<14} -> {deliverable.ref}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
