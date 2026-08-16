"""The KeyArtist skill's executable arm — compose a theatrical one-sheet and render it.

The KeyArtist is a *generalist-under-direction* seat (storyline 0048): it owns no
grounded source and no `crew/` enum vocabulary. Its judgement lives in
[`SKILL.md`](SKILL.md) (tier B); this script is the deterministic arm it directs —
it composes the one-sheet prompt via `sequitur.prompt.build_key_art_prompt`, renders
it through `ImageStudio`, and (optionally) files it through a `Gate` as a plan-phase
`Deliverable`.

Inputs are *inherited from parents*: the `--concept`/`--look`/`--motifs` come from the
Production Designer's design descriptor; the `--title`/`--tagline` are the story's
marketing copy. The skill fills these from the upstream seats before invoking.

Usage (offline compose preview):
    python .github/skills/keyartist/compose_key_art.py --concept "..." --title "..." --tagline "..." --dry-run

Live render (needs `az login`; writes under output/, gitignored):
    python .github/skills/keyartist/compose_key_art.py --concept "..." --title "..." --out output/verification/keyart/onesheet.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Compose + render a theatrical one-sheet (key art).")
    p.add_argument("--concept", required=True, help="the central image (from the PD's visual_concept)")
    p.add_argument("--title", required=True, help="the film title (story marketing copy)")
    p.add_argument("--tagline", default=None, help="a short tagline (story marketing copy)")
    p.add_argument("--motif", action="append", default=[], dest="motifs", help="a recurring motif (repeatable)")
    p.add_argument("--look", default=None, help="look tokens, e.g. 'a film look, moody chiaroscuro'")
    p.add_argument("--archetype", default=None, help="the poster archetype the KeyArtist chose")
    p.add_argument("--mood", default=None, help="the emotional register")
    p.add_argument("--billing", action="store_true", help="request a billing block (garbles — off by default)")
    p.add_argument("--aspect", default="9:16", help="aspect ratio (default 9:16 portrait one-sheet)")
    p.add_argument("--out", default=None, help="output path for the rendered one-sheet")
    p.add_argument("--production", default=None, help="if set with --store, file the one-sheet via a Gate")
    p.add_argument("--store", default=None, help="an OutputStore root to file the deliverable durably")
    p.add_argument("--dry-run", action="store_true", help="compose + print the prompt, no API call")
    return p.parse_args()


def main() -> None:
    import sys

    sys.path.insert(0, str(_REPO_ROOT))
    from sequitur import ImageStudio, build_key_art_prompt

    args = _parse_args()
    prompt = build_key_art_prompt(
        args.concept,
        title=args.title,
        tagline=args.tagline,
        motifs=args.motifs,
        look=args.look,
        archetype=args.archetype,
        billing=args.billing,
        mood=args.mood,
    )
    print("=== ONE-SHEET PROMPT ===\n")
    print(prompt)
    if args.dry_run:
        print("\n(dry run — no render)")
        return

    out = Path(args.out) if args.out else _REPO_ROOT / "output" / "verification" / "keyart" / "onesheet.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    result = ImageStudio().render(prompt, aspect_ratio=args.aspect, out_path=out)
    ref = result.ref

    if args.store and args.production:
        from sequitur import Gate, LocalFolderOutputStore
        from sequitur.crew.role import Phase

        gate = Gate(LocalFolderOutputStore(Path(args.store)), production=args.production)
        deliverable = gate.submit(ref, phase=Phase.PLAN, name="key_art.png")
        print(f"\nfiled: {deliverable.status.value}  {deliverable.ref}")
    else:
        print(f"\nrendered: {ref}")


if __name__ == "__main__":
    main()
