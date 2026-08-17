# 0055 — Casting as selection: the audition, the gate, the verdict

> Date: 2026-08-16 · Focus: build **Casting Phase 2** — render each principal's
> candidate `Actor`s (the audition), file them at a `Gate` for the Producer, and let the
> Producer **select** one, binding the cast Actor and locking its reference. This is the
> **verdict loop's first concrete instance** and the consistency backbone the studio was
> missing.

---

## What happened

Storyline 0054 built the cast *entities* and the seat, but stopped at design: a
`Character` could hold `candidates` and a `cast`, yet nothing rendered the audition or
performed the selection. So a named character (Nora) still had no *locked* look — the gap
0054 opened. This session closes it with the three moves casting actually is: **render the
audition → review at a gate → select one**.

1. **The audition is a render, not a new renderer.** Each candidate `Actor`'s
   persona-authored `look` becomes a still keyframe through the existing **STILL** backend
   (`gpt-image`) — casting produces the same media kind the Production Designer does, so it
   rides the same producer (the 0019 facilitative-renderer principle: a role gets its own
   renderer only if it makes a *distinct* artifact). A new prompt composer,
   [`build_character_prompt`](../../sequitur/prompt.py), reads the cast entities (Actor
   `look` + Character age/build/wardrobe/essence) rather than a camera `Shot`, and asks for
   a deliberately **scene-agnostic, neutral character reference** — a single consistent
   figure on a plain background, exactly the frame downstream renders can lock to.

2. **The audition rides the Gate.** `Director.audition(character, *, gate)` renders each
   candidate, files it durably through the `Gate` (0040) as a **PENDING** `Deliverable`,
   and **locks** each candidate's `reference` to its durable keyframe. It lives on the
   Director (the orchestrator that holds renderers), exactly like `deliver_plan` and
   `execute` — the seat *designs* the candidates, the Director *executes* the audition.

3. **Selection is the verdict.** `Character.select(actor)` binds the chosen embodiment as
   `cast` — and refuses any Actor that never auditioned (`ValueError`), the
   abundance-then-selection discipline (Directing Ch. 18: you choose from the field you
   called). The cast Actor's already-locked `reference` is now the character's look for
   every downstream render. This is the **first instance of the verdict loop** the dailies
   model needs — a Producer choosing among rendered, gated candidates.

## Decisions

1. **Reuse the STILL backend; add only a prompt composer.** No casting renderer — casting
   makes a still, so it goes through `renderer_for(Medium.STILL)`. The only new execution
   piece is `build_character_prompt`.
2. **`audition` on the Director, `select` on the Character.** The render+gate orchestration
   belongs with the other Director producers (`deliver_plan`, `execute`); the
   cast-must-be-among-candidates invariant belongs with the entity that owns both lists.
3. **The character reference is neutral by design.** A locked look must be reusable across
   any scene, so the audition frame asks for a plain-background portrait, not an action
   beat — the opposite of `build_image_prompt`/`build_poster_prompt`.
4. **Lock the reference at audition time, not selection time.** Every candidate's keyframe
   is durable the moment it's filed, so a candidate can be *shown* (and later reconsidered)
   with a real ref; selection only chooses which locked look is canonical.
5. **The seat still never selects.** The Casting Director agent designs and auditions; the
   **Producer** selects. The Director agent's plan-phase steps now spell this out.

## Resulting state

- **New code:** [`build_character_prompt`](../../sequitur/prompt.py) (the audition frame),
  [`Director.audition`](../../sequitur/crew/director.py) (render → gate → lock references),
  [`Character.select`](../../sequitur/cast.py) (the Producer's verdict, membership-checked),
  and the `build_character_prompt` export.
- **Agent:** [`director.agent.md`](../../.github/agents/director.agent.md) gained a
  plan-phase **Casting Director** dispatch and a **cast-the-principals** step (audition →
  Producer selects; the seat never selects).
- **Tests:** [`tests/test_casting.py`](../../tests/test_casting.py) 7 → 10 — the audition
  frame, the membership-checked selection, and an offline end-to-end audition (a fake STILL
  producer + a `LocalFolderOutputStore` + a `Gate`: two candidates rendered, filed, and
  reference-locked; nothing cast until the verdict). **12-module suite green.**
- The plan phase can now *design → audition → cast* a principal end-to-end in code; the
  locked reference is ready to thread downstream.

## Next

- **Phase 3 — thread the locked reference:** condition key art / PD / shots on the cast
  Actor's `reference` (the consistency payoff — stop re-inventing the character each render).
- **Generalize the verdict loop:** the board side — a Producer approve/revise on a
  `Deliverable` writes State back through the `ProductionProvider` (the AD/PA seat), so the
  gate persists the *verdict*, not just the artifact (the 0040 deferral). Casting selection
  is the first instance; make it the general pattern.
- **Board (deferred):** a **Casting** area + whether `Character`/`Actor` want WIT
  representation so the audition is reviewable on the board (the `Cut` question again).
- **Live proof:** run a real audition through `gpt-image` (this session's proof was offline
  with a fake producer) to confirm candidate references render and lock as designed.
