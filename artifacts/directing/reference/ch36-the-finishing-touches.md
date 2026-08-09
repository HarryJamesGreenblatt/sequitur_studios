# Chapter 36 — The Finishing Touches

> Abridged from Michael Rabiger & Mick Hurbis-Cherrier, *Directing: Film Techniques and Aesthetics* (6th ed.), Ch. 36.
> **Scope:** The two aesthetic passes that survive picture lock — **color correction/grading** (with LUTs) and **finalizing the multi-track sound design** through spotting, dialogue splitting, and the mix — plus titles and credits.

## Core idea

After picture lock and score, it can feel as if only mechanics remain. Two arenas say otherwise: **color** and **sound**, each carrying real interpretive weight. Color splits into a technical repair pass and an expressive **look**; sound splits into building a layered aural universe and then reconciling it in a **mix**. In both, the director rarely operates the tools but must name precisely what each moment should look and sound like — the specialist supplies alternatives, the director chooses. Restraint is the through-line: a grade or an EQ move overused reads as amateurism, so finishing is the discipline of taste applied under a magnifying glass.

## Color correction vs. color grading

The terms are confused but distinct:

**Color correction** — a technical pass most films undergo before release, with three jobs:
1. **Fix** obvious brightness/color faults — off color temperatures, inexact exposures.
2. **Match** brightness, contrast, and color (tint, saturation) shot-to-shot within a scene and scene-to-scene across the film.
3. **Legalize** — conform the technical specs to the distribution platform (broadcast, streaming, or theatrical projection).

**Color grading** — using color tools to create a deliberate **look**. Once left to editor and DP, it is now central enough that many directors plan it in preproduction with the cinematographer. It ranges from subtle mood/era tweaks to radical expressionist transformation: Jeunet's warm, lush, hyper-real *Amélie* / *Micmacs*; Granik and McDonough's two quiet looks in *Leave No Trace* — rich, vivid forest greens against muted, desaturated city, as if life had faded.

**The three-way color corrector** controls **color** (hue + saturation) and **luminance** (brightness) across three tonal ranges — **blacks, midrange, whites**. Most NLEs bundle a capable toolset (Premiere's **Lumetri Color**, Avid's **three-way corrector**); these are professional-grade, not accessories. But grading is easy to overuse — skin turns greenish or pasty, shadows go blue, highlights clip to white — so experiment on footage that does not matter. The specialist of restraint who gives a film its consistent polish is the **colorist**, generally working on a dedicated platform such as **DaVinci Resolve**, more powerful than bundled tools.

## Grading with LUTs and Log

**Log** recording uses a flat gamma profile to capture the sensor's maximum color and luminance response at reasonable file sizes. The footage looks dull and gray but holds more information — greater latitude and grading flexibility.

A **LUT** (Look Up Table) is a bundle of image settings that remap luminance, color, and gamma to produce a specific look — a **color preset**. Two lineages:

- **Custom LUTs** — built from the ground up in preproduction by director, DP, and colorist grading test footage, saved, loaded into the on-set preview monitor, and applied to the sequence in post.
- **Standard LUTs** — bundled with NLEs, some emulating film stocks (Fuji Eterna 250, Kodak 2395), others specialty looks (monochrome, golden glow, silvery blue, tobacco sepia); also purchasable or free online.

A LUT is thus **both a production tool** (making washed-out Log monitorable on set) **and a post shortcut** (dropped onto a clip, scene, or track to get close before per-scene refinement). *If Beale Street Could Talk* had Laxton and colorist Bickel engineer a LUT from a 1970s Fuji stock drawn from period Harlem photographs — a grade that then rippled backward into art direction and costume decisions.

## Finalizing the sound design

During the rough cut you edit only the tracks needed for dramatic decisions (dialogue, occasional scratch music). After picture lock, editor and sound designer build the multi-track **sound design** one track at a time — the aural universe of **dialogue, sound effects, music, ambient (atmospheres),** and sometimes **voice-over**. Elements are assembled, synced, grouped (typically 6–16 tracks for simple films), EQed, and **mixed to a master** — stereo at simplest, 5.1 surround for cinema. Short films may need nothing beyond the NLE; complex work transfers tracks into a **DAW** (Pro Tools, Nuendo) — a technical prelude, not a creative step, so the director stays focused on the narrative and emotional experience the sound must deliver.

### Voice / speech

| Type | Definition |
|---|---|
| **Sync dialogue** | Recorded in sync with picture, on location, during production; prevalent in narrative |
| **Off-screen dialogue** | In the scene's time/place but speaker unseen (Norman's cries in *Psycho*); recorded wild or in studio |
| **Voice-over (VO)** | Studio-recorded with actor/director interaction; either from outside the scene's time/place (the dead narrator of *Sunset Boulevard*) or interior monologue (Leonard's fractured thoughts in *Memento*) |
| **ADR / post-sync** | **Automatic Dialogue Replacement** ("looping") — studio re-recording lip-synced to replace substandard field audio. Laborious, hated by actors, and — done without the facilities, expertise, or time — deadening next to live location sound. Avoid where possible. |

