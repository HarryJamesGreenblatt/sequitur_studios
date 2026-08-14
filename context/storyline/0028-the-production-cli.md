# 0028 — The Production CLI (`produce.py`)

> Date: 2026-08-13 · Focus: **code** — a thin CLI over `Engine.run_production` (`0027`)
> so the board-to-board round trip is usable from the command line, no REPL. Closes the
> "board-to-board CLI" thread `0027` opened.

---

## What happened

- **Added [`scripts/produce.py`](../../scripts/produce.py).** It builds a
  `ProductionProvider`, runs `Engine().run_production(provider, scene=…)`, and prints the
  assembled timeline (per clip: incoming transition, applied grade, duration, and the shot).
  The board is the **configured ADO production** by default (pointers from `.env`), or a
  **local-folder** production with `--local <path>` for a quick offline run.

- **Two flags for the two useful modes.** `--scene` labels the assembled `Brief`; `--no-write`
  reads and assembles and prints *without* writing the `Sequence` back — a safe preview of what
  the crew would commit. Backends and the Studio are imported lazily, so `--local` needs no
  Azure credentials.

- **Validated both paths.** `--local` against a JSON fixture ran fully board-to-board offline
  (fade-in + cut, base grade, 8 s); `--no-write` against the *live* ADO board read the two
  shots, assembled a graded two-clip sequence, and printed it — touching nothing.

## Decisions

1. **A dedicated script, not a `generate.py` flag.** `generate.py` renders a *single shot*;
   `produce.py` runs a *whole production* off its board. Different inputs (grammar flags vs. a
   board), different outputs (a rendered clip vs. an assembled edit) — a separate, discoverable
   entry point keeps each CLI honest, mirroring the provider/renderer split in the library.

2. **`--no-write` instead of a dry-run of side effects.** The preview mode simply composes
   `read_brief` + `assemble` and skips `write_sequence` — it reuses the same pieces
   `run_production` joins, so there is no separate "dry" code path to drift.

## Resulting state

- `python scripts/produce.py` runs a production board-to-board from the shell; `--local` runs it
  offline; `--no-write` previews. The whole chain is now usable end to end without code: provision
  a board (`0026`) → work it (the ADO boards) → assemble & grade it board-to-board (`produce.py`).
  No new tests (a thin CLI, like `generate.py`); validated by running.

## Open threads

- Unchanged from `0027`: the read is still flat/positional and the look aggregates (uniform
  grade); scene-scoped reads + per-shot grade matching (Color Correction Handbook Ch. 9), and
  writing work-item **State** (not just `Look`), remain the next refinements. A `--render` flag
  that pushes the assembled `Sequence` through the `Cutter`/`Grader` to actual media is a natural
  future addition once per-shot grades land.
