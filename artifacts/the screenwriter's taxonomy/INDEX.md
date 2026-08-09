# The Screenwriter's Taxonomy — grounding index

Eric R. Williams, *The Screenwriter's Taxonomy: A Roadmap to Collaborative
Storytelling* (Routledge/Focal Press, ISBN 9781351610667). This is the studio's
**Screenwriter** grounding — the long-missing *story / development* source. Unlike
a prose screenwriting manual, it is a **classification system**: a structured
vocabulary of genre, voice, pathway, and point of view. That makes it
**enum-friendly** — the natural basis for a typed `Screenwriter` role vocabulary
(a `crew/screenwriting.py`), exactly as *Grammar of the Shot* became the camera
roles' enums.

> **Abridged (8 ch) — 0016.** The verbatim `source/` (8 chapters) has been abridged
> into 8 session-ready [`reference/`](reference/) chapters, each ending in a **Studio
> application** section. The chapter → role map below now links each reference;
> mappings remain **provisional** until the `Screenwriter` role exists in code.

## Folder layout

- [`extraction/`](extraction/) — the raw `.docx` originals. *(gitignored)*
- [`source/`](source/) — pandoc-converted verbatim Markdown, the **ground truth**. *(gitignored)*
- [`reference/`](reference/) — abridged, session-ready references (8 chapters). *(ships)*

## Chapter → (planned) role map

All chapters ground the **Screenwriter** (plan phase). The bold chapters are the
ones that most directly become **typed vocabulary** (candidate enums).

| Ch | Reference | Grounds |
|----|-----------|---------|
| 1 | [The Need for a Road Map](reference/ch01-the-need-for-a-road-map.md) | rationale — the 7-layer model; shape of a future `Screenwriter` role |
| 2 | [**Movie Types and Supergenres**](reference/ch02-movie-types-and-supergenres.md) | `MovieType` enum + closed 11-value `Supergenre` enum (Story·Character·Atmosphere bundles) |
| 3 | [**Macrogenres and Microgenres**](reference/ch03-macrogenres-and-microgenres.md) | large `Macrogenre` enum + open macro-scoped `Microgenre` tag |
| 4 | [Genre Case Studies](reference/ch04-genre-case-studies.md) | one logline → 3 films; super-choice cascades to POV/pathway |
| 5 | [**Voice**](reference/ch05-voice.md) | `Voice` = a *struct of ~6 axes* (the seam to the render grammar) |
| 6 | [**Pathway**](reference/ch06-pathway.md) | closed ~20-value `Pathway` enum (structural arc; pairs with Directing Ch. 5) |
| 7 | [**Point of View**](reference/ch07-point-of-view.md) | 3 small enums (Scope×Focus×Stance); upstream of camera coverage (overlaps Directing Ch. 9) |
| 8 | [Case Studies](reference/ch08-case-studies.md) | the full six-layer descriptor *vector*; analytic + generative |

## Scope note

This source fills the **Story / screenwriting** cell that has been *Planned* since
the library began. Its payoff is that it is **structured for code**: where a prose
manual would resist becoming vocabulary, Williams' supergenre → macrogenre →
microgenre hierarchy, plus Voice / Pathway / Point-of-View axes, map onto **typed
enums** a `Screenwriter` role can own — the same pattern that let *Grammar of the
Shot* become `crew/camera.py`. It **complements Directing Ch. 3–8**: the Taxonomy
classifies the story, Directing supplies the dramaturgical craft to realise it.
Point of View appears in both (Taxonomy Ch. 7 · Directing Ch. 9) — reconcile the
two when that axis is encoded.
