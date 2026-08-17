"""Run the casting audition (storyline 0055) — the plan-phase casting arm.

The companion to [`deliver_plan.py`](deliver_plan.py): where that produces the plan's
treatment + poster, this produces the **cast**. It reads a cast spec (the Casting
Director's designed characters + candidate looks), renders the **audition** — each
candidate's look as a still keyframe via ``ImageStudio`` — files each at a
:class:`~sequitur.gate.Gate` for the Producer to review, and locks each candidate's
reference. A second invocation with ``--select`` binds the Producer's chosen embodiment
per character (the verdict), locking its reference for downstream conditioning.

The judgment (which characters, which candidate looks) is the Casting Director
subagent's; this arm is the deterministic executor it directs — the same
judgment/execution split every seat uses.

Cast spec JSON (a list of characters, each with candidate looks)::

    [
      {"name": "Mara", "role": "protagonist", "billing": "PRINCIPAL",
       "age_band": "CHILD", "essence": "lonely, luminous curiosity",
       "build": "small", "wardrobe": "a hand-me-down cardigan",
       "candidates": [{"look": "..."}, {"look": "..."}]}
    ]

Examples
--------
Dry run — list the audition (characters + candidate prompts), no render, no store::

    python scripts/audition.py TheAudition --cast cast.json --dry-run

Run the audition — render candidates, file them at the gate, write the state::

    python scripts/audition.py TheAudition --cast cast.json

Select — bind the Producer's chosen candidate (1-based) per character::

    python scripts/audition.py TheAudition --select "Mara=2" --select "Sol=1"
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

# Make the `sequitur` package importable when run as a bare script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Casting audition: render candidate looks, file them at a gate, then select the cast."
    )
    p.add_argument("production", help="The production name (the output-store / board key).")
    p.add_argument("--cast", metavar="PATH", help="Cast spec JSON (characters + candidate looks). Required to audition.")
    p.add_argument("--store", metavar="PATH", help="Output-store root (local). Default: the configured store (OUTPUT_STORE_BACKEND).")
    p.add_argument("--state", metavar="PATH", help="Audition state JSON to write/read. Default: <production>_cast.json.")
    p.add_argument("--report", action="store_true", help="Stream each candidate to the board as it lands (report-after-each; board writes are non-fatal).")
    p.add_argument("--board", metavar="PATH", help="Report into a local JSON board double instead of ADO (implies --report).")
    p.add_argument(
        "--select", action="append", default=[], metavar="NAME=IDX",
        help="Bind the Producer's chosen candidate (1-based) for a character. Repeatable.",
    )
    p.add_argument("--dry-run", action="store_true", help="List the audition (characters + candidate prompts) — no render, no store.")
    return p.parse_args(argv)


def _characters_from_spec(spec: list[dict]):
    """Build :class:`~sequitur.cast.Character` objects (with candidates) from the spec."""
    from sequitur import Actor, AgeBand, Billing, Character

    characters = []
    for c in spec:
        candidates = [
            Actor(
                look=a.get("look", ""),
                reference=a.get("reference"),
                voice=a.get("voice"),
                notes=a.get("notes", ""),
            )
            for a in c.get("candidates", [])
        ]
        character = Character(
            name=c["name"],
            billing=Billing[c.get("billing", "PRINCIPAL").upper()],
            age_band=AgeBand[c.get("age_band", "ADULT").upper()],
            role=c.get("role", ""),
            essence=c.get("essence", ""),
            build=c.get("build", ""),
            wardrobe=c.get("wardrobe", ""),
            candidates=candidates,
        )
        cast_idx = c.get("cast")
        if isinstance(cast_idx, int) and 0 <= cast_idx < len(candidates):
            character.cast = candidates[cast_idx]
        characters.append(character)
    return characters


def _spec_from_characters(characters) -> list[dict]:
    """Serialise characters back to a spec, capturing each candidate's locked reference."""
    out: list[dict] = []
    for ch in characters:
        entry = {
            "name": ch.name,
            "billing": ch.billing.name,
            "age_band": ch.age_band.name,
            "role": ch.role,
            "essence": ch.essence,
            "build": ch.build,
            "wardrobe": ch.wardrobe,
            "candidates": [
                {"look": a.look, "reference": a.reference, "voice": a.voice, "notes": a.notes}
                for a in ch.candidates
            ],
        }
        if ch.cast is not None and ch.cast in ch.candidates:
            entry["cast"] = ch.candidates.index(ch.cast)
        out.append(entry)
    return out


