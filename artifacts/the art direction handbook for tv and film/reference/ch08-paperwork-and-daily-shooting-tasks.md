# Chapter 8 — Navigating Paperwork and Daily Shooting-Process Tasks

> Abridged from Michael Rizzo, *The Art Direction Handbook for Film & Television* (2nd ed., Routledge/Focal Press), Ch. 8.
> **Scope:** the art department's **logistics** — the schedules and lists that turn a script into a shootable plan, the roles that own each one, and the shooting-day discipline of "keeping ahead of the camera," cover sets, change/budget triage, and wrap. Abridged **hard** to the *process and roles* that matter; the paperwork-colour trivia (the rainbow of revision pages) is dropped. This is the chapter that maps least to a generative backend and most to an **Assistant Director / logistics** concern.

## Text becomes sets

The art department's core pipeline is a distillation: **script → script/design breakdown → set list → construction budget**. The pivot is the **set/design breakdown** — owned by the **Art Director**, one encapsulated page of vital data per set, derived from every scene. Everything downstream (the set list, the budgets) is generated from it, and it is only useful if **updated daily**.

## The schedule-and-list family

These artifacts look repetitive but each has a distinct owner and purpose. This is the "who plans what" table.

| Artifact | Owner | What it is |
|---|---|---|
| **Script / design breakdown** | Art Director | scene → set inventory with per-set data; the source of the set list + budgets |
| **One-liner schedule** | AD team | shorthand shooting order: day, scene, one-line description, time-of-day, int/ext, location, page count |
| **Shooting schedule** | UPM + 1st AD | the "**shooting bible**" — daily units of scenes, cast (principals / stand-ins / atmosphere), and each department's special needs |
| **Day out of days** | AD team | actor and special-equipment continuity across days (guards "hero detailing") |
| **Call sheet** | 2nd AD | the day's authoritative order — scenes, weather, location, who's needed; the **1st AD's signature** commits the day's budget |
| **Crew list** | production office | everyone, by department, head-first |
| **Director's plans** | art department PA | booklet of every set's **footprint** (ground plans), distributed at the final production meeting |

The **final production meeting** — 1st AD presiding, all heads present, an item-by-item walk of the one-liner and shooting schedule — is the gate between pre-production and principal photography. After it, "the camera stops only for holidays and emergencies."

## Keeping ahead of the camera

Once shooting starts, the Art Director's one job is to stay **far ahead of the shooting timeline** while feeding the crew's daily needs. The recurring disciplines:

- **Clearances & product placement.** Any logo, name, plate, address, or branded dressing in front of the camera must be cleared, or lawsuits follow. The Art Director supervises hero items *before* they shoot.
- **On-set presence & walk-throughs.** Opening a new set is a ritual walk-through with Designer and Director; the trick is to be the **first group to receive notes** so the art department finishes while other departments are still being briefed. Check standing sets for wear, missing dressing, and hazards — "nothing is too obvious to be triple-checked."
- **Cover sets.** Weather is one of the few things that can stop the schedule, so the art department keeps **fully-dressed interior cover sets** ready — established early in pre-production, sized to the location and season (shoot in Ireland and *every* interior is a cover set).
- **Communication with the Trinity** (Director, Cinematographer, UPM). Most mid-stream changes are acceptable; the Art Director's judgment is knowing which are **not** — and telling the truth, on the spot, with budget numbers at hand.

## Change and budget triage

The set list is **continuously modified** through production. The governing model is a triage of sets by importance:

| Tier | Treatment when change requests arrive |
|---|---|
| **Hero sets** | will almost certainly get extra work; budget for it |
| **Important-but-not-critical** | negotiable |
| **Dispensable** | first to cut in budgetary terms |

Every set-list item carries a **10–15% contingency cushion** to absorb repaints, duplicate builds, and *acts of God*. The archetypal drama is the tactical meeting: the Director decides ten days out that digital fire won't sell the emotion and wants a real house burned. Producer, UPM, construction, VFX/mechanical effects, accountant, and Art Director convene and trade options — full-scale duplicate ($374k) vs. a **quarter-scale miniature burned for real and composited** ($272k) — a "creative shell game" that shifts weight between physical build, miniature, and digital composite to satisfy the Director *and* the budget. Experience decides which option wins.

## Wrap

The Art Director runs at top speed to the last day, then **archives** — an ongoing process concluding in the art-department production manual and its database, plus the **wrap binder** (the "bible" for post-production and reshoots). **Reshoots** (led by the Second Unit Director, distinct from "pick-ups") are mini-productions of a few weeks; **sequels** reuse hero sets in storage and the previous show's research file, but guarantee nothing — "you're only as good as your last job."

## Studio application

- **Most of this chapter does not transfer — say so plainly.** A generative studio runs **no call sheet, no crew, no weather, no cover set, no 5 a.m. mill visit**. The daily human production management that fills this chapter has no analogue in the pipeline. This is the arc's honest floor: Rizzo Ch. 8 is largely *out of scope* for [`ImageStudio`](../../../sequitur/image.py), and it maps — where it maps at all — to a future **Assistant Director / logistics** concern, not to the Production Designer's look work.
- **The set/design breakdown *is* the studio's scene→shot inventory.** Rizzo's "distil the script into a per-set breakdown, then a set list" is exactly the enumeration [`production.py`](../../../sequitur/production.py) performs when it turns a production into an ordered board of scenes and shots for [`render.py`](../../../sequitur/render.py). The Art Director's breakdown page is the pre-image of the production board ([storyline 0024](../../../context/storyline/0024-the-production-board.md)).
- **The one-liner / shooting schedule is the phase-ordered render plan.** "Which shots, in what order, with what per-department needs" is the shooting schedule; in the studio it is the **phase axis and board ordering** that decide what renders when. The schedule's job — a single authoritative sequence everyone works from — is the [Director's](../../../sequitur/crew/director.py) reconcile made durable.
- **Change triage maps to render budget and priority.** "Hero / important / dispensable" is a **regeneration-priority** ranking: which shots earn a fresh, high-effort render and which are left as-is when intent shifts. The 10–15% contingency and the burn-the-house shell game are the physical-world version of a decision the studio makes for nearly free — *which* image is worth re-rendering — which is precisely why cheap iteration changes the economics ([storyline 0006](../../../context/storyline/0006-renderer-seam-and-image-backend.md)).
- **Archiving and the wrap binder are the OutputStore.** The Art Director's discipline of filing every artifact durably for post and reshoots is what [`output.py`](../../../sequitur/output.py) already does — every render persisted under its production and phase ([storyline 0038](../../../context/storyline/0038-the-output-store.md)). The wrap binder is a durable, queryable record of the show; so is the store.

This chapter is the **last of the Rizzo reference set**. With it, arc C — the *physical, historical, and logistics* half of *The Art Direction Handbook* — joins the design-process and digital chapters to complete the studio's dedicated grounding for the planned **Production Designer** seat over [`ImageStudio`](../../../sequitur/image.py). See the [book index](../INDEX.md) for the full chapter → seat map.
