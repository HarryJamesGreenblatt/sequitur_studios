# Chapter 7 — Staging

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 7.
> **Scope:** how a board arranges subjects and camera in space — visual weight in the single frame, staging a scene against the "talking-heads" default, secondary action, and depth as a tonal control. This is the chapter that *decides coverage before the DP arrives*.

## Core idea

**Staging** is the arrangement of characters and objects in the scene *plus* the character and camera movement that choreographs them. It is the storyboard artist's highest-leverage skill: strong staging manufactures efficiency, covers weak dialogue, and gives dull material visual and emotional life. Everything downstream — shot size, angle, composition — is a *consequence* of where you put the subjects and where you put the camera.

Staging works at two scales that reinforce each other. In the **single frame**, proximity and framing dictate the audience's emotional read; in the **scene**, the choreography of bodies and camera across the set turns a static exchange into a sequence of revelations. Staged well, a scene needs only two or three camera positions to carry pages of dialogue, and you **cut only when a cut is necessary** — so every shot delivers *new information* instead of cutting for its own sake.

## Staging the single frame

- **Never give two objects equal importance.** Equal weight splits the viewer's interest and flattens the picture. Give one subject dominance — usually by making it **bigger / closer** — and let that hierarchy carry the emotional beat.
- **Angle + arrangement encode emotion.** To sell a character's rejection, don't reach for the face — use a **high angle** and push her away from the group. Isolation reads best as a **small figure alone in a large empty frame**.
- **Expression is whole-body, not facial.** Attitude is conveyed by staging, environment, and body language; often the strongest choice is *not to show the face at all*.

## Staging the scene

The default dialogue solution — alternating singles of each speaker — produces inert "talking heads" with no motion. Break it:

- **Vary posture and orientation.** One character sits while the other stands; one turns their back mid-line. Cheap variety, immediate richness.
- **Move bodies and camera together across the set.** Movement lets you **combine lines that would otherwise be separate shots** (efficiency) and lets a **gesture mark the beat** — the witness rising and crossing the room exactly as the interrogator names the outcome.
- **Know the subject matter; mine the location.** Research the world (a mechanic slides out from under a car, rises, reaches for tools upstage) so the set yields **foreground elements** to pass the camera and **paths** for it to travel.

## Secondary action

Give a character a task that either **supports** the story point or **ironically contrasts** it — the contrast is the payload.

- Two fast-food workers debating weight loss *while serving greasy fries* — the setting mocks the goal, and the kitchen (register → fryer → grill) unlocks a tracking camera the park bench never would.
- Politicians revealing insider info *over a golf game* — and the *way* they play (one crowding the other's backswing) does the characterization.

Secondary action exists to generate motion and therefore **unique camera set-ups**. Keep it proportionate to the scene; don't stage business for its own sake.

## Depth as a tonal control

Rule of thumb: **deep space for drama, flat space for comedy.**

| Register | Space | Composition | Palette | Camera distance |
|---|---|---|---|---|
| Drama / tension / action | **Deep** | Diagonals; avoid symmetry and straight lines | Darker, limited | Close — being far back makes us watch *uninvolved*, killing the tone |
| Comedy | **Flat** | Movement parallel to or straight at the lens (one-panel-strip / stage-comic space) | Bright | Far back can even make extreme action read as *funny* |

Flat staging on a dramatic scene actively undercuts the feeling you're working to build. Blend the right **depth** with **camera and character movement that tracks the emotional beat**, and the staging becomes both exciting and economical.

## Studio application

- **Staging is the PLAN-phase source of truth for coverage.** A board *decides* where subjects stand and where the camera sits — i.e. it fixes the **inputs** that the shoot later expresses as `ShotSize`, `CameraAngle`, and `Composition` in [camera.py](../../../sequitur/crew/camera.py). A storyboard panel is a *pre-rendered [Shot](../../../sequitur/shot.py)*; staging is what the panel resolves before any DP heuristic runs.
- **"Never two objects of equal importance" is a `Composition` constraint.** The visual-weight rule is exactly the dominance decision `Composition` encodes; it enters generation through `build_image_prompt` in [prompt.py](../../../sequitur/prompt.py) and is realized as a reference keyframe by [image.py](../../../sequitur/image.py). It cross-links *Grammar of the Shot* [ch02-shot-composition](../../grammar%20of%20the%20shot/reference/ch02-shot-composition.md).
- **Secondary action + choreography = `CameraMovement` and shot efficiency.** Moving bodies and camera together is what lets one clip carry multiple beats — the "cut only when necessary" economy. This is the [grip.py](../../../sequitur/crew/grip.py) `CameraMovement` axis and *Grammar of the Shot* [ch06-dynamic-shots](../../grammar%20of%20the%20shot/reference/ch06-dynamic-shots.md); it is also why a single `Shot.single_scene` can span a beat instead of forcing a cut. The 180°/coverage grammar this chapter *assumes* lives in [ch05-shooting-for-editing](../../grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md).
- **Depth-as-tone is a genre/tone knob, not a per-shot whim.** Deep-for-drama / flat-for-comedy keys staging to supergenre and Voice — see the Screenwriter's Taxonomy [ch02-movie-types-and-supergenres](../../the%20screenwriter%27s%20taxonomy/reference/ch02-movie-types-and-supergenres.md) — so a future Storyboard Artist (or the [Director](../../../sequitur/crew/director.py) reconciler) should read tone and bias depth, palette, and camera distance accordingly. It sits alongside the preproduction visual-design work in Directing [ch23-planning-the-visual-design](../../directing/reference/ch23-planning-the-visual-design.md).
