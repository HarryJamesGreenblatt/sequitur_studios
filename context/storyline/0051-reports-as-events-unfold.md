# 0051 — Reports as events unfold: the coherent re-run, on the record

> Date: 2026-08-16 · Focus: fix the two failures the first `TheLaunch` run exposed — the
> **separate-chambers** incoherence (treatment and key art disagreed) and the **vacuum**
> (the whole plan ran in chat with no board record). Re-run the plan with the treatment
> *threaded* through every seat and the **AD/PA reporting each department to the board the
> moment it lands**. **Orchestration + a one-line routing addition; no engine change.**

---

## What happened

The prior `TheLaunch` run had two honest defects (both caught by the Producer): the key art
dropped the protagonist (the PD's metaphor abstracted the human out, and the KeyArtist
worked from the concept, not the story), and *none of it was recorded on ADO* — the
Producer sat at an empty board taking the Director's narration on faith ("how would I know
you didn't cook it?"). Both are process failures, not model failures.

1. **Coherence by threading, not prompting.** The fix was the *dispatch order and data
   flow*, not a better prompt. Story first: the **Screenwriter** authored the descriptor +
   treatment + copy (a named protagonist, **Mara Quinn**, her AI **Sol**, a concrete final
   image). Then the **Production Designer** was dispatched *seeded with the treatment* (not
   just the descriptor) — so its concept kept Mara the warm human subject against the cold
   machine glow, agency in her hand. Then the **KeyArtist** (a Skill, pattern (a)) was
   seeded with *all three* — treatment + concept + copy — and locked the frame to Mara
   reaching toward the crayon sun, Sol as surround glow + a deferring cursor. The re-rendered
   one-sheet is coherent with the film: it is *her* story. No content was hand-authored; each
   seat reasoned from the real upstream artifact.

2. **The AD/PA reports as events unfold.** Each department's verbatim output was filed to
   the store and **immediately reported to the board** by the AD arm — Story (copy #17,
   treatment #18), Art (concept #19, directive #20, key art #21) — each placed in its
   department area, on the Pre-Production iteration, tagged with the authoring seat, linked
   to the artifact. The board is now the **live, chronological audit trail**: the production
   accretes in view, and cooking is impossible because the record would contradict the chat.
   A one-line addition to the AD's routing map gave `concept.md` and `key_art_directive.md`
   their Art homes.

3. **The publish race, found and named.** The image **attachment** (ADO-hosted bytes) is
   instant and authoritative; the SharePoint **hyperlink** is *eventually* consistent —
   Tier-0 stores the file in a OneDrive-synced folder and the AD posts the URL before the
   desktop client has published the overwrite, so the link briefly serves the stale blob
   (verified: the URL is correct; only the cloud content lagged, then caught up). Both
   references have value (instant vs. durable); the confusion is transient.

## Decisions

1. **Threading is orchestration now, code later.** The conversational Director threads the
   treatment into each dispatch by hand. The *code* seam — `Plan.story` carrying the
   treatment so a headless runtime auto-seeds the design seats — is the future automation
   step, not built here.
2. **No interim churn on the link.** Since the hyperlink is eventually-correct and the
   attachment covers the instant case, removing the durable link would hide the problem, not
   fix it. Keep both.
3. **`GraphOutputStore` is the real fix (queued).** File bytes through the Microsoft Graph
   API and return an authoritative share URL only after upload completes — no dependence on
   the sync client's timing. This is `0038`'s deferred "URL later," now with a concrete
   motivating bug.

## Resulting state

- **A coherent, fully-recorded plan phase on `TheLaunch`** — five department reports, placed,
  authored, linked; the one-sheet finally agrees with the treatment.
- The AD/PA is doing its real job: the board as the live log, provenance on every event.

## Next

- **The verdict loop:** the Producer approves/revises on the board (or in chat) and the AD
  writes the State back — the two review surfaces stay in sync.
- **`GraphOutputStore`** — authoritative artifact URLs, closing the publish race.
- **Code the threading seam** — `Plan` carries the treatment so the design seats auto-seed
  (the step toward a headless `PersonaJudgment` runtime).
