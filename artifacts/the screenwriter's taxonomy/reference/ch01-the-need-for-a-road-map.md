# Chapter 1 — The Need for a Road Map

> Abridged from Eric R. Williams, *The Screenwriter's Taxonomy* (Routledge/Focal
> Press), Ch. 1. **Scope:** why story work needs a *shared, layered vocabulary*
> instead of a flat genre list, and a first pass over the seven layers the rest of
> the book defines. This is the **overview** chapter — the map of the map.

## Core idea

The word "genre" causes more trouble than it should because the public uses it as a
**flat search list** (Comedy, Sci-Fi, Western, Zombie…) — categories good for
*finding* a film but useless for *writing* one. "Write me a comedy. Go." is as vague
as "draw an animal. Go." Williams borrows the biologists' fix: a **taxonomy** — a
*layered* classification (kingdom → phylum → class …) that describes a thing by
naming its commonalities at each level. Applied to film, the taxonomy turns one
vague idea into a precise, discussable **road map** that a writer, a co-writer, and
a producer can all read the same way.

It is a **creative**, not scholarly, tool: it names the **audience's expectations**
so the writer can deliberately meet, subvert, or reinvent them. It doesn't limit the
imagination any more than the taxonomy of living things limits Mother Nature.

## The seven layers (the road-trip metaphor)

Every script is a road trip out of one city; each layer is a decision along the way.

| # | Layer | Road-trip analogue | What it fixes |
|---|-------|--------------------|---------------|
| 1 | **Type** | drive east or west | Comedy or Drama |
| 2 | **Supergenre** | which state you cross | broad Story · Character · Atmosphere (11 options) |
| 3 | **Macrogenre** | which city you stop in | refines the super (~50 options) |
| — | **Microgenre** | which restaurant | further specificity (200+, tied to a macro) |
| 4 | **Voice** | the vehicle you drive | *how* the story is told (linear? musical? animated?) |
| 5 | **Pathway** | which road you take | the *trajectory* that leads the audience through |
| 6 | **Point of View** | who's driving | how much the audience knows, and through whom |

Seven interlocking decisions yield **200 million+ unique combinations** — enough that
"is this a genre that interests you?" becomes a set of answerable questions rather
than a shrug.

## Worked example — adapting *Romeo & Juliet*

A producer wants a modern *Romeo & Juliet* whodunit. Opening on three dead teenagers
in a cemetery already fixes **Type** = Drama (tragedy), **Supergenre** = Crime,
**Macro/Micro** = Mystery/Whodunit + Legal/Courtroom. That in turn *implies* the rest:
an adult **POV** (the leads are dead → tell it through a detective-Friar), a
**nonlinear Voice** (start at the end), a **noir Pathway**, **primary omniscient**
POV. One conversation, seven connected decisions, a shared blueprint — and a clear
sense of how *this* version differs from Shakespeare's. (Revisited in
[Ch. 8](ch08-case-studies.md).)

## Studio application

This source is the studio's long-missing **Story / development** grounding, and it is
uniquely **enum-friendly** — a layered classification is exactly what a typed
vocabulary wants to be.

- **The seven layers are the shape of a future `Screenwriter` role.** Just as
  *Grammar of the Shot* became the camera roles' enums (`crew/camera.py`), this
  taxonomy is the natural basis for a `crew/screenwriting.py` `Screenwriter` (plan
  phase) that **owns** the Type/Supergenre/Macro/Micro/Voice/Pathway/POV vocabulary.
- **It is the plan-phase upstream of the whole pipeline.** The taxonomy's choices
  *cascade*: genre implies POV implies shot selection (camera), pathway implies the
  edit's sequence shape, voice's "modern style" constrains the entire grammar. A
  `Screenwriter` `Contribution` would seed the [`Brief`](../../../sequitur/crew/role.py)
  that the `Director` reconciler ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md))
  hands down to the shoot crew.
- **A road map, not paint-by-numbers.** Like every role's heuristic, the Screenwriter
  picks defaults (Traditional voice / single protagonist / filmmaker-omniscient) that
  a Producer brief can override — the same A→B (`HeuristicJudgment` → `PersonaJudgment`)
  seam the crew engine already uses.

The remaining chapters define each layer: [Type & Supergenre](ch02-movie-types-and-supergenres.md) ·
[Macro & Micro](ch03-macrogenres-and-microgenres.md) · [Voice](ch05-voice.md) ·
[Pathway](ch06-pathway.md) · [Point of View](ch07-point-of-view.md), with case studies
in [Ch. 4](ch04-genre-case-studies.md) and [Ch. 8](ch08-case-studies.md).
