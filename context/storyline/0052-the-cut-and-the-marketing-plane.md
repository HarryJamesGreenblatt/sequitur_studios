# 0052 — The Cut and the marketing plane: three planes, one keystone

> Date: 2026-08-16 · Focus: a **schema revision** provoked by a board-visibility bug. The
> `Deliverable` WIT wasn't showing on any board — and chasing *why* surfaced two genuine
> film-craft categories the architecture had conflated or omitted: the **market-facing
> plane** (key art is not a "deliverable") and the **diegetic crown** (there was no node for
> the *complete assembled work* — the **`Cut`**). Records the three-plane model before the
> process mutation. **Design + org-template change; no engine change.**

---

## What happened

The trigger was mundane: `Deliverable` work items were correctly authored, placed in
department areas, and assigned to iterations — yet nothing populated in **Boards** or
**Sprints**. Root cause (confirmed against the live process): the `Deliverable` WIT is
mapped to **no backlog level at all**. A type that isn't on a board-bearing level (a
portfolio level or the Requirement level; the Task level has no board) gets no Kanban board
and never surfaces in Sprint backlogs — regardless of how correctly area/iteration are set.
Area/iteration is orthogonal to *whether the type has a board*.

But "just map it to a level" begged the real question the Producer asked: **is a one-sheet
even a *deliverable*?** Pulling that thread found two things.

