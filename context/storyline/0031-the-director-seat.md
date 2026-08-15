# 0031 — The Director Seat (agents as the persona tier)

> Date: 2026-08-14 · Focus: **agent-customization** — answered "what executes the
> direction?" by putting the conversational agent in the **Director** seat and the crew in
> **dispatchable subagents**. The `.github/agents/` layer is the **PersonaJudgment (B)** tier,
> sitting beside `sequitur/`'s deterministic **HeuristicJudgment (A)**. Proved the
> dispatch→reconcile round-trip live. No `sequitur/` code changed.

---

## What happened

- **Named who executes the direction.** The three tiers (`0008`) get concrete runtime homes:
  **Producer = the human** (HITL — brief, greenlight, taste); **Director = the orchestrating
  conversational agent** (me) — *not* a peer in the swarm, but the one that conducts the
  discourse and directs; **Crew = department subagents**, each owning a closed grammar slice.
  A subagent is stateless and task-scoped; the Director *is* the conversation — which is why
  the Director can't be a `runSubagent` peer.

- **Built the first two seats** in [`.github/agents/`](../../.github/agents/): a
  **`director.agent.md`** (grounded in Directing — interprets the brief, dispatches the crew,
  reconciles their disjoint field slices into one `Shot`, reports back for greenlight) and a
  **`cinematographer.agent.md`** (the DP — grounded in Grammar of the Shot, reasons the camera
  slice, returns a typed `Contribution`).

- **Proved it live.** As Director, dispatched the Cinematographer with a lighthouse-keeper brief
  ("foreboding isolation; one person against vast nature"). It returned a **valid, grounded,
  vocabulary-bound** Contribution — `EXTREME_LONG` / `HIGH` / `REVERSE` / `WIDE` / `DEEP`,
  every field a real enum member, its notes citing Grammar of the Shot — which reconciled into
  a complete `Shot`. The seam works with no reload.

- **Settled the grounding-style fork with evidence.** The decision plane is **persona-bound**:
  the subagent reasons freely from grounding but its output is constrained to the code's closed
  enums (single source of truth = [`sequitur/crew/`](../../sequitur/crew/)). Subagents are
  **not** wired into the Python heuristics — decision-time needs only the *vocabulary*, not the
  code. `HeuristicJudgment` (A) remains the deterministic no-persona fallback.

## Decisions

1. **`.github/agents/` = the persona (B) tier; `sequitur/` stays the (A) scaffold + the seams.**
   Every `crew/<role>.py` class gets a `<role>.agent.md` twin: the code twin owns the
   *vocabulary + heuristic default*, the agent twin owns the *grounded judgment*. Nothing is
   duplicated — they're the two `Judgment` strategies of the same seat.

2. **Grounding style = persona-bound, not hybrid.** Free judgment from the reference, output
   bound to the enums. No code-wrapping at decision-time (proven unnecessary by the live run).
   The clean split is **judgment / schema / execution**, with decision-time and execution-time
   as separate code-touch points.

3. **Director = the orchestrating conversational agent, not a peer subagent.** Crew = subagents,
   Producer = human. A corollary already load-bearing: the Director suffers session amnesia, so
   **the devlog is the Director's continuity/memory** — the through-line of directorial intent.

## Resulting state

- Four agent files in [`.github/agents/`](../../.github/agents/) — `director` plus the full
  **shoot crew** (`cinematographer` · `gaffer` · `keygrip`), each grounded in its own source
  (Grammar of the Shot Ch. 1–3 / 4 / 6). All three seats were dispatched live on a shared brief
  and reconciled into one conflict-free `Shot`. The Director is user-invocable (a mode the
  Producer selects); the crew are subagent-only. **No `sequitur/` code changed** — this is the
  customization layer, the B tier realized in VS Code's agent system.

## Open threads

- **Expand the crew** — shoot crew is complete (camera/electric/grip, proven live); next are the
  `editor` / `colorist` (assemble) and `screenwriter` / `storyboard-artist` (plan) seats.
- **Vocabulary drift** — the enums are the single source of truth, but the agents list them by
  hand. A generated per-role "vocabulary card" would keep the code authoritative.
- **Wire execution** — on greenlight, run the reconciled `Shot` through `build_prompt` → the
  renderer (a Director execute-hook), closing decision → pixels.
- **Bind to the board** — a brief read from the `ProductionProvider` → Director → `Shot` →
  written back, so the persona tier drives the same board-to-board loop the engine already runs.
