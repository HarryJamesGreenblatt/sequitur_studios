# Chapter 6 — Screenplay Ground Rules

> Abridged from Michael Rabiger & Mick Hurbis-Cherrier, *Directing: Film Techniques and Aesthetics* (6th ed.), Ch. 6.
> **Scope:** What a screenplay *is* — the shareable skeleton of a film — its developmental stages, and its standardized formatting. This is the raw input the director interprets into images and sound; it grounds the *form* the story arrives in before any shot is composed.

## Core idea

A screenplay is only the **bones** of a film: its basic content (characters, locations, actions, dialogue, general dramatic shape) rendered in a standard, shareable form — much of which will change downstream. It is **not** a finished artwork and never should be treated as one; by nature it is malleable and revisable, and it keeps evolving in response to personnel, resources, locations, and new perspectives right up to (and through) the first day of shooting. The director's job is to read, test, and analyze this paper manuscript, then construct a coherent fictional universe from it. To do that, a director must know screenplay **form, stages, and language** cold.

## The writer writes; the director directs

Whoever holds the pen, it is folly to "direct the film on the page." A film reaches full expression only through a collaborative team, so the script must **leave room** for the director, actors, cinematographer, production designer, and editor to do their jobs — the final form is not set in stone. This holds doubly for the **writer/director**: over-committing to shortsighted directorial choices baked into the script months earlier blinds you to better opportunities that emerge in production. The discipline is to **switch hats** — wear the writer's hat when writing, the director's hat when directing — so you approach your own script with the same critical, analytical, interpretive rigor you would bring to a stranger's.

## Screenplay stages

Scripts almost always arrive already revised, and rewriting continues throughout the process. In student groups, rewriting is often skipped to spare the writer's feelings — a mistake. In the professional world a writer relinquishes control on delivery so the director and producer can alter the material as needed; among unpaid equals this demands more diplomacy.

| Stage | What it is |
|---|---|
| **Step outline** (aka **beat sheet**) | Brief sketch of the major dramatic beats in **third-person, present-tense** prose. One–two sentences per significant narrative moment: **who** is in the scene and **what happens**. Traces the essential plot line and the moves of major characters; spare language, important dialogue summarized. A screenplay-**analysis** tool used even *after* the full script exists. |
| **Treatment** | Present-tense prose version of the plot, more detailed than a step outline — commonly one paragraph per major dramatic unit. Outlines characters and interactions; traces conflicts, actions, resolution; sketches subtext, mood, and tone. Dialogue summarized (a key line may appear verbatim). Usually a **writer's tool**, especially for **spec scripts**, and often the first contracted submission when commissioned. Suggest changes here — a treatment is far easier to revise than a finished script because structural and character issues are more apparent. |
| **First draft** | First version in standard screenplay format with fully realized scenes and dialogue. A smart writer shows it to few people. |
| **Author's draft** | The reworked draft — after feedback, research, and rewrites — that the writer sends to producers/directors. Writers often believe *this* is final; it rarely is. |
| **Final draft** | The last draft *before* preproduction breakdown, incorporating producer and director input. |
| **Shooting script** | The visualized final draft taken into production — now with **scene numbers and camera angles** added. Shared with cast and crew; further cuts, tweaks, and alterations are common and are frequently made by the director **without** the writer. |

> A **spec (speculative) script** is a non-commissioned, unsolicited screenplay written to attract a sale or option.

## Standard screenplay formatting

The screenplay is a **dramatic manuscript** *and* a **technical document**. Standardized format lets it be broken down for scheduling and lets everyone quickly find what they need. The rules are simple, essential, and shared — **do not invent your own**. (Software: Final Draft, paid; Celtx, free; plus word-processor templates. But formatting is more than margins — consult a formatting reference.)

**Baseline conventions**

- **Tense:** third person, **present tense** — the film as it presents itself to an audience, moment by moment, scene by scene.
- **Typeface:** 12-point **Courier** — the industry standard because it makes **one page ≈ one minute** of screen time.
- **Numbering:** page numbers in the upper-right corner.
- A **scene** is an event or exchange with **unity of time and place**; a new location *or* a shift in time (day→night, "two days later") requires a **new scene** with a new heading.

