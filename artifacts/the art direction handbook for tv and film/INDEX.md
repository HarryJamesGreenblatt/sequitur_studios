# The Art Direction Handbook — grounding index

Michael Rizzo, *The Art Direction Handbook for Film & Television* (2nd ed.,
Routledge/Focal Press, ISBN 9780415842792). This is the studio's **dedicated
production-design source** — the text that seats the **Production Designer** over
the art/color layer (`ImageStudio`, gpt-image), the seat that until now had only
**Directing** Ch. 23 *(abridged, `0017`)* as a single borrowed chapter. It grounds
the *plan* phase's art department: how a script becomes a **visual concept**, then
physical (or digital) **scenery**, and how the art department is run as a design
managed process.

> **Staged + abridged (8 ch, `0044`→`0045`).** The Producer delivered the book's
> eight chapters; the staging pass (`0044`) **converted + gated + mapped** them —
> verbatim [`source/`](source/) is ground truth — and the abridgement pass (`0045`)
> transformed all eight into session-ready [`reference/`](reference/) chapters, each
> closing in a **Studio application** section that grounds the planned **Production
> Designer** seat. Follows the `0015`→`0017`, `0042`→`0043` precedent (staging, then
> abridgement). Mappings remain **leads** until the seat settles in code.

## Folder layout

- [`extraction/`](extraction/) — the raw `.docx` originals (as imported). *(gitignored)*
- [`source/`](source/) — pandoc-converted verbatim Markdown, the **ground truth** (8 ch). *(gitignored)*
- [`reference/`](reference/) — abridged, session-ready references (8 ch, `0045`).

## Chapter → seat map

All eight chapters ground the **Production Designer** (plan / art phase) over the
`ImageStudio` image backend. Rizzo's distinctive contribution — the reason he
supplements rather than repeats Directing Ch. 23 — is the **art department as a
managed design process**: the pipeline from script to a buildable visual concept.
Each row links the verbatim source and its abridged reference.

| Ch | Reference | Source | Grounds |
|----|-----------|--------|---------|
| 1 | [ch01](reference/ch01-introduction.md) | [CH-01](source/CH-01.md) | the art director's remit — "design manager"; Production Designer vs. Art Director — **Production Designer** |
| 2 | [ch02](reference/ch02-responsibilities-relationships-setup.md) | [CH-02](source/CH-02.md) | art department structure & interfaces — **Production Designer** (overlaps Directing Ch. 23) |
| 3 | [ch03](reference/ch03-visual-history.md) | [CH-03](source/CH-03.md) | media-technology history (film-vs-video look) + a **genre taxonomy** — **Production Designer** (palette-concept grounding lives with the Colorist, not here) |
| 4 | [ch04](reference/ch04-the-design-process.md) | [CH-04](source/CH-04.md) | script → research → visual concept → design — the **core** PD pipeline — **Production Designer** |
| 5 | [ch05](reference/ch05-the-physical-design.md) | [CH-05](source/CH-05.md) | locations vs. build, the set list, spatial design — the buildable scene — **Production Designer** |
| 6 | [ch06](reference/ch06-legacy-of-historical-techniques.md) | [CH-06](source/CH-06.md) | classic in-camera techniques a generative model collapses — **Production Designer** (lexicon only; lightest abridgement) |
| 7 | [ch07](reference/ch07-cgi-and-digital-filmmaking.md) | [CH-07](source/CH-07.md) | digital art direction — the bridge to a **generative** image backend — **Production Designer · ImageStudio** |
| 8 | [ch08](reference/ch08-paperwork-and-daily-shooting-tasks.md) | [CH-08](source/CH-08.md) | art-department logistics & shooting-day tasks — **Production Designer · Assistant Director** |

## Scope note

This source fills the **art-department gap** the catalog flagged since `0041`:
Directing Ch. 23 gives a single chapter of visual-design principle; Rizzo gives the
**whole department and its process**. The abridgement (`0045`) scoped each chapter to
what the **Production Designer over `ImageStudio`** actually needs — the design
*process* (Ch. 4) and the digital bridge (Ch. 7) are the high-value core; the
physical-construction, historical-technique, and logistics material (Ch. 5–6, 8) is
real craft that only partially transfers to a generative backend, so it was abridged
**surgically** and its Studio-application sections say so honestly. One correction
surfaced during abridgement: Rizzo's Ch. 3 "Visual History" is a **media-technology**
history (persistence-of-vision, telecine, film-vs-video) plus a **genre taxonomy** —
*not* the period/palette vocabulary the staging map assumed; the palette-concept
grounding lives with the Colorist and the Color Correction Handbook instead. Overlaps
reconciled: the art department's **remit & relationships** (Rizzo Ch. 1–2 ↔ Directing
Ch. 23); the **color/palette concept** boundary (Rizzo Ch. 3 ↔ Color Correction
Handbook, `0020` — Rizzo is *design intent*, Van Hurkman is *grading execution*; kept
separate).

> **Naming guard.** The folder is `the art direction handbook for tv and film/`
> (Rizzo, production design) — distinct from the *directing* and *editing* sources.
> It seats the **Production Designer**, not the Director.
