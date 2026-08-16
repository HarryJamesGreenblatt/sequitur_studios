# 0050 — Board-record remediation: placement, provenance, and real links

> Date: 2026-08-16 · Focus: the deliverables the AD/PA filed landed as *placeless* work
> items (root area/iteration, no author, a local filepath string for the artifact). Fix the
> `report()` mechanism so a deliverable lands in its **department area** on the **phase
> iteration**, tagged with its **authoring seat**, linked by a real **https** URL. **Code;
> reprovisioned + verified live on `TheLaunch`.**

---

## What happened

The `0049` board loop worked but the *records were thin* (Producer's critique): general work
items with no area/iteration placement, no trace of which seat authored them, and an
artifact reference that was a raw local filepath. This session fixes the record — the
mechanism, not the sample.

1. **Provenance on the `Deliverable`.** [`gate.py`](../../sequitur/gate.py)'s `Deliverable`
   gains `author` (the seat) and `department` (the board Area Path) — captured when the
   deliverable is produced/collected, carried to the board.

2. **`report()` places, tags, and links.** [`production.py`](../../sequitur/production.py):
   - **AreaPath** ← `deliverable.department` (`TheLaunch\Story`, `TheLaunch\Art`).
   - **IterationPath** ← the phase, via a `_PHASE_ITERATION` map (`plan → 1 🎬 Pre-Production`).
   - **Tags** ← the authoring seat (subagents aren't ADO identities, so a tag is the honest
     trace, not `AssignedTo`).
   - **Hyperlink** ← a real **https** link via a new `config.store_url()` mapper
     (`OUTPUT_STORE_ROOT` local path → `OUTPUT_STORE_URL_BASE` SharePoint URL), plus the
     image still pinned as an attachment. No more filepath strings.

3. **Story + Art departments.** The provisioner's `DEPARTMENTS` was the original seven
   (shoot/post only); the plan seats (Screenwriter → **Story**, Production Designer /
   KeyArtist → **Art**) had no area to land in. Added both, mirroring the code `Department`
   enum.

4. **The AD's routing knowledge.** [`report_to_board.py`](../../.github/skills/assistant_director/report_to_board.py)
   gains a routing map (`treatment.md → Screenwriter/Story`, `key_art.png → KeyArtist/Art`) —
   coordination metadata (which seat owns which deliverable type), not creative content.

## Decisions

1. **Author as a tag, not an assignee.** Crew subagents have no ADO identity, so tagging the
   seat is the truthful provenance; `AssignedTo` would be a lie.
2. **Links via a deterministic path→URL map**, not the Graph API. The store is
   OneDrive-synced and SharePoint-exposed, so mapping the local root to the https base is the
   "URL later" `0038` promised — no API call, just a config pointer.
3. **Routing is metadata, not cooked output.** The AD legitimately knows the production's
   structure (who produces what); a name→seat/dept map is its schedule, not hand-authored
   content.

## Resulting state

- **Reprovisioned `TheLaunch`** (deleted + recreated) with nine departments including Story
  and Art; re-ran the AD arm. **Verified live:** `#16 treatment` → `Story` / Pre-Production /
  tag `Screenwriter` / https link; `#15 key art` → `Art` / Pre-Production / tag `KeyArtist` /
  attachment + SharePoint Hyperlink. `test_production` covers the provenance round-trip; suite
  green.

## Next — the coherence pass (the *content*, not the record)

The record is right; the **content isn't yet honest**. The treatment on the board is still a
placeholder and the key art still omits the protagonist (the "separate chambers" problem).
Next: **thread the treatment through the pipeline** (story-first, seed the PD and KeyArtist
with it) and **re-dispatch the real subagents**, so the board fills with coherent,
genuinely-authored deliverables — no cooking.
