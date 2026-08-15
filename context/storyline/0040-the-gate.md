# 0040 — The Gate

> Date: 2026-08-15 · Focus: **code** — built the **deliverable + gate** model, the dailies
> model's review checkpoint (`0036`). `sequitur/gate.py`: an immutable `Deliverable`
> (production · phase · durable `ref` · `GateStatus`) with `approve` / `revise` transitions,
> and a `Gate` that binds a production to an `OutputStore` and `submit`s an artifact — filing
> it durably under its phase and returning a **pending** deliverable ready to present. The
> tier-agnostic core the Director agent (chat) and the board (durable record) will share.
> 51 tests green.

---

## What happened

`0038` gave the studio a durable place for bytes; `0039` made a render land there. This session
added the *review* concept on top — the thing that makes the dailies model interactive: a
**deliverable** a Producer sees at a **gate**, and the verdict that either advances the phase or
sends it back.

- **`GateStatus`** — the Producer's verdict: `PENDING` (produced, awaiting review), `APPROVED`
  (accepted; the phase may advance), `REVISE` (sent back to re-run, optionally with notes).

- **`Deliverable`** — a frozen dataclass: `production`, `phase` (the existing
  `crew.role.Phase`), `name`, a durable `ref` (the `OutputStore` location from `0038`), a
  `status`, and optional `notes`. It is **immutable**: `approve()` and `revise(notes)` return a
  *new* record via `dataclasses.replace`, so a deliverable's life is a chain of versions, not a
  mutated cell — exactly what "compare a phase's deliverable across revisions" (`0036`) needs.

- **`Gate`** — binds one `production` to an `OutputStore`. `submit(artifact, *, phase, name=None)`
  files the artifact durably (`store.put(..., layer=phase.value)`) and returns a **pending**
  `Deliverable`. `artifact` is raw bytes or a produced path (a rendered shot, a poster, an
  encoded treatment) — the store's contract, so the same gate serves every phase's output.

- **Tests** (`tests/test_gate.py`, 4, offline against a temp store): submit files the bytes under
  `<production>/<phase>/` and returns a `PENDING` deliverable; `approve` flips to `APPROVED` and
  clears notes while leaving the original `PENDING` (immutability); `revise` carries the
  Producer's notes; a produced path defaults its name. Suite **51 green** (was 47).

## Decisions

1. **The deliverable is immutable; transitions return new versions.** A gate's whole value is a
   durable, comparable history — a mutated status cell would erase it. `approve`/`revise` produce
   fresh records, so "revise → re-run → new deliverable" is a version chain over the same phase.

2. **`phase` is the first-class `Phase` enum, mapped onto the store's generic `layer`.** The
   store deliberately kept `layer` a free string (`0038`); the gate is phase-aware, so it speaks
   `Phase` and files under `phase.value`. `Phase.SHOOT.value == "shoot"` also lines up with the
   `0039` execute-hook's default, so shot dailies and gate submissions land in the same place.

3. **The Gate persists the artifact, not (yet) the verdict.** `submit` durably files the
   *bytes* via the `OutputStore`; recording the *verdict* durably — linking the `ref` onto the
   board and moving the phase's State — rides the `ProductionProvider` and is the next step
   (the board State-write thread deferred since `0025`). This keeps the model testable offline
   and avoids bloating the provider protocol before the ADO State work is actually done.

4. **One Gate, every phase's output.** Because `submit` takes the store's `bytes | path`
   contract, the *same* gate handles a Shot render (via the `0039` hook's durable ref), a poster
   image, or an encoded treatment — the plan phase's non-shot deliverables ride it directly, as
   `0039` flagged.

## Resulting state

The dailies model now has its review vocabulary in code: a phase produces an artifact → `Gate.submit`
files it durably and returns a pending `Deliverable` → the Producer's `approve` / `revise` are
immutable transitions carrying notes. It is tier-agnostic — the conversational Director agent
presents the deliverable in chat, and the board will hold the durable verdict — and fully offline-
testable. No new dependency; 51 tests green.

## Open threads

- **Bind the verdict to the board.** Extend the `ProductionProvider` (or a sibling) so `approve`
  links the `ref` and moves the phase's State/iteration, and `revise` re-opens it — the long-
  deferred board State-write, now with a concrete consumer.
- **The interactive loop.** The Director agent runs a phase → `Gate.submit` → present the
  deliverable → capture the Producer's verdict → advance or re-run *that* phase.
- Unchanged from `0036`: the **Screenwriter treatment** (Directing Ch. 3–11) and the **Production
  Designer seat + key-art source** — the two producers of the plan phase's deliverables. With the
  store, the render→persist hook, and now the gate all in place, the first slice — **plan →
  {treatment + poster} → gate** — is down to building those two producers.
