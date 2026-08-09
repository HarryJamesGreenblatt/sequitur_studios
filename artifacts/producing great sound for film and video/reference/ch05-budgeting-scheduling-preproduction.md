# Chapter 5 — Budgeting, Scheduling, and Pre-production

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 5.
> **Scope:** what sound costs in cash and time, and how to scout a location with
> your ears. The producer-level resource decisions that gate everything the crew
> does on the day.

## Core idea

Sound is **faster and cheaper than picture — but not instant and not free.** The
governing constraint is the **Golden Triangle: fast, good, cheap — pick two.** The
cheapest, highest-leverage investments are *people and planning*: an experienced
mixer works fast and saves takes; an hour of pre-production saves a day in post.

## Where the money goes (order-of-magnitude)

| Item | Rough cost |
|------|-----------|
| Audio mixer/recordist | $350–600/day (brings own kit) |
| Boom operator | $200–350/day |
| Wireless lav rig | $45–150/day |
| Headphones | **~$5 — the most important item** (isolation lets you hear what's actually recorded) |
| Stock music | $15–100/cue; original $200–1,000/min |
| Audio post studio | $150–300/hr |

Time budgets scale with complexity: a 20-min corporate piece ≈ **1 day** of audio
post; a 1-hr documentary ≈ **1 week**. **Syncing after the edit is 3–5× slower**
than syncing during ingest — so decide sync strategy up front.

## Scouting a location — the three questions

1. **Is it quiet enough for dialog?**
2. **Does it have the right acoustics** (reverb, reflections)?
3. **Can the gear operate** without interference?

**Noise:** scout at the *same time of day* as the shoot (traffic, flight paths,
HVAC cycle all vary). The worst offender indoors is **HVAC** — turning it **off**
beats every other fix; if you can't, remove the grille (cuts noise ~50%) and
record room tone with it running. Check windows, doors, and **open plenums** above
suspended ceilings (sound bleeds across the building).

**Acoustics:** the **foam test** — sing "ahh" with a foam pad held in front of your
face, then without; a difference means reflections that will hurt the track.
Position matters more than room size: **distance + angle + absorption +
diffusion** beats facing a bare parallel wall. Treat with **sound blankets** (2"
off the wall) or Owens-Corning #703 fiberglass panels.

**Room tone:** record ~30–60 s with the set still before striking — insurance for
every later edit.

## Studio application

Provisional leads for the studio's sound layer:

- **The Golden Triangle is the Producer's (HITL) knob.** In the crew engine the
  **Producer = the human** owns what/whether; fast-vs-good-vs-cheap is precisely
  the brief-level trade-off they set, which then bounds the agent crew's choices.
- **"Sync strategy decided up front" is an architecture rule.** Because
  post-hoc sync is 3–5× costlier, the studio should carry timing/sync metadata
  with every generated take from the moment it's rendered (ch. 8, 12) rather than
  recovering it later.
- **Location scouting has a generative analogue:** the acoustic *intent* of a
  scene (quiet/dry vs. reverberant/live) is a parameter the `SoundMixer` role and
  the render prompt should set deliberately — the "room" a shot implies is part of
  its grammar, alongside *Grammar of the Shot*'s lighting and lens.
- Most concrete dollar/day figures are **reference-only context** for the
  Producer's human judgment, not values the code computes.
