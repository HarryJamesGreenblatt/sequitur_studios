# 0027 — Board-to-Board (binding the provider into the engine)

> Date: 2026-08-13 · Focus: **code** — closed the top open thread of `0025`: the crew
> `Engine` now reads its `Brief` from a `ProductionProvider` and writes the assembled
> `Sequence` back, so a whole production runs **board-to-board** in one call. The payoff
> of the provider arc (`0024`–`0026`): the board is now a first-class input *and* output
> of the studio, not just a place a human logs work.

---

## What happened

- **Added `Engine.run_production(provider, *, scene=None)`.** A single method that binds
  the assemble phase to a production board: it calls `provider.read_brief(...)` (the board's
  coverage → a `Brief`), `self.assemble(brief)` (the crew reconciles a graded edit
  `Sequence`), and `provider.write_sequence(sequence)` (the applied grade → back onto the
  board), returning the `Sequence`. The three pieces already existed (`0023` assemble,
  `0025` provider); this is the seam that joins them.

- **Kept the engine backend-agnostic.** The `provider` parameter is typed only under
  `TYPE_CHECKING` and used purely by duck typing (it is a `runtime_checkable` Protocol), so
  `crew/engine.py` imports nothing from `production.py` at runtime — no import cycle, and the
  same swappability the `Renderer` seam gives the execution plane. A `LocalFolderProduction`
  and an `AzureDevOpsProduction` are interchangeable behind the one call.

- **Verified both offline and live.** A new guard test drives
  `Engine().run_production(LocalFolderProduction(...))` end-to-end through the real crew
  (board → brief → graded sequence → board), all **32 smoke tests green**; and a live run
  against the actual board — `Engine().run_production(AzureDevOpsProduction())` — read the two
  shots, assembled a graded two-clip sequence, and wrote the look back (restored afterward so
  the example tree keeps its per-shot looks).

## Decisions

1. **The round trip is one method, not a flag-laden pipeline.** `run_production` *is* the
   board-to-board flow (read → assemble → write); a caller who wants to assemble without
   writing simply composes the pieces (`engine.assemble(provider.read_brief())`). No
   `write=False` knob — the method's name is its contract.

2. **Bind on the engine, depend via the Protocol.** The binding lives on `Engine` (the driver)
   and reaches the provider through the `ProductionProvider` Protocol, never a concrete class —
   so the engine stays ignorant of ADO vs. local-folder, exactly as it is ignorant of Gemini
   vs. Azure behind the `Renderer` seam.

## Resulting state

- `Engine().run_production(provider)` runs a production board-to-board. The provider supplies
  the `Brief` and receives the `Sequence`; the engine and crew are unchanged otherwise. Guard
  test `tests/test_production.py` now 6 (added the round-trip-through-the-engine case); 32
  smoke tests green; verified live against the board.
- This closes the `0025` "bind the provider into the engine" thread. The studio can now read a
  production off the board, let the crew assemble and grade it, and record the result back —
  with a `LocalFolderProduction` for tests and an `AzureDevOpsProduction` for the real board.

## Open threads

- **Read is still flat/positional and the look aggregates** (`0025`): `read_brief` returns every
  `Shot` in id order and collapses per-shot looks to one brief nudge, so `run_production` grades
  the whole sequence uniformly. Scene-scoped reads and per-shot grade matching (Color Correction
  Handbook Ch. 9) remain the next refinements.
- **Write records only the look** — advancing work-item **State** on write (so a graded shot
  visibly progresses on the board) is still open.
- **A board-to-board CLI** — a `scripts/generate.py` mode (or a small new entry) that runs
  `run_production` against the configured board would make the round trip usable without a REPL.
- **The shoot phase** — `run_production` binds the *assemble* phase; a symmetrical
  read-brief → `run(Phase.SHOOT)` → write-shot path (per-shot grammar back to the board) is a
  natural follow-on once the shoot-phase board write is designed.
