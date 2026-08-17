# 0061 — Documentation as policy, not plumbing: the report-after-each stream

> Date: 2026-08-16 · Focus: the Producer watched the board sit empty for minutes while the
> whole plan phase ran in the agent layer, then got dumped at the end. We considered a
> Nystrom **Event Queue**, weighed the "in-process" consequences and the wariness against
> **provisioning infra for documentation**, and landed somewhere better: **no queue, no
> infra** — the OutputStore is already the durable log, so documentation is an idempotent
> **projection** of it. Built the **`--report` streaming policy** and proved it end-to-end
> offline.

---

## The conversation that led here

Running the *mysterious audition* pipeline, the whole plan phase (Screenwriter → Production
Designer → Casting) executed in chat, then reported to ADO only at the very end — the board
was blank the entire time, and I hadn't even provisioned it yet. That's the 0036 "ramrod" /
0051 "chat vacuum" returning: **the board treated as an end-of-phase archive, not the live
spine.**

The instinct was Nystrom's **Event Queue** (decouple production from documentation *in
time* — emit and continue). Two objections dismantled the naïve version:

1. **"Infra for documentation" is tail-wags-dog.** Standing up a Service Bus / Storage Queue
   to keep *records* is the wrong tool. (Producer, correct.)
2. **In-process buys almost nothing for us.** Our CLIs are short-lived; a worker thread must
   flush before the process exits, so the board-write latency just moves to the end — it
   never leaves the critical path. The real payoff needs a *long-lived* process we don't have.

**The resolution — it's already solved by pieces we own:**
- The **OutputStore** is a durable, append-only log of "this deliverable happened."
- The **board write is idempotent** (`report` / `record_verdict` by title).
- Therefore **reporting is an idempotent, replayable *projection* of the store onto the
  board** — Event *Sourcing* in spirit, not a message bus. It gives every property we wanted
  with **zero infra and zero worker thread**: never blocks production (report is
  fire-and-continue), never deferred to approval (stream after each), survives failure
  (re-run reconciles from the store). "Mediator now, Event-Queue later" holds — later is
  still later (a long-lived orchestrator daemon would be the trigger).

## What happened

The fix is a **policy**, made concrete as a flag. `deliver_plan.py` and `audition.py` gained
**`--report`** (+ `--board <path>` for the local double): after each deliverable is filed to
the store, it is **streamed to the board immediately**, tagged with its authoring seat +
department, and the board write is **non-fatal** — on failure it logs and continues, because
the store still holds the truth.

## Proven end-to-end, offline

A throwaway harness (`output/testing/policy_e2e.py`, gitignored) drove the **real**
orchestration (`Director.deliver_plan` / `Director.audition` → `Gate` → store →
`provider.report`) with a fake still renderer + a `LocalFolderProduction` board double — no
gpt-image, no ADO:

1. **Provision first** — the board exists, empty.
2. **Stream plan** — `treatment` (Story) + `poster` (Art) appear the instant each lands.
3. **Stream audition** — each candidate (Casting) appears as it renders; board grows to 5.
4. **Board outage** — pointing the board at an unwritable path raised `PermissionError` on
   every write; the arm **continued** and the store **kept every artifact** (non-fatal).
5. **Reconcile** — the AD arm replayed the store onto the board idempotently; all 5 items
   whole again.

## Decisions

1. **No queue, no infra.** The store is the log; reporting is its idempotent projection.
2. **Board writes are non-fatal.** Production never stalls on documentation; the store is the
   source of truth and reconcile is always available.
3. **Provision-first is step 0.** The projection needs a target; the (cheap) board is created
   before the first subagent.
4. **Streaming lives in the arms** (`--report`), not a new component — the policy is a flag,
   not plumbing.

## Resulting state

- **Code:** `--report` / `--board` on [`deliver_plan.py`](../../scripts/deliver_plan.py) +
  [`audition.py`](../../scripts/audition.py) (stream-after-each, non-fatal, seat/dept routing).
  No `sequitur/` change; the 12-module suite is unaffected.
- **Proven:** the offline harness shows the full policy (provision → stream → outage →
  reconcile). The live run is the *same commands* with an ADO board + real renders.

## Next (the live end-to-end, on the Producer's go)

1. Provision `TheAudition` first (cheap; board appears empty).
2. `deliver_plan.py … --report` (treatment + poster stream to the board as they render).
3. `audition.py … --report` (candidates stream as they render).
4. Producer reviews the *live* board, selects, records the verdict; a `report_to_board.py
   --phase plan` reconcile trues up anything a transient board outage dropped.
- Watch: the AD's filename-based routing still leaves dynamic `Name-candidate-N.png` frames
  under a default department unless routed — a small Casting rule is the follow-on.
