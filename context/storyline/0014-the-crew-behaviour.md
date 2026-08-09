# 0014 — The crew makes choices: Judgment, the Director, and a dumb Engine

> Date: 2026-08-08 · Focus: the third crew-engine pass (`0008`) — give the seated
> roles **behaviour**. Roles stop being namespaces and start *choosing*: a swappable
> `Judgment`, a `Contribution`, a `Director` reconciler, and a dumb `Engine`. A
> **code** entry; the shoot-phase crew now assembles a complete `Shot` from a brief.

## What happened

`0012`/`0013` seated the vocabulary under roles but left them inert. This pass wires
the A→B seam and the dispatch loop so the crew actually produces a decision.

1. **`Judgment` — the swappable reasoning strategy**
   ([`crew/judgment.py`](../../sequitur/crew/judgment.py)). A `Judgment` ABC with one
   `decide(role, brief) -> Contribution`; `HeuristicJudgment` (**A**) is the first
   concrete — deterministic, delegating to the role's own default. `PersonaJudgment`
   (**B**, LLM) and `HumanJudgment` (HITL) are future concretes with the same
   signature, so any single role can be upgraded or hand-driven individually.

2. **`Brief` + `Contribution`** ([`crew/role.py`](../../sequitur/crew/role.py)). The
   `Brief` is the producer's context (scene + `hints` overriding a role's defaults +
   pass-through mood/audio/aspect); a `Contribution` is one role's proposed slice.
   `Role` gained `propose(brief)` (delegates to its `Judgment`) and `heuristic(brief)`
   (its deterministic default — the **A** the default judgment uses).

3. **Department heuristics.** Each shoot-phase role now chooses its *owned* fields:
   the **Cinematographer** picks framing defaults (`MEDIUM`, `EYE_LEVEL`, objective,
   rule-of-thirds), the **Gaffer** lighting (`THREE_POINT`, soft, neutral), the
   **Key Grip** motion (`STATIC`) — each reading `Brief.hints` for producer overrides.

4. **`Director` — the reconciler** ([`crew/director.py`](../../sequitur/crew/director.py)).
   Itself a `Role` (dept `DIRECTION`), but its job is to merge the crew's
   contributions into a `Shot`. Because the departments own **disjoint** slices of
   the shot, the merge is conflict-free. "Agency in a component, not the container."

5. **`Engine` — dumb dispatch** ([`crew/engine.py`](../../sequitur/crew/engine.py)).
   Filters the crew by the active `Phase`, collects each role's `Contribution`, hands
   them to the Director. No film logic. `shoot_crew()` returns the default trio;
   `Engine().run(Phase.SHOOT, brief) -> Shot`.

**End-to-end proven:** a `Brief` (scene + hints + mood) runs through the engine to a
complete `Shot` that renders via the existing `build_prompt` — the crew assembled the
shot the CLI used to require spelled out by hand.

## Decisions

1. **Heuristic lives on the role; the Judgment selects the strategy.** The role's
   `heuristic()` is its deterministic domain default (the **A**); `HeuristicJudgment`
   just uses it, while `PersonaJudgment` will ignore it for an LLM. This keeps the
   role's baseline knowledge with the role and the *strategy* swappable — the exact
   A→B seam, and it keeps the roles non-hollow (they make real, sensible choices now).
2. **Heuristics inject sensible defaults, not just echo the brief.** A crew that only
   passed the scene through would be pointless; the DP *picks* a framing, the Gaffer a
   scheme. Producer `hints` override any default per field. This is what makes the
   crew worth having.
3. **Shoot phase only, honestly.** The Director reconciles to a `Shot`; the assemble
   phase (Editor over clips → a `Sequence`, wrapping `validate()`) is a different
   context and is the *next* behaviour slice — not faked here. `Editor` keeps the base
   empty `heuristic` and stays out of `shoot_crew()`.
4. **No Production yet.** `run` takes a `Brief` directly; binding role state to a
   per-instance Production via the `0005` provider is deferred (the container comes
   after the loop is proven).

## Resulting state

- The crew engine's behaviour layer works: `Judgment`/`HeuristicJudgment`, `Brief`/
  `Contribution`, `Director`, `Engine`/`shoot_crew` — all exported. `Engine().run`
  turns a brief into a grammar-complete `Shot`.
- New guard test [`tests/test_engine.py`](../../tests/test_engine.py) (default
  assembly, hint overrides, disjoint slices, swappable judgment). All three suites
  green (prompt 3 · edit 4 · engine 4); no lint errors.

## Open threads

- **Assemble-phase behaviour** — an Editor `heuristic`/judgment over a set of clips
  producing/validating a `Sequence`; a phase-aware Director (shoot→`Shot`,
  assemble→`Sequence`). Wrap `Sequence.validate()` as the Editor's first heuristic.
- **Bind a Production (`0005`)** — swap the bare `Brief` for role state read/written
  through a local-folder `ProductionProvider`; then the PM-board binding.
- **`PersonaJudgment` (B)** — back one role's `Judgment` with an LLM over its scoped
  grounding, once A has proven the seam (it now has).
- **`Renderer` protocol** (deferred `0006`, three backends) — still independent.
- Carried: `SoundMixer` behaviour; the reconciliation sweep; toaster-strudel MCP
  (`0009`); the cut-decision engine (`0007`).
