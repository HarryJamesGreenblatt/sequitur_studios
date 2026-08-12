# Chapter 10 — Advanced Storyboard Techniques

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 10.
> **Scope:** higher-order craft — efficient staging, complex/handoff camera moves, transitions, cutting styles, dialogue and screen-direction play, action scenes, and the animatic tricks (swoosh lines, hook-ups, layered parallax) that make a *static* board encode **motion and time**.

## Core idea

Once a sequence works, advanced technique amplifies it — turning a flat, boring scene into a thrilling visual experience. The through-line is **efficiency**: fewer cuts, staging that combines multiple story points into a single moving shot, and camera moves that reveal new information rather than sit still. Every technique here fights the medium's central limitation for a storyboard artist — a board is a *still* image, yet it must convey movement, camera travel, elapsed time, and the flow from one shot to the next. The answers are all conventions for smuggling motion into a frozen frame (arrows, swoosh lines, multi-panel moves, layered parallax) and for carrying the eye across cuts (hook-ups, transitions, matched direction).

## Creating efficiency

Use **fewer cuts**. Plan staging so several story points land in one set-up, and keep characters moving in their world for visual appeal. A **tracking shot** across three characters, for instance, is boarded by separating the move into beats — one panel per camera position — so the animatic reads the continuous travel.

## Complex camera moves

**Start on one subject, end on another.** Move the camera through the scene to reveal information — begin wide, end on a close-up; chase depth and dynamic space. A **handoff shot** tracks with one subject, then passes the focal point to a *second* subject who crosses in front of camera — a built-in visual transition or a mood-setting opening. In opening shots, **camera speed and height** set mood: *show, don't tell* with the camera, which also cuts unnecessary dialogue. A boarded complex move is a run of panels (start subject → travel beats → end subject).

## Transitions

Transitions carry action smoothly and uniquely from one scene to the next — the "bread and butter" of the story artist.

| Type | How it works |
|------|-------------|
| **Visual** | Camera leads the eye across (pan from one conversation to a window revealing another); or **match cut** on a similar shape (setting sun cross-dissolving into a grandfather clock). Handoff/complex moves also serve. |
| **Story point** | Cut to similar subject matter — usually the thing named in the last line ("the upcoming battle" → cut to the battle). Sets an expectation and pays it off. |
| **Audio** | Carry music/song across the cut (same song on two radios; a character's song becomes the next scene's score). Boards can only *note* these as written suggestions. |
| **Effects** | Fades, wipes, dissolves, montage morphs where objects transform into the next scene's objects. An exaggerated visual transition. |

## Cutting styles & creative dialogue

- **Vary the cutting** (long shots vs quick cuts) to match content. Cut **on action** with solid **hook-ups**: continue one action into the next shot, and **lead the eye** — if a character exits left-to-right, cut to an object also travelling left-to-right.
- **Dialogue:** stage blocks of talk in **longer shots** with interesting staging and **secondary action** ("business" — a vet moving from paperwork to animals to washing hands as he speaks) to generate movement, fewer cuts, and character beats. Better still, use **less** dialogue and tell it visually. Make every word count: **set up** a line in one scene and **pay it off** later.

## Creative screen direction

The 180° rule is usually held rigidly, but breaking it *on purpose* is a tool. **Flopping** screen direction / crossing the line jars the audience and creates unease — done from cut to cut, or via a clean exit then a clean entry on the opposite side. An **orbit** around a character as they reveal key information re-establishes direction *and* emphasises the beat by landing them on the other side of the screen. In heavy action, arbitrary direction can deliberately disorient. The rule: a flop must be a *conscious* choice, never read as an accidental mistake.

## Awesome action scenes

Action is pointless without emotional weight — assume the beats are already worked out, then make it **cinematic** (dull staging ruins a good fight). Build **anticipation**: faster cuts, camera moving closer with each cut, rising danger. Maximise depth by driving objects **toward and away** from camera; tilt and lower the camera; keep the action **travelling** through the set with the camera tracking it — the camera *follows* the action, never leads it. Shot variety and strong compositions matter *more* here, not less.

