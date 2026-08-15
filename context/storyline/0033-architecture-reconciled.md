# 0033 — The Architecture Reconciled to the Pivot

> Date: 2026-08-14 · Focus: **docs** — brought [`context/architecture.md`](../architecture.md)
> up to the pivot. The doc still opened with "the studio implements **one department in one
> phase**," framed post-production as "the next layer," called the runtime model "not yet
> built," and described `PersonaJudgment` only in the abstract. It now reflects where we
> actually are — and installs **the pivot** as a first-class architectural axis. No code.

---

## What happened

- **Named the pivot in the doc.** The headline change of `0031`–`0032`: the crew engine's
  swappable `Judgment` has **two concrete runtime homes**, and `sequitur/` stops being "the
  studio." Added a new section — **The two Judgment tiers — `sequitur/` (A) and
  `.github/agents/` (B)** — with its own diagram:
  - **Tier A = `sequitur/` (code)** — `HeuristicJudgment` + the **enum schema** (the closed
    answer space), the **execution** plane (`build_prompt` → renderers, the `Grader`), and the
    **seams** (`Renderer`, `ProductionProvider`). The offline / CI fallback.
  - **Tier B = `.github/agents/` (personas)** — `PersonaJudgment`, one `<role>.agent.md` twin
    per `crew/<role>.py`; reasons freely from `reference/`, output **bound to the code's enums**.
  - **The Director is the conversational agent**, not a code object nor a subagent — it
    dispatches the crew subagents, reconciles, and on greenlight runs the **execute-hook**
    (`0032`). The code `Director` is the A-tier reconciler + hook.

- **De-staled the authoritative cells.** The intro now says the studio spans **two phases in
  code** (shoot + assemble), driven by a real crew engine, bound to a live ADO board, rendering
  **real bytes** across four media. The phase headers flipped: *shoot* = "implemented (crew
  engine)", *assemble* = "now implemented (`0022`–`0023`)". The "Reading the map" post-layer
  line no longer claims the cut engine is "not yet built."

- **Runtime section caught up.** The runtime model is no longer "not yet built": the
  `ProductionProvider` seam + its **Azure DevOps** board are **built** (`0024`–`0028`), the
  platform question (`0005`) is **resolved (ADO)**, and the remaining piece is named as the
  Graph-backed `OutputStore`. Rewrote the two open-decisions bullets (provider seams DONE,
  production-store platform RESOLVED) and folded the now-built "post layer" decision away.

## Decisions

1. **Add the pivot as a third dimension, don't rewrite the craft tables.** The doc already
   maps *craft layers* × *runtime model*; the pivot is a **third axis** (which tier decides a
   layer). Installed it as one new section + a diagram rather than re-flowing the whole doc —
   the tables are still accurate as the *what*, the tiers are the *who-decides*.

2. **Keep the code class-diagram as-is.** `Role <|-- Director` and `PersonaJudgment` as a
   `Judgment` strategy are still true of the *code* model; the new section carries the
   conversational-agent nuance (the acting Director isn't a `runSubagent` peer).

3. **Docs-only, per the process rule.** This is a reconciliation pass — the abridgement/design
   sessions taught us to keep those separate from code; the same applies to a doc catch-up.

## Resulting state

- [`context/architecture.md`](../architecture.md) now reflects the built crew engine (shoot +
  assemble), the live ADO board + `ProductionProvider`, the four-medium renderer seam, the
  execute-hook, and — as a first-class section with a diagram — **the two Judgment tiers** and
  the conversational-agent Director. OVERVIEW's architecture bullet updated to match. No
  `sequitur/` code changed; the 33-test suite is untouched.

## Open threads

- **Expand the agent crew** — assemble seats (`editor` / `colorist`) + plan seats
  (`screenwriter` / `storyboard-artist`), then a generated **vocabulary card** so the enums
  stay the single source of truth (`0031` drift thread).
- **Bind the execute-hook to the board** — `read_brief` → Director → `Shot` → **execute** →
  record the output `ref` back (an `OutputStore` seam, `0005`), unifying the persona tier with
  the board-to-board loop (`0027`).
- **A-tier deepenings** — per-shot grade matching (CCH Ch. 9), `write` State transitions, a
  `--render` flag on `scripts/produce.py`.