**The six manuscript elements**

| # | Element | Function |
|---|---|---|
| 1 | **Scene heading** | Capitalized: (a) INT./EXT., (b) specific location *(not a description)*, (c) time of day (usually DAY, NIGHT, DAWN, DUSK). |
| 2 | **Stage directions** (actions) | Essential actions, images, and sounds, present tense, in the order an audience perceives them. Paragraphing marks dramatic beats or shifts in visual perspective. |
| 3 | **Character cue** | The speaker's name in ALL CAPS; consistent throughout. Carries **(O.S.)** *off-screen* and **(V.O.)** *voice over* (speech from another time/place). |
| 4 | **Dialogue** | What characters say — any tense; reflects human speech and needn't obey strict grammar. |
| 5 | **Personal direction** (parenthetical) | A brief note of a small action on a line, the specific addressee (if unclear), or the manner of delivery (e.g. whispering). |
| 6 | **Scene transitions** | Used **only** when unavoidable to sense — e.g. DISSOLVE TO: (into flashback/fantasy) or MATCH CUT TO: (shared graphic element). |

**What the author's draft deliberately omits.** No scene numbers and **no camera cues** ("CLOSE UP," "PAN WITH") — those are added later, in the preproduction breakdown that produces the shooting script and shot list (Ch. 24), usually without the writer. No **emotion indications** ("wistfully," "sorrowfully") in personal directions either: how a line is spoken is discovered by actor and director in rehearsal, and a well-written line *reads* correctly without an emotional tag. Scripts that smuggle in camera and emotion cues are **hybrid deviations** written for a particular person or purpose, and such cues are normally ignored.

## Studio application

- This chapter grounds the **screenplay as the input artifact** the Director agent interprets — the thing that exists *before* any of the crew's decisions. The "scene = unity of time and place" rule maps straight onto the editorial decision model in [edit.py](../../../sequitur/edit.py) (`Clip`/`Beat`/`Scene`/`Act`/`Sequence`); the **step outline / beat sheet** is that model's `Beat`/`Scene` layer expressed in prose, and the "one page ≈ one minute" heuristic is exactly the kind of duration estimate `timeline()` needs.
- The **six manuscript elements** partition cleanly across the code seams: the **scene heading** → `Scene` metadata; **stage directions** → the `Brief.scene` text plus `hints` consumed in [role.py](../../../sequitur/crew/role.py); **character cue / dialogue** → the future Screenwriter role and the voice layer in [speech.py](../../../sequitur/speech.py). Crucially, camera cues are **excluded** from the author's draft — that omission *is* the seam where the Director and Cinematographer add `ShotSize`/`CameraAngle` downstream ([camera.py](../../../sequitur/crew/camera.py)). The **shooting script** is the artifact the crew engine ([engine.py](../../../sequitur/crew/engine.py)) is meant to produce: an author's draft *visualized* into a shot list.
- Authority tiers: the **Producer (human, HITL)** supplies/greenlights the script; the **Director (agent)** interprets it and reconciles crew contributions into a `Shot` ([director.py](../../../sequitur/crew/director.py)); the Screenwriter role that would *own* screenplay form is planned but uncoded — this chapter is the **form its output must take**. That output seeds the `Brief` → Director reconciler ([0014](../../../context/storyline/0014-the-crew-behaviour.md)).
- Cross-department through-lines: the script's scene structure is where editing begins ([Grammar of the Edit, Ch. 1](../../grammar%20of%20the%20edit/reference/ch01-the-editing-process.md)); its plot sequencing is the concern of the Taxonomy's **Pathway** layer ([Taxonomy, Ch. 6](../../the%20screenwriter%27s%20taxonomy/reference/ch06-pathway.md)).

> **Overlap flag (staging note 0015):** This chapter is screenplay **form/format**, whereas *The Screenwriter's Taxonomy* is a **classification** system — the overlap is light. The one genuine touchpoint is "scene = unity of time and place," which the Taxonomy assumes and the [edit.py](../../../sequitur/edit.py) `Scene` model encodes.

*Next: [Ch. 7 — Recognizing the Superior Screenplay](ch07-recognizing-the-superior-screenplay.md), where the director learns to judge whether a given script is worth this long marriage.*
