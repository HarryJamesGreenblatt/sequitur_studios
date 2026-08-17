# 0060 — The audition arm: a live entry point for casting

> Date: 2026-08-16 · Focus: the connective tissue for an end-to-end casting run. A
> readiness check for the "delete TheLaunch, reprovision a *mysterious audition*" test
> found the plan/copy slice runnable but the **casting slice had no live entry point** —
> `Director.audition` / `Character.select` existed with no CLI to drive them. Build the
> **audition arm** and wire the plan CLIs to the fork-3 store factory. Local only; nothing
> deleted, nothing live.

---

## Why

The pieces of Casting Phase 2/3 all existed and passed offline — `Director.audition`
(render candidates → Gate → lock, 0055), `Character.select` (the verdict), the Shot↔cast
conditioning (0056–0057), the share-link store (0059) — but **nothing runnable called
them.** `deliver_plan.py` files a treatment + poster and knows nothing of cast. So for a
pitch literally *about* an audition, the marquee capability couldn't be exercised end to
end. This closes that gap before any live/destructive reprovision.

## What happened

`scripts/audition.py` — the casting companion to `deliver_plan.py`. It reads a **cast
spec** (the Casting Director subagent's designed characters + candidate looks), and runs
the two-step casting workflow:

1. **Audition** (default): build `Character`s (with `Actor` candidates), run
   `Director.audition` on each — render every candidate's look through `ImageStudio`, file
   it at the `Gate`, lock its reference — then write an **audition-state JSON** (the cast,
   enriched with each candidate's durable reference) for the Producer to review.
2. **Select** (`--select "Mara=2"`): re-read the state, apply `Character.select` per
   1-based choice (the membership-checked verdict), and persist the chosen `cast` index.
   No re-render — the audition's locked references carry through.

`--dry-run` lists the audition (each character + its candidate prompts via
`build_character_prompt`) with no render or store, mirroring the other CLIs. Judgment
(which characters, which looks) stays the Casting Director subagent's; the arm is the
deterministic executor — the same judgment/execution split every seat uses.

Both plan CLIs now resolve their store through **`config.get_output_store()`** (fork 3):
`--store PATH` forces a local root, otherwise the configured backend is used — so a
production filed with `OUTPUT_STORE_BACKEND=graph` carries authoritative SharePoint share
links through the plan and the audition alike.

## Decisions

1. **A separate arm, not a flag on `deliver_plan`.** Casting is its own producer with a
   two-step (audition → select) rhythm and its own state; it earns its own CLI, parallel to
   `deliver_plan` (copy) and `produce` (assemble).
2. **Stateful via a cast JSON.** The audition and the selection are separate Producer
   moments; persisting the audition's locked references between them avoids re-rendering and
   models the real "audition, review, then cast" flow.
3. **1-based selection for the Producer, 0-based `cast` index in the file.** Human-facing
   choice is 1-based; the stored index matches Python.
4. **Thin CLI, no unit test.** The substance (`Director.audition`, `Character.select`,
   the store) is already covered by `test_casting` / `test_output`; the arm is orchestration,
   verified by `--dry-run` (like `generate.py` / `produce.py` / `deliver_plan.py`).

## Resulting state

- **New:** [`scripts/audition.py`](../../scripts/audition.py) (audition + select modes,
  cast-spec JSON codec, `--dry-run`, store factory). **Wired:**
  [`scripts/deliver_plan.py`](../../scripts/deliver_plan.py) resolves its store via
  `get_output_store()` (fork 3) with a `--store` local override.
- **Verified offline:** the audition dry-run composes correct per-character candidate
  prompts (honouring age/build/wardrobe/essence); select binds `Mara=1` / `The
  Adjudicator=2` and persists the `cast` index; `deliver_plan --dry-run` still composes the
  treatment + poster. 12-module suite unaffected (no `sequitur/` change).
- The casting slice now has a runnable entry point. The end-to-end *mysterious audition*
  test is unblocked — pending the Producer's go for the live/destructive parts.

## Next (the live end-to-end, on the Producer's go)

1. Provision a fresh `TheAudition` production (keep `TheLaunch` until this replaces it).
2. Dispatch Screenwriter / Production Designer / Casting Director subagents for the pitch →
   treatment, concept, cast spec.
3. `deliver_plan.py` (treatment + poster) → `audition.py` (render the audition) → Producer
   selects → conditioned key art on the locked lead → AD reports + records the verdict.
4. First live exercise of `record_verdict` (0058), the audition path, and — if
   `OUTPUT_STORE_BACKEND=graph` — the Graph share-link store (0059). Expect it to surface
   real integration issues (the 0050/0051 pattern).
- Known gap to watch: the AD arm's `_ROUTING` maps deliverables to a seat/department by
  exact filename; dynamic `Name-candidate-N.png` audition frames land unrouted — a Casting
  routing rule is a small follow-on.
