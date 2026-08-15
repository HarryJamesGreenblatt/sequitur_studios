# 0034 — The Assemble Crew (persona seats for post)

> Date: 2026-08-14 · Focus: **agent-customization** — expanded the persona (B) tier from the
> shoot crew to the **assemble crew**: `editor.agent.md` (the cut) and `colorist.agent.md`
> (the look). Every `crew/<role>.py` that owns enums now has its `<role>.agent.md` twin.
> Proved both live on a shared assemble brief. No `sequitur/` code changed.

---

## What happened

- **Built the two assemble seats** in [`.github/agents/`](../../.github/agents/):
  - **`editor.agent.md`** — grounded in **Grammar of the Edit** (Ch. 5 the six motivators,
    Ch. 6 transitions & categories, Ch. 8 "a reason for every edit"). Owns the `Transition` /
    `EditReason` / `EditCategory` enums (source of truth
    [`crew/editorial.py`](../../sequitur/crew/editorial.py)). Its Contribution is a **per-shot
    cut** — a `transition` + the motivating `reason` (optionally the `category`), one entry per
    shot in the coverage, opening on `FADE_IN`.
  - **`colorist.agent.md`** — grounded in the **Color Correction Handbook** (Ch. 3 tonal bands,
    Ch. 4 colour/cast, Ch. 9 shot matching). Owns `Look` / `Cast` / `TonalRange`
    ([`crew/colorist.py`](../../sequitur/crew/colorist.py)). Its Contribution is the sequence's
    base **`look`** (with optional `cast` / `tonal_range`); the Tier-A code compiles the chosen
    look into an executable `Grade` (`Colorist.grade`) — the persona chooses the *look*, not the
    op stack.

- **Proved both live.** Dispatched them on one assemble brief (a lantern-lit graveside vigil,
  three shots, mood "quiet grief, cold"). The **Editor** returned a valid cut — `FADE_IN` open,
  then `CUT`/`INFORMATION` into the widow's face, then `CUT`/`MOTIVATION` + `SCREEN_POSITION`
  down to her hands (straight cuts to hold the stillness; it correctly declined a dissolve on the
  handles cost). The **Colorist** returned `look: COOL` working the `SHADOWS` band, cast left
  `NEUTRAL` to spare the warm lanterns. Every value a real enum member, each citing its grounding.

- **They reconcile conflict-free.** The Editor owns `cut`, the Colorist owns `look` (→ the base
  `grade`) — **disjoint** fields, exactly as `Director.assemble` merges them into a graded
  `Sequence`. The persona tier now covers the whole assemble phase, not just the shoot.

## Decisions

1. **Only seats with a code twin get an agent.** The `0031` principle is a `<role>.agent.md`
   *twin* of a `crew/<role>.py` that owns enums. Editor and Colorist qualify; the **plan seats
   (Screenwriter / Storyboard Artist) do not yet** — `crew/screenwriting.py` and a storyboard
   role aren't built, so there's no enum schema to bind a persona to. They wait on their code
   twin (a larger piece), keeping the tier honest: no agent without a schema.

2. **The Colorist persona chooses a `look`, not a `Grade`.** Judgment owns the *vocabulary*
   (`Look`); compiling it into the reified op stack is Tier-A execution (`Colorist.grade` →
   [`grade.py`](../../sequitur/grade.py)). This mirrors how the shoot agents emit enum members
   and the code assembles the `Shot` — the clean judgment / schema / execution split.

## Resulting state

- Six agent files in [`.github/agents/`](../../.github/agents/) — `director` + the **shoot**
  crew (`cinematographer` · `gaffer` · `keygrip`) + the **assemble** crew (`editor` ·
  `colorist`), each grounded in its own source and bound to its code enums. The Director agent
  gained an assemble-phase dispatch step; the architecture doc's tier-B bullet records the
  assemble crew. **No `sequitur/` code changed**; the 33-test suite is untouched.

## Open threads

- **Plan seats need code first** — build `crew/screenwriting.py` (the Taxonomy layered
  descriptor — `MovieType`/`Supergenre`/`Macrogenre`/`Microgenre`/`Voice`/`Pathway`/`POV`) and a
  `StoryboardArtist` seat, *then* their agent twins. This is the last stretch of the crew.
- **Vocabulary card** — the six agents still list enums by hand (drift risk). A generated
  per-role card from `crew/` would keep the code authoritative.
- **Bind the execute-hook to the board** — `read_brief` → Director → assemble → **execute** →
  record the output `ref` back (the `OutputStore` seam, `0005`).