def _store(args: argparse.Namespace):
    if args.store:
        from sequitur import LocalFolderOutputStore

        return LocalFolderOutputStore(args.store)
    from sequitur.config import get_output_store

    return get_output_store()


def _provider(args: argparse.Namespace):
    """The board to stream candidates to, or None when reporting is off."""
    if not (args.report or args.board):
        return None
    if args.board:
        from sequitur import LocalFolderProduction

        return LocalFolderProduction(args.board)
    from sequitur import AzureDevOpsProduction

    return AzureDevOpsProduction(project=args.production)


def _report(provider, deliverable, *, author: str, department: str) -> None:
    """Stream one candidate to the board — non-fatal; the store stays the source of truth."""
    if provider is None:
        return
    from dataclasses import replace

    routed = replace(deliverable, author=author, department=department)
    try:
        wid = provider.report(routed)
        print(f"    -> board {wid}")
    except Exception as exc:  # noqa: BLE001 - board write is non-fatal by policy
        print(f"    ! board write failed ({type(exc).__name__}): left in store to reconcile")


def _run_audition(args: argparse.Namespace) -> int:
    from sequitur import Director, Gate, build_character_prompt

    if not args.cast:
        print("error: --cast is required to run an audition (or pass --select to bind a cast).")
        return 2

    spec = json.loads(Path(args.cast).read_text(encoding="utf-8"))
    characters = _characters_from_spec(spec)

    if args.dry_run:
        for ch in characters:
            print(f"[{ch.billing.name}] {ch.name} — {ch.role or 'role?'}")
            for i, actor in enumerate(ch.candidates, 1):
                print(f"  candidate {i}: {build_character_prompt(ch, actor)}")
        return 0

    gate = Gate(_store(args), production=args.production)
    provider = _provider(args)
    director = Director()
    with tempfile.TemporaryDirectory() as scratch:
        for ch in characters:
            deliverables = director.audition(ch, gate=gate, out_dir=scratch)
            print(f"{ch.name}: {len(deliverables)} candidate(s) auditioned")
            for i, d in enumerate(deliverables, 1):
                print(f"  candidate {i}: {d.ref}")
                # Report-after-each: stream the candidate to the board the instant it lands.
                # Non-fatal — the store holds the keyframe; a later report reconciles the board.
                _report(provider, d, author="Casting Director", department="Casting")

    state = args.state or f"{args.production}_cast.json"
    Path(state).write_text(json.dumps(_spec_from_characters(characters), indent=2), encoding="utf-8")
    print(f"\naudition state -> {state}   (review the candidates, then re-run with --select)")
    return 0


def _run_select(args: argparse.Namespace) -> int:
    state = args.state or f"{args.production}_cast.json"
    path = Path(state)
    if not path.exists():
        print(f"error: no audition state at {state} — run the audition first.")
        return 2

    characters = _characters_from_spec(json.loads(path.read_text(encoding="utf-8")))
    by_name = {ch.name: ch for ch in characters}
    for sel in args.select:
        name, _, idx = sel.partition("=")
        ch = by_name.get(name.strip())
        if ch is None:
            print(f"! no character named {name.strip()!r} in {state}")
            continue
        try:
            actor = ch.candidates[int(idx) - 1]  # 1-based for the Producer
        except (ValueError, IndexError):
            print(f"! bad candidate index {idx!r} for {name.strip()}")
            continue
        ch.select(actor)
        print(f"cast {ch.name} = candidate {idx.strip()}  ->  {actor.reference}")

    path.write_text(json.dumps(_spec_from_characters(characters), indent=2), encoding="utf-8")
    print(f"cast state -> {state}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.select:
        return _run_select(args)
    return _run_audition(args)


if __name__ == "__main__":
    raise SystemExit(main())
