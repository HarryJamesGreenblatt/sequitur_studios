# Grammar of the Edit — grounding index

Christopher J. Bowen, *Grammar of the Edit* (4th ed.), DOI
`10.4324/9781003257349`. This is the studio's **post-production / editorial**
grounding: how to assess coverage, decide *when and why* to cut, choose
transitions, and assemble shots into scenes. It is the companion to
[*Grammar of the Shot*](../grammar%20of%20the%20shot/INDEX.md) and the source that
the studio's **planned post-production layer** (`movie.py`) will be derived from.

> **No code layer exists yet.** Unlike the shot layer — which was retrofitted onto
> a pre-existing `grammar.py` — the editorial capabilities open a **new
> architectural surface** (the post phase). The "code layer" column below therefore
> points at the *intended* `movie.py` / sequence layer, and every reference's
> **Studio application** section is a **provisional lead** to be reconciled once
> that analogue is designed.

## Folder layout

- [`extraction/`](extraction/) — the raw `.docx` originals + `media/` (as imported).
- [`source/`](source/) — pandoc-converted verbatim Markdown, the **ground truth**.
- [`reference/`](reference/) — abridged, session-ready references (what agents load).

## Chapter → (planned) code map

| Chapter | Covers | Planned post-layer concern |
|---------|--------|----------------------------|
| [Ch. 1 — The Editing Process](reference/ch01-the-editing-process.md) | what editing is, factors, the staged workflow, four transitions | the pipeline as `movie.py` agent workflow (ingest→organize→assemble→refine) |
| [Ch. 2 — Visual Material](reference/ch02-visual-material.md) | shot vocabulary editorially; simple/complex/developing | coverage as input; clip tagging; cuttability |
| [Ch. 3 — Audio Material](reference/ch03-audio-material.md) | production vs post sound; diegetic/non-diegetic; sync | **production-dialogue vs post-soundtrack** phase split |
| [Ch. 4 — Assessing Footage](reference/ch04-assessing-footage.md) | quality checklist; continuity rules; master-scene order | shot-selection scoring; "can these cut together?"; assembly template |
| [Ch. 5 — When to Cut and Why](reference/ch05-when-to-cut.md) | the six motivators; sound bridge; pace/rhythm | the **cut-decision engine** (cut-to-cue) |
| [Ch. 6 — Transitions & Edit Categories](reference/ch06-transitions-and-edit-categories.md) | cut/dissolve/wipe/fade; handles; 5 edit types | atomic transition ops; **handle padding** on generated shots |
| [Ch. 7 — Terms & Techniques](reference/ch07-terms-and-techniques.md) | timecode, montage, multicam, L/J-cuts, stills, grading | audio-offset primitives; time-aligned coverage; stills-as-clips |
| [Ch. 8 — Editor's Mindset](reference/ch08-editors-mindset.md) | the durable principles, synthesized | the assembler's **design charter** |

## Scope note

Grammar of the Edit grounds the **editorial/post-production phase** — the layer
after [*Grammar of the Shot*](../grammar%20of%20the%20shot/INDEX.md)'s production
grammar. Its Ch. 4–5 overlap Grammar of the Shot's Ch. 5 (shooting-for-the-edit):
the shot layer *prepares* for the cut, the edit layer *makes* it. Together they
frame the studio's **shots → scenes → acts** hierarchy and the open **cut-to-cue**
and **production-dialogue** problems recorded in
[`../../context/architecture.md`](../../context/architecture.md).
