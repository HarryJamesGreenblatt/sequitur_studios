# 0032 — The Execute Hook (decision → pixels)

> Date: 2026-08-14 · Focus: **code** — closed the top `0031` open thread by giving the
> **Director** an **execute-hook**: a greenlit `Shot` runs through the renderer registry to
> real bytes. The persona tier can now *decide* **and** *do*. One small method, one guard
> test; all 33 smoke tests green.

---

## What happened

- **Built `Director.execute`** ([`sequitur/crew/director.py`](../../sequitur/crew/director.py)):
  `execute(shot, *, medium=Medium.VIDEO, out_path=None) -> RenderResult`. It resolves the
  producer for `medium` from the renderer registry (`renderer_for`, `0021`) and hands it the
  Shot — which the backend composes through `build_prompt` internally. Reconciling *chooses*
  the shot; this hook *executes* it. The default medium is **video** (Gemini Omni — the
  studio's headline), with **still** (`gpt-image`) the other Shot-rendering medium.

- **The Director holds a renderer *by medium*, never a concrete class.** The hook goes through
  the `Medium`-keyed registry, so the Director stays backend-agnostic — the same swappability
  the `Renderer` seam already gives the execution plane. No new import cycle: `render.py` pulls
  nothing from `crew/` at module load (its factories are lazy).

- **Guard test** (`tests/test_engine.py`, now 6): register a credential-free fake producer for
  `Medium.STILL`, reconcile a Shot via the real `Engine`, `execute` it, and assert the *same*
  greenlit Shot and `out_path` reach the producer untouched — decision flows into execution
  with nothing lost. Restores the default factory in a `finally`. All 33 smoke tests green.

- **Updated the Director agent** ([`.github/agents/director.agent.md`](../../.github/agents/director.agent.md)):
  the old "DO NOT render — name it, don't fake it" constraint is now "DO NOT render *before
  greenlight*." On the Producer's greenlight the Director runs the execute-hook. The B (persona)
  tier and the A (code) tier now share the same decision → pixels path.

## Decisions

1. **The execute-hook lives on the `Director`, not the `Engine`.** The Engine is the dumb
   dispatcher (`run` / `assemble` / `run_production`); *executing* a reconciled decision is the
   Director's act (it already owns `reconcile`/`assemble`). A caller does
   `engine.director.execute(shot, …)` — no new Engine surface, no over-reach.

2. **No medium-policing in the hook.** The Director doesn't gate which media accept a Shot;
   the renderer contract does. Video and still are the Shot-rendering producers today; passing
   voice/film is a programming error the backend surfaces, not a boundary to guard here.

3. **Reuse, don't rebuild.** The hook is one line over existing seams (`renderer_for` +
   `Renderer.render`). No new export (`Medium`/`renderer_for`/`RenderResult` already public),
   no new dependency, no change to any backend.

## Resulting state

- `Director.execute` closes the `0031` "wire execution" thread. The crew engine now runs
  brief → crew → reconciled `Shot` → **rendered artifact** in-process; the Director agent
  (B tier) triggers the same hook on greenlight. `tests/test_engine.py` is 6, the suite 33.
  No new files in `sequitur/`; the change is one method + one test + the agent constraint.

## Open threads

- **Bind the execute-hook to the board** — the natural next step: a brief read from the
  `ProductionProvider` → Director → `Shot` → **execute** → and the output `ref` recorded back
  onto the board (an `OutputStore` seam, `0005`). This unifies the persona tier with the
  board-to-board loop the engine already runs (`0027`).
- **Expand the crew** — assemble seats (`editor` / `colorist`) + plan seats (`screenwriter` /
  `storyboard-artist`) as their own session(s); pair with a generated **vocabulary card** so
  the enums stay the single source of truth (`0031` drift thread).
- **A-tier deepenings** (deferred, refinements not gaps): per-shot grade matching (CCH Ch. 9),
  `write` State transitions, a `--render` flag on `scripts/produce.py`.
