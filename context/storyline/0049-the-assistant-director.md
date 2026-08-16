# 0049 — The Assistant Director: the board as the production's memory

> Date: 2026-08-16 · Focus: close the control-plane gap — nothing was being written to the
> ADO board during runs. Build the **AD/PA** (Assistant Director / Production Assistant) as
> the **Mediator** that collects deliverables and reports them onto the board, so the
> Producer/Director review + approve there and later phases read them back (board-as-RAG).
> **`ProductionProvider` seam + a second Skill; proven live on `TheLaunch`.**

---

## What happened

The runs produced good deliverables but filed them only to the **OutputStore** (OneDrive);
the ADO board stayed a provisioned-but-empty shell. The fix is a dedicated coordination
seat — the one Appendix D stubbed as *Assistant Director (planned)*.

1. **The `ProductionProvider` gains a deliverable seam.** New
   [`report(deliverable, *, body=None)`](../../sequitur/production.py) and
   `fetch_reports(*, phase=None)` on the Protocol and **both** backends:
   - `LocalFolderProduction` (test double) — a JSON `deliverables` list, idempotent by
     phase+name, body persisted for read-back.
   - `AzureDevOpsProduction` (live) — each deliverable is its **own `Deliverable` work
     item**: text body → `System.Description` (queryable — the RAG substrate), image →
     **attachment**, gate verdict → `State` (`pending→To do`, `revise→Doing`,
     `approved→Done`). Idempotent by title.
   - Added the `Deliverable` work-item type + its states to the shared process (reusable by
     every production).

2. **The AD/PA as a Skill — the second generalist-under-direction seat.** Lives as
   [`.github/skills/assistant_director/`](../../.github/skills/assistant_director/): a
   `SKILL.md` (the persona — what's ready, what to chase, what context to hand down) + a
   bundled arm `report_to_board.py` (the deterministic **messenger**). It owns board I/O so
   the producing craft seats never touch ADO. Two directions: **report up** (collect a
   phase's store deliverables → board) and **fetch down** (read approved deliverables back
   as context — the board-as-memory).

3. **Proven live on `TheLaunch`.** The AD arm collected the plan deliverables (treatment +
   one-sheet) and filed them as board items **#13/#14** — the treatment's full text in the
   Description, the one-sheet attached, both `To do` (pending). `--fetch` read them back.
   The board is now the production's working memory.

## Decisions

1. **Mediator, not the Gate.** The `Gate` stays pure (files bytes, returns a
   `Deliverable`); the **AD** owns the board-write. Producing seats stay ignorant of the
   board API — the decoupling Nystrom's messenger is about. Corrected terminology: the
   **Producer** (human) and **Director** *do* use the board (their review/approval
   console); the *craft seats* are the ones kept board-ignorant.
2. **Mediator now, Event-Queue later.** The AD *owns* board I/O; no async signal bus until
   a real multi-consumer/async need appears. Match machinery to need.
3. **Deliverable-as-work-item.** Its own item (approvable, State-trackable, queryable)
   rather than fields buried on a narrative item — this is what makes the board a RAG hub.

## Resulting state

- **The control plane is closed.** Deliverables + verdicts flow onto the board; seats can
  read prior deliverables back as grounding. `test_production` 7 → 10; suite green.
- **Two Skills-pattern seats** (KeyArtist `0048`, AD/PA here) — the pattern applied only to
  generalists under direction, not the grounded specialists.

## Next

- **Bind the verdict fully:** approve/revise made in chat should flow back to the board
  State via the AD (the two review surfaces stay in sync).
- **Fetch-down into dispatch:** hand a later department its approved context automatically
  (the treatment to the shoot crew, the concept to the KeyArtist).
- The `TheLaunch` run needs refinement (noted for discussion) — the one-sheet and the plan
  flow have rough edges to iterate.
