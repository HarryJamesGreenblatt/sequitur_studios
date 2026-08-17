"""The Assistant Director / PA skill's executable arm — collect + report to the board.

The AD/PA is a *generalist-under-direction* coordination seat (storyline 0049): it owns
no grounded source and no `crew/` enum vocabulary. Its judgement lives in
[`SKILL.md`](SKILL.md) (tier B — what's ready, what to chase, what context to hand down);
this script is the deterministic **messenger arm** it directs — the Mediator that owns
the board I/O so the producing craft seats never touch ADO.

Two directions (the board-as-memory / RAG hub):
  * **report (up):** scan a production phase's deliverables in the OutputStore and file
    each onto the board via `ProductionProvider.report` (text -> Description, image ->
    attachment, gate verdict -> State). The Producer/Director review + approve there.
  * **verdict (down):** record the Producer's approve/revise on a reported deliverable
    via `ProductionProvider.record_verdict` — it advances the board item's State (approved
    -> Done, revise -> Doing, with the notes as a comment) without touching its content.
  * **fetch (down):** read prior board deliverables back so a later department gets the
    approved context (the treatment, the concept) as grounding.

Usage (report the plan deliverables of a production to its ADO board):
    python .github/skills/assistant_director/report_to_board.py --production TheLaunch --phase plan

Record a Producer verdict (the approvals loop):
    python .github/skills/assistant_director/report_to_board.py --production TheLaunch --phase plan --approve treatment.md
    python .github/skills/assistant_director/report_to_board.py --production TheLaunch --phase plan --revise poster.png --notes "warmer, show the protagonist"

Offline (file into a local JSON board double, no network):
    python .github/skills/assistant_director/report_to_board.py --production X --phase plan --local board.json

Read the board's memory back:
    python .github/skills/assistant_director/report_to_board.py --production TheLaunch --fetch
"""

from __future__ import annotations

import argparse
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]

# Deliverables whose bytes are text get their body embedded on the board (queryable RAG);
# everything else is filed as an attachment (image posters, etc.).
_TEXT_SUFFIXES = {".md", ".txt", ".json"}

# The AD's coordination knowledge: which seat produces which deliverable, and the board
# department (Area Path) it files under. Routing metadata, not creative content. The
# KeyArtist's outputs route to **Marketing** — the market-facing plane (key art / one-sheet
# is a campaign artifact, not production design), filed as a Marketing Asset (storyline 0052).
_ROUTING: dict[str, tuple[str, str]] = {
    "treatment.md": ("Screenwriter", "Story"),
    "copy.md": ("Screenwriter", "Story"),
    "concept.md": ("Production Designer", "Art"),
    "poster.png": ("Production Designer", "Art"),
    "key_art_directive.md": ("KeyArtist", "Marketing"),
    "key_art.png": ("KeyArtist", "Marketing"),
}


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AD/PA: collect a phase's deliverables and report them to the board.")
    p.add_argument("--production", required=True, help="the production (one ADO project = one production)")
    p.add_argument("--phase", default="plan", help="the phase whose deliverables to report (default plan)")
    p.add_argument("--store", default=None, help="OutputStore root (default: configured OUTPUT_STORE_ROOT)")
    p.add_argument("--local", default=None, help="report into a local JSON board double instead of ADO")
    p.add_argument("--fetch", action="store_true", help="read the board's deliverables back instead of reporting")
    p.add_argument("--approve", default=None, help="record a Producer APPROVE verdict for this deliverable name")
    p.add_argument("--revise", default=None, help="record a Producer REVISE verdict for this deliverable name")
    p.add_argument("--notes", default=None, help="revise notes, recorded with --revise")
    p.add_argument("--dry-run", action="store_true", help="list what would be reported, no board write")
    return p.parse_args()


def _provider(args):
    from sequitur import AzureDevOpsProduction, LocalFolderProduction

    if args.local:
        return LocalFolderProduction(args.local)
    return AzureDevOpsProduction(project=args.production)


def main() -> None:
    import sys

    sys.path.insert(0, str(_REPO_ROOT))
    from sequitur import Deliverable, GateStatus
    from sequitur.crew.role import Phase

    args = _parse_args()
    phase = Phase(args.phase)
    provider = _provider(args)

    if args.fetch:
        for d in provider.fetch_reports(phase=phase if not args.fetch else None):
            print(f"{d.status.value:8}  [{d.phase.value}]  {d.name}")
        return

    # Verdict (down): record the Producer's approve/revise on a reported deliverable.
    verdict_name = args.approve or args.revise
    if verdict_name:
        base = Deliverable(
            production=args.production, phase=phase, name=verdict_name, ref="",
            status=GateStatus.PENDING,
        )
        verdict = base.approve() if args.approve else base.revise(args.notes)
        if args.dry_run:
            print(f"would record {verdict.status.value}: [{phase.value}] {verdict_name}")
            return
        wid = provider.record_verdict(verdict)
        print(f"verdict {verdict.status.value}: [{phase.value}] {verdict_name}  ->  board item {wid}")
        return

    # Collect this phase's deliverables from the store: <root>/<production>/<phase>/*.
    if args.store:
        root = Path(args.store)
    else:
        from sequitur.config import get_output_store_root

        root = Path(get_output_store_root())
    phase_dir = root / args.production / phase.value
    if not phase_dir.is_dir():
        print(f"no deliverables at {phase_dir}")
        return

    for artifact in sorted(phase_dir.iterdir()):
        if not artifact.is_file():
            continue
        body = None
        if artifact.suffix.lower() in _TEXT_SUFFIXES:
            body = artifact.read_text(encoding="utf-8")
        author, department = _ROUTING.get(artifact.name, (None, None))
        deliverable = Deliverable(
            production=args.production,
            phase=phase,
            name=artifact.name,
            ref=str(artifact),
            status=GateStatus.PENDING,
            author=author,
            department=department,
        )
        if args.dry_run:
            kind = "text" if body is not None else "attachment"
            who = f"{author or '?'} / {department or '?'}"
            print(f"would report ({kind}): [{phase.value}] {artifact.name}  ({who})")
            continue
        wid = provider.report(deliverable, body=body)
        print(f"reported: [{phase.value}] {artifact.name}  ->  board item {wid}")


if __name__ == "__main__":
    main()
