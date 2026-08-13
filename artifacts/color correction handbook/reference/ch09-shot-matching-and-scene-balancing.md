# Chapter 9 — Shot Matching and Scene Balancing

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 9.
> **Scope:** Making every shot in a scene read as one continuous space and time — matching **contrast, color, and quality** across angles by grading one anchor shot and matching the rest to it. Covers the client workflow, comparison tools (still store, split-screen, scopes), what to look for, how close is close enough, and recycling grades. This grounds the future Colorist's *color-continuity* function across an edit.

## Core idea

Shot matching is the most time-intensive colorist task: even one passing cloud drifts the light between takes, and unmatched brightness/color at a cut **accentuates the edit** and can read as a **continuity error**. The method is disciplined: pick one **representative (anchor/hero) shot**, grade it to define the scene's look, then match every other shot **to that single reference** — never shot-to-adjacent-shot, which drifts like a game of telephone.

## Heritage — color timing and printer points

- The photochemical ancestor is the **color timer** working a **color analyzer** (Hazeltine): **four controls only** — red, green, blue exposure + **density** (contrast). No per-zone color, no secondaries, no curves.
- Adjustments are **printer points** (c-lights), each a fraction of an *f*-stop; ~50-point range, 25 = neutral. This was the near-universal DoP↔lab language.
- Digital analogues: **Offset** color balance ≈ the RGB analyzer dials; **Exposure / Master Offset** ≈ density. Many apps also expose literal printer-point +/- buttons for DoP-supervised sessions ("give me two more points of red").
- Lesson: four controls balance a whole film — beginners should **stay on primaries** for a project or two before reaching for secondaries.

## Client workflow

- **Supervised throughout** — most efficient; turn and ask the DoP/director rather than guess and revise.
- **Sample-shots supervised** — grade 2–3 representative shots per scene *with* the client to set each scene's tone, then match the rest unsupervised. Save graded samples to the **still store** and "play through" them to confirm the scenes flow.
- **First day is slowest** — you're learning the client's aesthetic and their vocabulary; schedule for it.
- **Schedule review + revision** — grading is iterative; clients sleep on decisions. Bob Sliga's **two-pass** habit: a fast balance pass, then a detail pass. Play the finished program on **many venues** so real problems (common to all) separate from bad-display phantoms.

## Begin by balancing to an anchor

- Watch the scene through; pick the **most representative shot** (usually the master — most people + environment; sometimes a two-shot or key close-up).
- Grade it to lock **contrast ratio, exposure, color balance**; don't dwell (adaptation misleads). This becomes the **single reference** for all other shots.
- **Split the difference** when a scene mixes well- and poorly-exposed shots: *consistency beats beauty* — "editors cut for story; somebody else evens it out."

## Organize the adjustments

- **Balance + stylize in one grade** — fastest, fine for naturalistic/simple work; but if the style params also carry the balance, later restyles force a rebalance.
- **Balance first, stylize later** — first pass = neutral balance (avoid extreme moves that limit you); second pass = a separate **style** grade applied scene-wide. Buys cheap restyles; watch for shots with unique elements (a yellow shirt, a window the vignette must reframe) that need per-shot handling.

## How to match one shot to another

The core skill is **image evaluation** — spotting the difference; the adjustment is then easy. Three comparison methods:

- **Successive / flip** — jump edit-to-edit, loop across the cut. **Toggle a full-frame reference still on/off** to *out-race adaptation* — your eye rebalances to any cast if you stare, so flip fast. (Some suites keep a **white spot** to "wash out" the eyes.)
- **Split-screen** — wipe the division so a common element (skin, sky, sand) sits on each half for direct comparison; horizontal/vertical, pannable. **Multiple playheads / multiclip / Lightbox** extend this to whole-frame, scrubbable, side-by-side comparisons.
- **Still store / gallery** — one-button grab of an anchor frame; many apps also **store the grade** with the still so you can copy it as a match starting point.

## What you're looking for (in order)

- **Contrast first** (it changes how color moves): do the **black and white points** line up? How do **midtones / average lightness** compare? Adjust shadow/highlight/midtone contrast to align.
- **Color balance next**: flip and read the *overall* cast, not one element. Most temperature difference lives in the **highlights** (lighting-driven), some in midtones, little in shadows — *unless* a shadow imbalance is quietly poisoning the midtones. Watch dominant colors (an orange shirt, dry grass) skewing your read of scene temperature.
- **Saturation separately**: don't confuse "wrong balance" with "under-saturated." Pushing color balance to force a match adds a cast; ease the balance and **raise overall saturation** instead.
- **Check exceptions**: one vivid element (saturated red/yellow/magenta) present in one angle only — is it meant to pop, or does it need a **secondary** to "hammer the nail that sticks out"?
- **Wash, rinse, repeat**: contrast↔color interact; iterate quickly. Know when to stop — adaptation kills objectivity; use the **next-day rule** and let the review session catch the rest.

