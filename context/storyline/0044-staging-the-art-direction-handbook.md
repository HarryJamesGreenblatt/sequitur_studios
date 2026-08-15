# 0044 — Staging *The Art Direction Handbook*: the last source, converted + mapped

> Date: 2026-08-15 · Focus: **stage** Michael Rizzo's *The Art Direction Handbook for
> Film & Television* (2nd ed.) — the last outstanding source gap — into verbatim
> `source/` plus a chapter → seat `INDEX.md`. A **staging** entry (source conversion +
> gate + map); **no code**, and the per-chapter `reference/` transformation deferred to
> `0045`.

---

## What happened

The `0015`/`0042` staging pattern: the Producer's eight `.docx` chapters land in
[`extraction/`](../../artifacts/the%20art%20direction%20handbook%20for%20tv%20and%20film/extraction/);
this pass converts + gates + maps them, leaving the transformation for its own session.

1. **Fought the misnamed-OLE2 defect across three re-extractions.** Several deliveries
   carried a legacy OLE2 `.doc` payload behind a `.docx` name (magic `D0 CF 11 E0`, not
   a Zip/OOXML `PK`), which pandoc can't read ("Did not find end of central directory
   signature"). The bad chapter *moved* between deliveries — first CH-04, then CH-03 —
   until a clean re-extraction produced eight valid OOXML files. Ground truth is the
   file magic, not the extension.

2. **Converted all eight to verbatim Markdown.** `pandoc -t gfm --wrap=none
   --extract-media` per the house convention: `CH-NN.md` filenames matching the
   extraction set, images extracted to `source/media/`. The book is an O'Reilly export —
   chapter titles as bold-linked text, images as `<img>` tags (bytes stripped, tags
   kept). CH-04 (the previously OLE2-blocked, image-heavy design-process chapter) came
   through at 874 lines / 168 KB.

3. **Wrote the source
   [`INDEX.md`](../../artifacts/the%20art%20direction%20handbook%20for%20tv%20and%20film/INDEX.md)** —
   a chapter → seat map placing all eight under the **Production Designer** (plan / art
   phase) over `ImageStudio`, with the high-value core (Ch. 4 process, Ch. 3 vocabulary,
   Ch. 7 digital bridge) flagged and the overlaps to reconcile at abridgement noted
   (Rizzo Ch. 1–2 ↔ Directing Ch. 23; Rizzo Ch. 3 ↔ Color Correction Handbook).

4. **Flipped the living docs to *staged*:** the catalog row in
   [`artifacts/INDEX.md`](../../artifacts/INDEX.md) and the Production Designer grounding
   cell in [`architecture.md`](../architecture.md).

## Decisions

1. **Copyright gate holds.** `extraction/` + `source/` stay gitignored; only `INDEX.md`
   (and later `reference/`) ship. Same discipline as every prior source.

2. **The seat is the Production Designer, not the Director.** Rizzo supplements rather
   than repeats Directing Ch. 23: he gives the **whole art department as a managed
   design process**, the dedicated production-design source the `0041` sourcing note
   called for. The naming guard in the INDEX keeps the folder distinct from the
   *directing* and *editing* sources.

3. **Abridgement deferred to `0045`** — one long source's transformation does not share
   a budget with its staging. (In practice `0045` ran the same day, once staging was
   confirmed clean.)

Next: [`0045`](0045-abridging-the-art-direction-handbook.md) — the eight chapters
transformed into session-ready `reference/`.
