# Chapter 7 — Production Mic Technique

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 7.
> **Scope:** boom, lavaliere, and wireless technique for capturing dialog on set —
> and the **dual-mic** strategy that leaves the keep-vs-replace decision to post.

## Core idea

**Bad dialog recordings are forever** — you fix them at the shoot or you loop them
(ADR), and looping always compromises the performance. A **$15 mic used correctly
beats a $3,000 camera mic**. The preference hierarchy: **boom overhead → boom
below → plant mic → wired lav → wireless lav**, and a **wired lav always beats a
wireless one** of the same element.

## Boom

Hypercardioid or short shotgun on a rigid pole, **above and in front, pointed at
the mouth, as close as the frame allows** — 30 inches is often *too far*, and
closer is always better. Perspective is a subtle lever: move out a little on wide
shots (more room), in on tight shots (less echo), but keep the **volume
consistent**. Control footsteps by keeping the mic close to the mouth and the
null toward the floor. Operating a boom is a **physical skill** — half a day of
practice minimum.

## Lav

Small omni electret, mounted **close to the mouth**, wired (phantom) beats
wireless. Hide it with tape triangles and a strain-relief loop; route the cable
**down a pant leg, not to a floor connector**; avoid synthetics (clothing noise).

**Multiple lavs are never mixed together** (hollow, muddy) — record each to its
**own track and choose per edit**.

## Wireless

A mic *plus* a radio link — added cost, complexity, and interference risk. Use
**UHF with diversity reception and frequency agility**; set the transmitter so the
limiter just catches the loudest line, and **don't crank the transmitter** (it
distorts). Rig the antenna to wardrobe, not skin (RF absorption). Always carry a
**wired backup**. The 700 MHz band is illegal in the US.

## The dual-mic strategy (the load-bearing idea)

Record **boom and lav to separate tracks simultaneously** and **choose in post** —
boom for its natural perspective, lav for intimacy or when the boom can't get in.
Also always grab **room tone** (1 min, same mic/levels) at the end of a location
for filling edits and patching ADR.

## Studio application

Provisional leads for the studio's sound layer:

- **The dual-mic "capture both, choose later" pattern is the model for the
  keep-Omni-take-vs-ADR seam.** Just as a mixer records boom+lav on separate
  tracks and defers the choice, the studio keeps the generated **diegetic
  dialog** as the primary and holds a **TTS/ADR fallback** (`SpeechRenderer`) as
  the alternate take — the `SoundMixer` role owns the keep-or-flag judgment (the
  "keep diegetic dialogue, TTS as fallback" decision from `0007`).
- **The mic hierarchy is the role's preference ordering.** "Wired beats wireless,
  boom beats camera mic, closer beats farther" is exactly the kind of scoped,
  ranked heuristic `HeuristicJudgment` encodes before any LLM persona is added.
- **"Never mix multiple sources; keep separate tracks and choose per edit"**
  becomes an assembler rule: candidate audio takes stay as distinct tracks/stems
  until the mixer commits (ch. 10, 17).
- **Room tone as an always-captured asset** is an invariant the pipeline should
  enforce — the bed that ch. 13's dialog editor depends on.