### Sound effects (SFX)

**Spot effects** sync to something on-screen (door, coin, punch); **off-screen effects** are non-sync, from beyond the frame (doorbell, plane, distant dog). Three sources:

- **Wild location SFX** — clean close recordings the recordist grabs on set for important sounds, logged as **wild sound** and synced in post.
- **SFX libraries** — online, fee or free (sound-ideas, asoundeffect, freesound, soundsnap). Never assume a sound works until proved against picture; hunt early, since libraries skew old and can carry ambient hiss, and the nitty-gritty (footsteps, door slams) is hardest to get right.
- **Foley** — named for Jack Foley (1940s), performed live to picture in a studio floored with varied surfaces (concrete, wood, carpet, gravel). Foley artists improvise: baking powder in a bag for snow footsteps, a punched cabbage for a blow to the head. For low budgets only two things matter — the effect sounds authentic and syncs.

### Ambient sound and walla

**Ambient sound** (atmospheres) defines a location's aural environment. You may keep the natural background or, better, select and layer specific ambiences to establish a different place or inject mood — the same motel window scored with birdsong, surf, playground, or highway drone each reframes the lovers' conversation without a note of score; a layer of cicadas can read as a character's rising anxiety. **Walla** (rhubarb) is the unintelligible chatter of a crowd (a diner, a theatre house) — a gift to low budgets, implying an off-screen crowd that was never there, found in libraries or recorded wild.

## The sound spotting session

Before the sound editor gathers resources, director and editor hold a roundup on the film's broader sound identity and how each sequence fits. **Sound spotting** determines:

- Where SFX are needed and their *specific* nature — "dog barking" is not enough (yappy Yorkie? German shepherd growl? lazy hound?).
- Where ambient layering is needed and of what character (wind through trees vs. birdcall).
- Where transitions benefit from ambience, SFX, or music **sound bridges**.
- Where dialogue needs special EQ or, worst case, ADR.

Every SFX placement is logged by timecode on an **SFX spotting sheet** (the counterpart of the music cue sheet). Dialogue problems get a strategy first, because reconstruction is expensive, specialized, and time-consuming, and no worthwhile film survives it done poorly.

## Dialogue tracks and their inconsistencies

Varying location acoustics, mics, and working distances wreck voice consistency and signal-to-noise ratio; assembled raw, they make every cut artificial and pull the viewer out of the story. Seamless continuity comes from level and EQ work at the mix — possible only if tracks are laid intelligently for it:

- **Splitting dialogue tracks** — group by mic position: all close-shot sound on one track, medium-shot on another, so a single EQ and level setup covers a track across the whole scene. Six setups/six mic positions may mean six tracks, further split per character where each voice needs its own treatment.
- **Inconsistent backgrounds** — strip removable extraneous noise (creaks, wind-rumble, mic handling) that does not overlap dialogue; poach impaired words from another take; fill gaps with the one minute of **room tone** recorded on location; augment quieter backgrounds to match noisier angles. Because the ear registers a hard cut more than a gradual change, ambience shifts are made through **sound dissolves**, not cuts.

## Preparing for and directing the mix

You are ready to mix when you have: finalized content (picture lock + completed multi-track design); fitted music; split dialogue tracks (grouped by EQ need, per mic position and possibly per speaker); filled-in backgrounds; recorded/laid narration; and recorded/laid SFX and atmospheres. The **mix** brings all tracks into acceptable compatibility — voice levels and perspectives varying with camera distance, all elements balanced — an evolving interplay of psychoacoustics and aural verisimilitude judged only by ear. It determines:

| Mix control | What it does |
|---|---|
| **Relative levels** | Balance dialogue against ambience and music across a scene |
| **Equalization (EQ)** | Filter/profile tracks for match or intelligibility (roll off low rumble, keep voice frequencies) |
| **Quality consistency** | Match EQ, level, and ambience across two angles on one speaker |
| **Perspective** | Use EQ and level to mimic spatial distance and dimensionality |
| **Level changes** | Fade-up/down, sound dissolves, adjustments for new elements |
| **Sound processing** | Delay, reverb, echo, and effect EQ (telephone timbre, voice behind a door) |
| **Dynamic range** | Compression squeezes cinema range for domestic TV; a limiter caps peaks under a ceiling |
| **Multichannel** | Route elements to channels for stereo/5.1 spread |
| **Noise reduction** | Dolby and similar suppress hiss under quiet passages |

