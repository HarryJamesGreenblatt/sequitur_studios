# 0016 — Abridging the Screenwriter's Taxonomy

> Date: 2026-08-08 · Focus: run the first of the **designated abridgement sessions**
> deferred in `0015` — transform Eric R. Williams' *The Screenwriter's Taxonomy*
> (the smaller of the two staged plan-phase sources) from verbatim `source/` into
> **8 session-ready `reference/` chapters**, grounding a future `Screenwriter` role.
> A **grounding** entry (transformative references + doc reconciliation); no code.

## What happened

`0015` staged two long plan-phase sources (Directing + the Taxonomy) with verbatim
`source/` and a chapter→role *plan*, but deferred the heavy abridgement to dedicated
sessions to avoid blowing a single budget. This session executes that plan for the
**Taxonomy** (8 chapters — the smaller task).

1. **Read the source fully, chapter by chapter — no further pruning.** Per the user's
   direction, all 8 chapters were scanned in full and all 8 abridged; the curation was
   already made at staging, so nothing was dropped. (The same rule will apply to
   Directing.)

2. **Wrote 8 abridged [`reference/`](../../artifacts/the%20screenwriter's%20taxonomy/reference/)
   chapters**, matching the house idiom (title · blockquote scope · core idea ·
   sections · a closing **"Studio application"** tying each chapter to the code layer
   it grounds, with cross-links):
   - `ch01` The Need for a Road Map — the 7-layer model + road-trip metaphor.
   - `ch02` Movie Types and Supergenres — `MovieType` + the closed 11-value `Supergenre`.
   - `ch03` Macrogenres and Microgenres — large `Macrogenre` enum + open `Microgenre` tag.
   - `ch04` Genre Case Studies — one logline → three films; super-choice cascades.
   - `ch05` Voice — Voice as a *struct of ~6 axes*, the seam to the render grammar.
   - `ch06` Pathway — the closed ~20-value `Pathway` enum (7 divergence families).
   - `ch07` Point of View — three small enums (Scope × Focus × Stance); upstream of camera.
   - `ch08` Case Studies — the full six-layer descriptor *vector*; analytic + generative.

3. **Reconciled the living docs:** the taxonomy
   [`INDEX.md`](../../artifacts/the%20screenwriter's%20taxonomy/INDEX.md) (staged →
   abridged; per-chapter reference links), the catalog row in
   [`artifacts/INDEX.md`](../../artifacts/INDEX.md), and the Screenwriter row +
   reading-the-map note in [`architecture.md`](../architecture.md).

## Decisions

1. **Abridge the whole source, not just the "enum" chapters.** The `0015` plan flagged
   ch 2/3/5/6/7 as the vocabulary-bearing chapters; the user directed a **full scan
   with nothing dropped** — the selection was already made at staging. So the case-study
   chapters (4, 8) and the rationale (1) were abridged too; they carry the *cross-layer
   dependency* lessons (super → POV → coverage) that the enum chapters alone don't show.

2. **Model the taxonomy as a *layered descriptor vector*, not a flat tag.** The Studio
   applications converge on one design: `MovieType`/`Supergenre` = closed enums,
   `Macrogenre` = large enum (multiple allowed), `Microgenre` = open macro-scoped tag,
   `Voice` = a struct of ~6 orthogonal axes, `Pathway` = closed ~20-value enum, `POV` =
   three small enums (Scope×Focus×Stance). A future `crew/screenwriting.py`
   `Screenwriter` owns them — the same closed-enum discipline that made
   `crew/camera.py`.

3. **The taxonomy is the plan-phase *control surface* for the whole pipeline.** The
   references make the cross-layer links explicit rather than treating story as an
   isolated cell: **POV → camera coverage**, **Pathway → the edit `Sequence`**, **Voice
   (medium/dialogue) → the render backends + `SpeechRenderer`**, **Type/Super
   (atmosphere) → Production Design/DP**. A `Screenwriter` `Contribution` seeds the
   `Brief` the `Director` reconciles (`0014`).

## Resulting state

- The Taxonomy is now the library's **fourth abridged source** (three prior: Grammar of
  the Shot, Grammar of the Edit, Rose). `source/`+`extraction/` stay gitignored; the 8
  `reference/` chapters + INDEX ship. **Five sources total: four abridged, one staged
  (Directing).** No code.
- Overlap flags preserved for future encoding: **POV** (Taxonomy Ch. 7 ↔ Directing
  Ch. 9) and **Pathway/structure** (Taxonomy Ch. 6 ↔ Directing Ch. 5) — reconcile when
  the axes are encoded and when Directing is abridged.

## Open threads

- **Abridge Directing — the remaining designated session(s)** — start with the
  **Director** chapters (7–11, 17), since the role exists in code (`0014`); full scan,
  nothing dropped (same rule as this session).
- **Design the `Screenwriter` role** — `crew/screenwriting.py` with the typed
  genre/voice/pathway/POV vocabulary this abridgement grounds; wire its `Contribution`
  into the plan phase of the `Engine` ahead of the shoot crew.
- **Model the casting/actors dimension** (`0015`) — still open.
- Carried: crew-engine assemble-phase behaviour + Production binding (`0014`); the
  `Renderer` protocol (`0006`); the reconciliation sweeps.