1. **The market-facing plane was missing.** Film artifacts fall into three planes, and the
   schema only modelled one-and-a-half of them:
   - **Diegetic (the work):** `Act → Scene → Beat → Shot` — the story world, internal-facing.
     Already modelled.
   - **Production deliverables (the film *becoming*):** treatment, storyboard, dailies,
     rough/final cut — *the same narrative at successive fidelities*. A storyboard panel **is**
     a Shot; a treatment **is** the act structure in prose. They trace back to the tree; the
     dailies/gate ritual reviews them. `Deliverable` is apt here.
   - **The campaign (about the film, for the market):** key art, one-sheet, trailer, EPK — a
     *new creative work whose subject is the film*, made by a different craft (creative
     advertising), for a different audience (the ticket-buyer), for a different purpose (sell,
     not tell). **Not the film at a stage.** The studio already half-knew this: `0048`
     deliberately refused to make the **KeyArtist** a crew `Role` ("key art = graphic-design /
     marketing ≠ production design"), seating it as a Skill *outside* the crew departments —
     but then dropped its output into the same generic `Deliverable` bucket, re-flattening the
     distinction. The structural tell: **key art has no Scene, no Beat, no Shot.** It anchors
     to the film *as a released title* — a different plane, not a missing leaf.

2. **The diegetic crown was missing — the `Cut`.** The narrative tree topped out at **Act**,
   a *structural* unit. There was no node for the **complete assembled work**. Yet the *code*
   already has one: in [`edit.py`](../../sequitur/edit.py) the editorial aggregate is
   `Clip → Beat → Scene → Act → Sequence` — `Sequence` is the crown, the assembled timeline —
   and the board had no analogue for it (`shot.py` `Shot` ↔ **Shot** WIT ✓; `edit.py`
   `Sequence` ↔ **nothing** ✗). The **`Cut`** (rough/fine/final — the craft term for the
   assembled whole) is that missing board analogue. It also fixes an earlier weak answer:
   when asked where editorial lands, `0030` said **Beat** ("the rhythm level"). That conflated
   two editorial senses — **the cut (verb)**, a per-join *transition* that genuinely applies at
   Beat/Shot, and **the Cut (noun)**, the *assembled whole* that had no home. Editorial works
   at **two altitudes**: micro (per-beat transitions) and macro (the assembled `Cut`).

The keystone is that `Cut` ties all three planes together: it is simultaneously (a) the
diegetic crown of the narrative tree, (b) editorial's first-class landing node, and (c) the
anchor both the rough/final-cut **deliverables** and the key-art **marketing** point back to
as "the whole film."

## Decisions

1. **`Cut` = the diegetic crown, a new top portfolio level** (`Cut → Act → Scene → Beat →
   Shot`). Phase-spanning like the other upper levels (`0030`): its **structure** is authored
   in *plan* (Screenwriter) and its **assembly** realised in *post* (Editor). Base model =
   **one `Cut` per production**; alternate cuts (theatrical/director's/streaming) are deferred
   (they'd become additional `Cut` items or `Deliverable` versions *if* ever needed — not
   built). States stay **To do / Doing / Done** for now (Doing = assembling, Done = locked);
   maturity-specific states (rough → fine → final → locked) are a future refinement, not worth
   the custom-state cost yet.
2. **Split the planes into distinct WITs.** Keep **`Deliverable`** for production/film-becoming
   artifacts (treatment, storyboard, concept, dailies, rough/final cut). Add **`Marketing
   Asset`** for the campaign (key art / one-sheet; room for trailer/EPK later), under a new
   **Marketing** area — mirroring how the KeyArtist seat sits outside the production crafts.
3. **Backlog level = altitude; Area Path = who works it.** Both review-artifact WITs
   (`Deliverable`, `Marketing Asset`) sit at the **Requirement level** — the working-leaf
   altitude that has a board — alongside `Shot`, and are separated onto **department boards by
   Area Path** (Camera sees Shots, Story sees treatments, Editorial sees the cut, Marketing
   sees key art). Their narrative *altitude* is expressed by which node they point at, not by
   their backlog level. This is also the original bug's fix: mapping `Deliverable` to the
   Requirement level is what finally gives it a board (and the surface the verdict loop needs).
4. **`Cut` is the only new narrative level.** The market-facing plane does **not** get its own
   portfolio level — it doesn't parent the narrative tree, so a portfolio level would falsely
   imply Marketing Assets are parents of Acts. Requirement-level + Marketing area keeps it
   honest without cluttering every team's level switcher.

## What got built (this pass)

The design above was implemented end-to-end against the live shared process:

1. **The process template, applied.** Created the **Cuts** portfolio level (rank 60, above
   Acts) + the **`Cut`** WIT (`icon_crown`, mapped default on Cuts); the **`Marketing Asset`**
   WIT (`icon_megaphone`); mapped **both** `Deliverable` *and* `Marketing Asset` to the
   **Requirement** level (non-default beside `Shot`) — the mapping that finally gives them
   boards. Each new WIT got To do / Doing / Done states.
2. **The template is now *codified*, not hand-built.** The org-level process (WIT types +
   icons/colours/descriptions + states + backlog-level mappings) had only ever been assembled
   by ad-hoc REST across `0024`/`0049`/this session — "tier 1" was never scripted. New
   [`scripts/provision_process.py`](../../scripts/provision_process.py) declares it and applies
   it **idempotently** (a `--dry-run` reports drift; a live run heals it). It sits beside
   [`scripts/provision_production.py`](../../scripts/provision_production.py) (which stands up a
   *project* on the process) and reuses its REST client. Running it healed real drift the
   screenshot exposed: `Cut`'s `icon_crown` had silently fallen back (fixed), `Shot`'s icon had
   become a megaphone (restored to a clipboard), and `Act`'s description still read "top
   narrative unit" (now "under a Cut").
3. **The provisioner learned the Marketing area.** `DEPARTMENTS` gained **Marketing** (10th
   area/team) and the example tree now crowns with a `Cut`. The custom-level visibility loop
   already picks up any `Custom.*` behaviour, so the new **Cuts** level auto-enables on every
   team — no code change needed there. Ran live on `ASequiturProduction`.
4. **Plane-aware routing.** [`production.py`](../../sequitur/production.py)'s `report()` now
   files a deliverable as a **`Marketing Asset`** when its department is Marketing, else a
   production **`Deliverable`**; `fetch_reports()` reads both planes back. The AD arm's routing
   map sends key art to the **Marketing** department (a campaign artifact, not production
   design). Verified live: a probe `Deliverable` and `Marketing Asset` landed as the correct
   types at the Requirement level (board-visible), then were cleaned up.

## Resulting state

- The three-plane model is **live on the board**: **diegetic** (`Cut → Act → Scene → Beat →
  Shot`), **production deliverables** (`Deliverable`, Requirement level, per-dept boards),
  **campaign** (`Marketing Asset`, Requirement level, Marketing area). The original
  invisibility bug is fixed (both review WITs now sit on a board-bearing level).
- The process template is codified + drift-free (`provision_process.py`), and every new
  production inherits the three planes for free.

## Next

- **The verdict loop** — now unblocked: the review artifacts finally have boards, so the
  Producer approve/revise → AD writes `State` back can land on a real surface.
- **Maturity states for `Cut`** (rough → fine → final → locked) if the To do/Doing/Done proxy
  proves too coarse.
- **`GraphOutputStore`** — **done** (`0053`), authoritative artifact URLs.