- **Combat poses:** *guard* (power centering) → *anticipation* (powering up, power in the shoulders) → *set-up* (glancing blows) → *the strike* (impact/unload). Choreography should reflect each character's real skill set (a Navy SEAL ≠ a ninja) — research authentic styles.
- **Fight rhythms:** vary the beats — `strike, strike, strike, block` / `block, block, strike` / `block, block, strike, strike` / `strike, block, block, strike`.
- **Staging arc:** establishing down- or up-shot → cut closer between fighters to build anticipation → medium (usually up-shots) on the first exchange to show skill → lead-in close on an anticipation pose → OTS of striker over the parrying/evading fighter → close-ups on impacts, wides on acrobatics → wide down-shot to sell environmental danger (a ledge).

## Animatic techniques

Because most boards now feed an **animatic** (a cut, timed reel), some tricks look silly in a lone still but transform the cut sequence:

- **Swoosh / action lines.** Comic motion lines seem ridiculous frozen, but cut together they massively improve how action flows. Always add them even when they feel unnecessary.
- **Hook-ups.** Board so an action continues visibly from one panel into the next; good hook-ups are what make the animatic flow.
- **Illusion of parallax.** Split the composition onto **foreground / middle-ground / background** layers that move at different speeds during a pan or track — closer elements shift *more* than distant ones. A camera move may need **5–10 panels** to sell it; a **zoom** is successive scale-ups of the image. Build it like a 2D animation layout: one large background, a **camera guide** (constant aspect ratio, changing size) laid over it, character/foreground layers added, then each camera position cut out as a separate frame — composited in After Effects or overlapped by the artist by hand.

## Studio application

- **This chapter is exactly the problem `build_prompt` solves that `build_image_prompt` skips.** A still board must encode *motion and time*; in [`../../../sequitur/prompt.py`](../../../sequitur/prompt.py) the video builder (`moving=True`) layers on the `movement`, `speed`, `audio`, and `single_scene` faces of the [`../../../sequitur/shot.py`](../../../sequitur/shot.py) that the still builder (`moving=False`) drops. **Arrows and swoosh lines are the board analogue of those video-only motion faces** — the manual convention a static panel uses to say what `Shot.movement`/`Shot.speed` say to the video renderer ([`../../../sequitur/studio.py`](../../../sequitur/studio.py)).
- **A handoff / complex move that starts on one subject and ends on another is a `single_scene` continuous shot.** It maps onto the `single_scene` face ("a single continuous shot, no scene cuts") that `build_prompt` emits — one `Shot`, camera travelling, rather than a cut. The camera vocabulary itself (tracking, speed, height for mood) is the `CameraMovement`/`MotionSpeed` grammar of Grammar of the Shot [`../../grammar%20of%20the%20shot/reference/ch06-dynamic-shots.md`](../../grammar%20of%20the%20shot/reference/ch06-dynamic-shots.md), decided by the camera role in [`../../../sequitur/crew/camera.py`](../../../sequitur/crew/camera.py).
- **Multi-panel-for-a-move (5–10 panels + layered parallax) is the shot-to-sequence seam.** When one camera move needs a run of boards, that's a sequence of [`../../../sequitur/image.py`](../../../sequitur/image.py) keyframes conditioning successive beats of a single rendered shot — the previz bridge from plan-phase decisions to a per-shot visual spec, and the point where a Storyboard Artist role's `Contribution` would emit a *panel series*, not one still.
- **Transitions, cutting styles, and hook-ups belong to the edit layer, not the shot.** Match cuts, cut-on-action, story-point cuts, and eye-leading are decisions about *joining* shots — grounded in Grammar of the Edit [`../../grammar%20of%20the%20edit/reference/ch05-when-to-cut.md`](../../grammar%20of%20the%20edit/reference/ch05-when-to-cut.md) — while deliberate screen-direction flops are the 180°-continuity concern of [`../../grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md`](../../grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md). The `Director` reconciling shot order ([`../../../sequitur/crew/director.py`](../../../sequitur/crew/director.py)) owns these seams; the per-`Shot` spec owns only what happens *inside* the frame.