**Directing the mix:** you need not know how an effect is achieved, only what each sequence should sound like and what you dislike or prefer; the mix engineer offers alternatives and you choose. **Approve section by section, then listen to the whole film start to finish without stopping** — the uninterrupted pass reliably exposes an anomaly or two.

## Titles and credits

The final **title** is often chosen late and in agony — it must be short, distinctive, and epitomize the film's allure, since a festival listing may give it no other chance to catch an eye. NLEs generate most titles; go to After Effects only for custom fonts, spacing, or resolution beyond the basics.

- **Style** — conservative; overambitious front titles promise more than the film delivers. Prioritize legibility; place against the background composition; model on comparable films.
- **Credits** — brisk; the same name should not recur across key roles. Skip fancy logos and grandiose company names — let the film, not its packaging, talk.
- **Obligations** — honor contractual credit terms for union talent (size, wording) and any funder or institutional wording to the letter; favors were granted for acknowledgment, so leave no one out.
- **Spelling** — check names scrupulously; a misspelling reads as indifference to the people who gave you everything.

## Studio application

- **Two post-finishing roles land here, both designed and unbuilt.** The **ReRecordingMixer** owns the final mix over speech stems and score; the **Colorist** owns the grade over still and video output. In the studio these sit above the only built renderers: [`speech.py`](../../../sequitur/speech.py) (dialogue / VO / the ADR analogue — a re-render of a speech stem when the first take fails), [`image.py`](../../../sequitur/image.py) (the still / grade analogue), and [`studio.py`](../../../sequitur/studio.py) (video output). The sound-layer design is in [storyline 0009](../../../context/storyline/0009-the-sound-layer.md); the voice layer in [0011](../../../context/storyline/0011-the-voice-layer.md).
- **Correction vs. grading maps onto validate vs. judgment.** Color *correction* (fix + match + legalize) is a deterministic pass, kin to the validation in [`edit.py`](../../../sequitur/edit.py); color *grading* (the LOOK) is an aesthetic reconciliation the Colorist owns, scored via [`crew/judgment.py`](../../../sequitur/crew/judgment.py). A **LUT is a reusable look-preset** — a Production-level style config the [`image.py`](../../../sequitur/image.py) renderer honors, analogous to the shot-design keyframes planned in [Ch. 23, *Planning the Visual Design*](ch23-planning-the-visual-design.md); the exposure/Log lineage traces back to [Grammar of the Shot Ch. 04, *Lighting*](../../grammar%20of%20the%20shot/reference/ch04-lighting.md).
- **Sound design is a multi-track aural universe the studio has only begun.** Only [`speech.py`](../../../sequitur/speech.py) (dialogue/VO) is built; **SFX, ambient, walla, and Foley are unbuilt renderer seams**, and music is the strudel seam from [Ch. 35](ch35-working-with-music.md). Split dialogue tracks, the spotting sheet, room-tone fills, and sound dissolves are timeline track-management the ReRecordingMixer performs over the Sequence in [`edit.py`](../../../sequitur/edit.py), executed by [`cutter.py`](../../../sequitur/cutter.py) under [`crew/editorial.py`](../../../sequitur/crew/editorial.py).
- **Direct craft overlap — flag it:** the mix and processing content here re-covers [Rose Ch. 17, *The Mix*](../../producing%20great%20sound%20for%20film%20and%20video/reference/ch17-the-mix.md) and [Ch. 16, *Processing*](../../producing%20great%20sound%20for%20film%20and%20video/reference/ch16-processing.md); the SFX/Foley material overlaps [Rose Ch. 15, *Sound Effects*](../../producing%20great%20sound%20for%20film%20and%20video/reference/ch15-sound-effects.md); the dialogue-inconsistency and ADR triage overlaps [Rose Ch. 18, *Help — It Doesn't Sound Right*](../../producing%20great%20sound%20for%20film%20and%20video/reference/ch18-help-it-doesnt-sound-right.md). Sound bridges tie to [Grammar of the Edit Ch. 06, *Transitions*](../../grammar%20of%20the%20edit/reference/ch06-transitions-and-edit-categories.md).
- **Authority through-line:** the Director ([`crew/director.py`](../../../sequitur/crew/director.py), on [`crew/engine.py`](../../../sequitur/crew/engine.py) via [`crew/role.py`](../../../sequitur/crew/role.py)) is the agent reconciler holding the *don't over-grade / don't over-EQ* restraint; the **Producer (the human)** signs off the final mix, the grade, and the contractual/spelling credit gates before the film ships to [Ch. 37](ch37-getting-it-out-there.md).

*Finishing is taste under a microscope — the director names the feeling, the specialist finds the setting, and the whole is judged only on an uninterrupted pass.*