## Matching with scopes

- **Waveform (Low Pass) / YRGB parade** — contrast match: align bottoms (black), tops (white), middle cluster (midtones). A split-screen waveform shows both graphs; a perfect match reads as one continuous graph.
- **Vectorscope** — color: **offset from center** = color balance (matched shots offset same direction/distance); **arm angle** = an element's hue; **overall diameter** = saturation. Flip full-frame graphs to compare.
- **RGB / YRGB parade** — highlight/shadow balance: compare how the tops/middles/bottoms of R, G, B align; in an ideal match the *channel offsets* of both images agree.

## How close is close enough

- Aim for a **convincing** match — no shot sticks out on a casual viewing — not floating-point precision on every element (that costs hours nobody notices). **Perceptual match > numeric match**; a scope-perfect pair can still "not look the same," so trust flipped full-frame comparisons.
- Grade the **whole frame**, not just the subject. Some exposure difference between a master and its close-up is **deliberate** — subdue only enough not to blind the audience.
- **Don't over-match skin tones** — complexions genuinely differ; keep reference stills of each principal's ideal tone.
- **Break down to a secondary** for irreconcilable differences (a hazy-sky insert vs a blue-sky scene; a background/product that must match exactly — where scopes also *prove* the match).
- **Noise/grain**: sometimes color is matched but grain isn't — reduce noise, or *add* grain to a too-clean insert so it matches a noisier scene.

## Recycling grades

- **Angles of coverage** repeat (A master / B reverse / C close-up): copy A's grade to every A shot; B and C often start from A ("do I get lucky?") but usually need a tweak — don't over-polish a copy, restart if faster.
- **Doc talking-heads / recurring establishers / reality re-cuts**: keep a stash of grades; group and reuse — but don't hoard till you can't find the one you need.
- **Correction vs grade**: a correction = one primary/secondary (Resolve node / Baselight strip); a grade = the stack. Move grades via **copy/paste, drag-drop, bins/galleries/scratchpads/PowerGrade**, and **groups** that ripple a change across all like shots.
- **Manage style separately**: balance clips individually, then a **track grade / adjustment layer** applies one scene-wide look — restyle by editing a single grade, no per-shot rework (as long as the balance pass didn't clip/crush needed detail). Legal caveat: pushing a scene-wide look can knock individually-balanced shots back out of balance.

## Studio application

Provisional leads — the **Colorist** role and the **grade renderer** are not built yet.

- **Ch. 9 is the color analogue of the Editor's continuity check.** The edit layer asks "can these shots cut together?"; scene balancing asks the same question of **color**. Because the Omni renderer generates each ~10s `Shot` **independently** — no shared clock, no shared look — shot-to-shot color drift is *expected*, and reconciling it across an edit `Sequence` ([sequitur/edit.py](../../../sequitur/edit.py)) is exactly the Colorist's problem.
- **Strongest lead — a scene-balance pass = grade an anchor, then reconcile the rest.** Pick a hero/anchor `Shot`, grade it, and have a Colorist/Director step **match every other clip to that single reference** — the grade analogue of `Sequence.validate()`/continuity. This mirrors the Director reconciler ([crew/director.py](../../../sequitur/crew/director.py)) merging per-role contributions into a coherent whole, and overlaps the Editor seat ([crew/editorial.py](../../../sequitur/crew/editorial.py)) that owns cut continuity. The "match to one reference, never adjacent-to-adjacent" rule is a concrete guard against drift in that reconcile.
- **Grade renderer flavor = transform, on the Cutter execution plane.** The actual match is a per-clip **LUT/curve transform** over an already-rendered shot (ffmpeg/MoviePy — the `Cutter`, [sequitur/cutter.py](../../../sequitur/cutter.py)), not a regeneration. The anchor's saved grade = a reusable **Contribution** copied across clips (the "recycle grades by angle-of-coverage group" pattern → clips sharing a look).
- **Objective match wants a sensor/reader.** A scope-reader (waveform black/white points, vectorscope offset/diameter) can drive the match numerically and give a `HeuristicJudgment` its target; but keep the **perceptual > numeric** caveat — a `PersonaJudgment`/human check catches the "still don't quite look the same" that scopes miss.
- **Overlap to log:** color temperature lives in **two seats** — the Gaffer's capture enum ([crew/lighting.py](../../../sequitur/crew/lighting.py) `ColorTemperature`) vs the future Colorist's *grade*-time match — the same capture-vs-grade split noted for the color grounding.
