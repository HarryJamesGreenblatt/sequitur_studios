# 0036 — The Interactive Production (the dailies model)

> Date: 2026-08-15 · Focus: **product design / vision** (no code) — a Producer-driven reframe
> of *what the studio's experience is*. The current optimal path is a **batch "ramrod"**:
> one `run_production` pass, commit to every decision at once, dislike the result, start over.
> That's shooting the whole film blind and screening it once. This entry reframes Sequitur as
> an **interactive, phase-gated, iterative** production — the **dailies model** — where each
> phase emits a **Producer-reviewable deliverable** (treatment, poster, board, dailies, cut)
> and the human approves or revises *that phase* before spend flows downstream.

---

## The realization

The prior north star treated the studio's atoms as `Shot` and `Sequence`, with the experience
being `scripts/produce.py` → `Engine.run_production`: read the board → crew assembles → render
→ splice → out, **one pass**. The Producer sits and watches the machine commit to the whole
film simultaneously; if the ending is wrong, they're back at the pitch. No real studio works
this way — they shoot **dailies**, cut a rough, screen it, reshoot. **The gate is the point.**

A second, related realization: earlier I argued "Sequitur never emits a screenplay." That was
defending the *implementation*, not the *product*. The studio **should** emit human-readable
artifacts at each phase — a **treatment/screenplay**, a **theatrical poster** — not as end
products but as the **cheapest possible checkpoints** that let the Producer feel and correct
the film *before* expensive rendering. A poster sells the film in one image; a treatment fixes
the story in text — both for pennies, both before a frame is shot.

## The reframe — a pipeline of Producer-gated deliverables

Each phase produces an artifact the Producer reviews at a **gate** (approve → advance; revise →
re-run *that phase only*, not the whole production):

| Phase | Deliverable (the gate artifact) | Seat · grounding | Producer at the gate |
|---|---|---|---|
| **Plan** | a **treatment / screenplay** *and* **key art / theatrical poster** | Screenwriter (Taxonomy + **Directing Ch. 3–11** dramaturgy) · **Production Designer** (needs a source) → `ImageStudio` | read it, feel it, revise the pitch — before render spend |
| **Previz** | **storyboard panels / shot list** | Storyboard Artist (Prof. Storyboarding) → `ImageStudio` | approve the coverage or re-board |
| **Shoot** | **rendered dailies** (per-shot video/still) | DP / Gaffer / Key Grip → `Studio` / `ImageStudio` | re-roll individual shots, not the film |
| **Assemble** | **rough cut → graded final** | Editor / Colorist → `Cutter` / `Grader` | approve the cut or re-order / re-grade |

The screenplay and the poster are the highest-leverage gates: cheap, human-readable, evocative,
and they **seed everything downstream**. This is also where the earlier "Taxonomy only classifies"
concern resolves — the descriptor stays the machine-facing *classification*; the treatment is the
human-facing *dramatic content* the descriptor + Directing generate. One seat, two outputs.

## Why this is an evolution, not a teardown

Almost every piece already exists — what changes is **orchestration + deliverables**:

- **Producer = HITL greenlight** (`0008`) → becomes a **per-phase gate** (was a single approve).
- **Phase axis on the board** (`0030`, Pre/Prod/Post iterations) → becomes the **pipeline stages**
  with real deliverables (was decoration).
- **The board = the Production instance** (`0024`/`0025`) → already holds state, so **revise-don't-
  restart** is a State transition and re-run of one phase, not a from-scratch rerun. This directly
  kills the "start over from the beginning" fear.
- **The conversational Director** (`0031`) → is already the interactive host that dispatches crew
  and reports back for greenlight. The Producer "sitting in the seat, giving input each phase" *is*
  a Director-agent session.
- **The execute-hook** (`0032`) renders a phase's shots; **`run_production`** (`0027`) is the batch
  version — it **survives as the auto / CI path**, while the gated conversational loop becomes the
  primary human experience. Both ride the same seams.

## Decisions (design intent — not yet built)

1. **The studio emits human-readable phase deliverables.** Reverse the "atoms are only Shot/
   Sequence" stance: a **treatment** and a **poster** (and later a board, dailies, a cut) are
   first-class artifacts, persisted **by reference**, shown at a gate. The engine's atoms don't
   change; the *product's* surface gains named deliverables.
2. **The primary experience is phase-gated and iterative (the dailies model).** Batch
   `run_production` stays as the non-interactive path; it is not the headline UX.
3. **Revise re-runs one phase, not the production.** The board persists each approved phase's
   output, so iteration re-enters at a phase — the whole point of the Production-as-board.
4. **The Screenwriter gains a generative output.** Alongside the typed descriptor, it produces a
   **treatment** grounded in **Directing Ch. 3–11** (dramaturgy the Taxonomy lacks). Deeper
   structural generation (Truby's *Anatomy of Story*) is an optional later source, only if the
   studio should *originate* structure rather than *realize* the Producer's pitch.
5. **Production Design becomes a real seat with its own grounding.** The poster/lookbook needs a
   **Production Designer** over `ImageStudio` and a **dedicated production-design / key-art source**
   (the architecture already flags this cell as open).
6. **The gate lives in BOTH chat and the board.** Chat (the Director agent presents the deliverable,
   the Producer responds) is the live experience; the ADO board (approve = State transition, artifact
   linked) is the durable record.

## The concrete new pieces (dependency order)

1. **`OutputStore` seam, finally built** (`0005`) — Graph/SharePoint, so deliverables persist by
   reference, are shown at gates, and are comparable across iterations. Every later phase reuses it.
2. **Deliverable + gate ritual** — each phase emits an artifact + a review point (approve → advance
   State/phase; revise → re-open + re-run that phase). A small "Deliverable" concept + board State
   transitions per phase.
3. **Screenwriter → treatment** (Directing-grounded), beside the existing descriptor.
4. **Production Designer seat + key-art source** — the poster deliverable.
5. **Interactive orchestration** — the Director agent runs the production **phase by phase with
   gates**, not `run_production` in one shot.

## Recommended first slice

The cheapest, highest-signal gate: **Plan → {treatment + poster} → Producer review.** It forces us
to build the **`OutputStore`** and the **gate/revise ritual** *once*, reusable by every later phase,
and it delivers the most emotionally legible early artifacts (you feel the film before it's shot).

## Open forks (for the Producer to settle)

- **Story-generation depth:** treatment from Directing (realize the pitch) — *recommended start* —
  vs. add Truby (originate structure). Start with the former.
- **Production-design source:** which text grounds key art / the poster (a production-design or
  concept-art / key-art source — an 8th grounding session).
- **Gate mechanics:** chat + board (recommended both) — how much of the ritual is durable on the
  board vs. live in the conversation.

## Open threads

- Build the **`OutputStore`** (`0005`) — now on the critical path, not deferred.
- **Screenwriter treatment output** grounded in Directing Ch. 3–11 (wire Directing into the seat).
- **Production Designer seat** + a key-art grounding source.
- **Gate/revise orchestration** — the Director agent's phase-by-phase interactive loop; `run_production`
  demoted to the batch/CI path.
- Still-open crew code from `0035`: the **Storyboard Artist** seat and a **plan-phase reconcile** —
  both fold naturally into this pipeline (previz deliverable; descriptor → downstream briefs).
