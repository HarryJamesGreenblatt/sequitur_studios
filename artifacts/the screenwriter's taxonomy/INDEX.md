# The Screenwriter's Taxonomy — grounding index

Eric R. Williams, *The Screenwriter's Taxonomy: A Roadmap to Collaborative
Storytelling* (Routledge/Focal Press, ISBN 9781351610667). This is the studio's
**Screenwriter** grounding — the long-missing *story / development* source. Unlike
a prose screenwriting manual, it is a **classification system**: a structured
vocabulary of genre, voice, pathway, and point of view. That makes it
**enum-friendly** — the natural basis for a typed `Screenwriter` role vocabulary
(a `crew/screenwriting.py`), exactly as *Grammar of the Shot* became the camera
roles' enums.

> **Staged, not yet abridged.** The verbatim `source/` is complete (8 chapters);
> the `reference/` abridgement is **deferred to a designated session** (0015). The
> chapter → role map below is the plan; mappings are **provisional** until the
> `Screenwriter` role exists in code.

## Folder layout

- [`extraction/`](extraction/) — the raw `.docx` originals. *(gitignored)*
- [`source/`](source/) — pandoc-converted verbatim Markdown, the **ground truth**. *(gitignored)*
- `reference/` — abridged, session-ready references. *(pending; ships when written)*

## Chapter → (planned) role map

All chapters ground the **Screenwriter** (plan phase). The bold chapters are the
ones that most directly become **typed vocabulary** (candidate enums).

| Ch | Title | Grounds |
|----|-------|---------|
| 1 | The Need for a Road Map | rationale — why a shared story taxonomy matters |
| 2 | **Movie Types and Supergenres** | candidate `Supergenre` enum (the top classification) |
| 3 | **Macrogenres and Microgenres** | candidate `Macrogenre` / `Microgenre` enums |
| 4 | Genre Case Studies | worked examples for the genre vocabulary |
| 5 | **Voice** | candidate `Voice` enum (the storytelling stance) |
| 6 | **Pathway** | candidate `Pathway` enum (structural arc; pairs with Directing Ch. 5) |
| 7 | **Point of View** | candidate `PointOfView` enum (overlaps Directing Ch. 9) |
| 8 | Case Studies | worked examples applying the whole taxonomy |

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
