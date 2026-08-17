# 0058 — The approvals loop: recording the Producer's verdict on the board

> Date: 2026-08-16 · Focus: the Producer resolved the 0057 conditioning forks and named the
> real gap — **the approvals still haven't materialized.** This session records those
> decisions and builds the keystone: `ProductionProvider.record_verdict` — the Producer's
> approve/revise, written back onto the board item's State. It is the verdict half of the
> dailies loop (deferred since 0040) and the substrate the overflow policy rides on.

---

## The fork decisions (Producer's call, 0057)

1. **Conditional depiction (fork 1):** *select the chosen character design and then lock it.*
   → **One locked selected design per Character** (the audition → select → lock already built
   in 0055). Identity is held by **state**, not by a library of keyed references — so no
   multiple-references-per-Character model. Conditions (wet, wounded, aged) are driven in the
   prompt over the single locked identity.
2. **Omni consistency (fork 2):** *both stateful but mindful of the budget.* → Use **both**
   levers together: the **stateful** thread (`previous_interaction_id`, establish once and
   carry forward) **and** the reference-image budget — while respecting the ~4–5 character-ref
   cap. Neither alone; combined, budget-aware.
3. **URL→bytes (fork 3):** *the graph output should be resolved to provide the share links as
   initially proposed.* → Wire **`GraphOutputStore`** so the durable ref is the authoritative
   **share URL** (the 0038/0053 design), and conditioning **fetches bytes from that URL** when
   it needs to seed a render. The board links stay authoritative; the edits/`input` inputs
   resolve from the same URL.
4. **Overflow (fork 4):** *executed in ADO with the approvals — which still haven't
   materialized.* → When a scene has more principals than the character-ref budget, the
   **Producer decides on the board** (approve which to prioritise). That decision rides the
   **approvals loop** — and the approvals loop was the missing piece. So it is built first.

## What happened

The verdict was always modelled as *data* — `Deliverable.approve()` / `.revise(notes)` return
new immutable versions (0040) — and `report()` even mapped a deliverable's `GateStatus` onto
the board State on write. But there was **no first-class, tested operation to record a verdict
back onto an already-reported item**: no protocol method, no notes-preserving update, nothing
the AD/PA arm could call. Re-`report()`-ing worked but re-wrote the whole item (and could clobber
the body). So the approvals loop existed on paper but had never *materialized*.

`ProductionProvider.record_verdict(deliverable)` closes it:

- **Protocol:** a third board-write verb beside `report` / `fetch_reports`.
- **`AzureDevOpsProduction`:** locates the item by title and **PATCHes only `System.State`**
  (approved → Done, revise → Doing) plus the revise note as a `System.History` discussion
  comment. The content the report wrote (Description, attachment, hyperlink) is untouched — a
  verdict changes *standing*, not *substance*. If the item isn't on the board yet, it files it
  first (carrying its verdict), so a verdict always lands.
- **`LocalFolderProduction`:** updates the reported record's status + notes **in place**,
  preserving its `body` — the same semantics, offline.
- **AD/PA arm + skill:** `report_to_board.py` gains `--approve <name>` / `--revise <name>
  --notes …`; the skill's "two directions" becomes **three** (report up · **verdict down** ·
  fetch down). The Producer decides; the AD *records* — it still never owns the decision.

## Decisions

1. **A dedicated `record_verdict`, not re-`report()`.** A verdict must not rewrite content;
   State-and-notes-only is the correct, non-destructive operation, and naming it makes the
   approvals loop first-class (the thing the arm and skill call).
2. **Idempotent, self-healing.** Locate-then-patch; file-first if unreported. A verdict is
   always recorded, never lost, never duplicated.
3. **`System.History` for the revise note.** A work-item PATCH to `System.History` appends a
   discussion comment — the note lands as an on-the-record remark, not a clobbered field.
4. **The AD records; the Producer decides.** The loop keeps the authority tiers intact
   (Producer = verdict, AD = messenger).

## Resulting state

- **Code:** `ProductionProvider.record_verdict` on the protocol + both backends
  ([`production.py`](../../sequitur/production.py)); the AD arm's verdict mode + skill doc.
- **Tests:** [`test_production.py`](../../tests/test_production.py) 10 → 13 — approve writes
  the verdict and **preserves the body**; revise carries its notes; a verdict on an unreported
  deliverable files it. **12-module suite green.**
- The dailies loop is closed in code: file (Gate 0040) → report (AD 0049) → **verdict (0058)**.

## Next

- **Wire `GraphOutputStore` live** (fork 3): point a production's `OutputStore` at Graph so
  refs are authoritative share URLs, and add **fetch-then-condition** (resolve URL → bytes) for
  the still/video seeds.
- **The Omni video path** (fork 2): teach `Studio` the multimodal `input` list + the
  `previous_interaction_id` stateful thread, budget-aware to the ~4–5 character cap.
- **Overflow policy** (fork 4): surface a budget-exceeded cast to the Producer as an
  approvals decision (now that the loop exists).
- **Live proof:** exercise `record_verdict` against the real ADO board (offline double proven).
