# 0035 — The Screenwriter Seat (the plan-phase story vocabulary)

> Date: 2026-08-14 · Focus: **code** — built `crew/screenwriting.py`, seating the
> **Screenwriter** (the plan phase) over Eric R. Williams' *Screenwriter's Taxonomy* as a
> **layered descriptor vector**. Vocabulary + a heuristic default — the plan-phase analogue
> of `0012`'s camera re-seating. Grounded from the abridged source, not guessed. 5 new guard
> tests; suite 38 green.

---

## What happened

- **Built the story department's owned language** in
  [`sequitur/crew/screenwriting.py`](../../sequitur/crew/screenwriting.py), encoding the
  taxonomy's seven layers from the [abridged reference](../../artifacts/the%20screenwriter's%20taxonomy/reference/):
  - **`MovieType`** (Comedy/Drama) and the closed eleven-value **`Supergenre`** (Action …
    Western) — the umbrella that *defines* Story/Character/Atmosphere (Ch. 2);
  - **`Macrogenre`** — a curated **50-value** modifier enum, multiple-allowed, plus an open
    macro-scoped **microgenre** tag as a plain `str` (200+ and meant to grow, Ch. 3);
  - **`Voice`** — a `@dataclass` **struct of six orthogonal axes** (`Linearity` ·
    `FilmmakingStyle` · `Audience` · `Performer` · `DialogueMode` · `FourthWall`) defaulting
    to the book's *traditional voice* (Ch. 5) — the seam where the story layer reaches into
    the render grammar;
  - **`Pathway`** — the closed **20-value** trajectory (the Hero's-Journey baseline + 19
    divergences, each carrying the traditional rule it `breaks`, Ch. 6);
  - point of view as **three small enums** — `Scope` × `Focus` × `Stance` (Ch. 7) — the
    direct upstream of camera coverage.

- **Seated the `Screenwriter` role** (`Department.STORY`, new; `Phase.PLAN`) owning all
  thirteen enum types, with a `heuristic` that returns the **neutral descriptor** (a linear,
  broad, objective slice-of-life — the cheapest umbrella to render), every field
  hint-overridable. Its `Contribution` is a **story descriptor**, not a `Shot`.

- **Wired it minimally.** Added `Department.STORY`, a `plan_crew()` helper, and the public
  exports (`Screenwriter` + the vocabulary + `Voice`). Kept the Screenwriter **out of
  `full_crew()`** — a story descriptor isn't `Shot`-reconcilable, so it needs a plan-phase
  reconcile (a later pass) before the `Engine` can dispatch it. Guard test
  `tests/test_screenwriting.py` (5): plan-phase seat, full membership (2/11/50/20), the
  traditional `Voice`, the neutral descriptor, and hint overrides. **Suite 38 green.**

## Decisions

1. **Vocabulary-only first — mirror `0012`.** The camera seats were re-seated as vocabulary
   before behaviour (`0014`); the Screenwriter follows the same discipline. Building the
   *language* correctly (grounded, full membership) is the deliverable; the plan-phase
   reconcile is a separate, honest next step, not smuggled in half-built.

2. **Three storage shapes for three tiers.** Closed enum (`Supergenre`), large curated enum
   (`Macrogenre`, multiple-allowed → a list field), open tag (`microgenre` → `str`) — the
   same closed-vs-open discipline the crew already practices. POV is three enums, not one
   (their product names a POV); `Voice` is a struct, not an enum (six independent axes).

3. **Grounded, not guessed.** Read the abridged Ch. 2/3/5/6/7 for the actual membership
   (the eleven supers, the ~50 macros, the 20 pathways, the six Voice axes) rather than
   approximating — the lesson that a domain vocabulary must come from the source.

## Resulting state

- The plan phase has its first code seat. `crew/screenwriting.py` owns the taxonomy;
  `Department.STORY` + `plan_crew()` are in place; the public surface gained the Screenwriter
  and its vocabulary. No existing behaviour changed — `full_crew()` is still shoot + assemble,
  so `Engine.run`/`assemble`/`run_production` are untouched (38 tests green). The architecture
  doc's plan-table Screenwriter row flipped to **role built — vocab**.

## Open threads

- **The Screenwriter's agent twin** — now that the code seat (enums) exists, it earns a
  `screenwriter.agent.md` (the persona **B** tier), grounded in the Taxonomy, bound to these
  enums.
- **The Storyboard Artist seat** — the other plan seat still needs its code twin (a previz
  role over the reference-keyframe flow) before its agent.
- **Plan-phase reconcile** — a Director/Engine pass that turns the story descriptor into
  downstream briefs (POV → coverage constraint, Voice → backend/sound routing, Pathway → the
  edit's sequence shape), then adds the Screenwriter to `full_crew()`.
