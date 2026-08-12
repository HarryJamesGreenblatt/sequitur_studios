# Chapter 2 — Visual Literacy

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 2.
> **Scope:** the artist's grammar for reading and composing a single frame — story point, appeal, line/shape/contrast, focal point, and the toolkit for creating depth on a flat surface.

## Core idea

Visual storytelling juxtaposes flat images inside a **frame** and plays them over **time** to move an audience emotionally. Every panel therefore has two obligations. First, it must serve a **story point** — the reason the shot exists, the answer to "why?" (why did the character enter, why is she afraid, why did the bank explode). A panel with no story point should not be drawn. Second, it must have **appeal** — that read-at-a-glance clarity, pleasing design, and simplicity that lets the eye grasp it instantly; a drawing that is cluttered, over-worked, or hard to read has none, no matter how skilled. When a panel "feels off," it is usually a failure of one of these two, not of rendering.

The craft, then, is arranging elements inside the frame so the audience's eye is steered to a single intended **focal point** that delivers that story beat — one beat, one focus, per panel. The frame is a flat two-dimensional surface, so a second discipline runs underneath everything: manufacturing (or deliberately withholding) the **illusion of depth**. The artist reads the real world's depth cues and then *emphasises or suppresses* them at will to control what the eye feels.

## The grammar of the frame

**Line** — direction carries emotion:

| Line | Feeling |
| --- | --- |
| Horizontal | calm, static, at rest |
| Vertical | calm but more active than horizontal |
| Diagonal | dynamic, energetic, unstable |
| Parallel / symmetric | order, stateliness, formality |
| Asymmetric | chaos, unease, disorder |

- **Divide unevenly.** Splitting the frame into equal spaces is boring; unequal divisions create interest.
- **Rule of thirds.** Divide the frame in thirds each way; place key elements on the lines or their intersections. Symmetry (elements on the halfway line) reads stiff and formal — use it only when *that* is the intent. Beginners default to static symmetry; force an asymmetrical composition first, then pull it back toward order only if the story asks.

**Shape** — silhouettes carry conditioned emotional associations:

| Shape | Evokes |
| --- | --- |
| Circles / ovals / curves | friendliness, fun, happiness |
| Squares / rectangles / right angles | formality, order, stability |
| Triangles | aggression, dynamism, tension |

**Focal point** — steering the eye:

- Choose *where* the focus sits **before** drawing; angle every supporting element (branches, tables, chairs) to point at it.
- **One primary focus per panel**, matching the one story beat. You may add a **secondary** and **tertiary** focus, but they exist only in a strict order of importance that *supports* the primary — never competes.
- **Declutter to clarify.** If a beat reads as confusing, the focal point is probably unclear or contested; remove elements until one clean focus emerges.

## The depth toolkit

The default beginner tendency is flat space; depth is a set of deliberate tricks. "Deep space" (expansive, room for the eye to travel) vs. "flat space" (subject against a wall/backdrop) is itself a dramatic choice, not a limitation of skill.

- **Perspective grid — draw one in every frame.** Parallel lines converge to a **vanishing point** on the **horizon line**, and the horizon line *is the camera's eye-level / height* — nothing about it should be arbitrary. One-, two-, and three-point perspective (add points for more sides / more distortion) plant figures at consistent size and depth.
- **Cheating perspective.** Grids need not be ruled; vanishing points can sit off-canvas. A roughly-sketched convergence is enough — with practice the grid is drawn freehand by *knowing* where the horizon should be.
- **The grid trick.** Changing *only* the grid direction under an unchanged subject converts a down-shot into an up-shot — the grid alone can restate the camera angle.
- **Hanging perspective.** Figures/objects of the same height are cut by the horizon line at the same proportional place regardless of distance, so they "hang" from it. This plants a whole crowd in correct perspective freehand, using head-height proportions to the horizon as the measure.
- **Contrast.** The eye goes to what is *different* — big vs. small, dark vs. light, sharp vs. soft, moving vs. still, one curve in a field of angles. Contrast both *creates a focal point* and *reads as depth*: light/warm advances, dark/cool recedes; near objects hold a wider light-to-dark range than far ones (atmospheric perspective).
- **Foreground / middle ground / background.** Stage all three whenever possible — even a close-up can carry a foreground or background element — to break the flattening instinct.
- **Overlap.** One form occluding another reads unambiguously as "in front," manufacturing depth cheaply.
- **Change in size.** An object growing across frames advances toward us, shrinking recedes — so **stage for size change, avoid flat profile shots**, letting subjects grow/shrink within the frame for depth and interest.

## Studio application

- **This is the compositional vocabulary the Cinematographer already owns in code.** The chapter's frame grammar overlaps directly with the enums in [`crew/camera.py`](../../../sequitur/crew/camera.py): the rule-of-thirds-vs-centered distinction *is* [`Composition`](../../../sequitur/crew/camera.py), the horizon-as-camera-height insight *is* [`CameraAngle`](../../../sequitur/crew/camera.py) (eye-level / high / low / Dutch), and the depth toolkit (perspective, contrast, overlap, atmospheric recession) *is* [`FocalLength`](../../../sequitur/crew/camera.py) + [`DepthOfField`](../../../sequitur/crew/camera.py). A storyboard panel and a rendered shot are composed with the same controls — cross-read with [Grammar of the Shot Ch. 2 — Shot Composition](../../grammar%20of%20the%20shot/reference/ch02-shot-composition.md) and [Ch. 3 — Depth, Perspective, Focus](../../grammar%20of%20the%20shot/reference/ch03-depth-perspective-focus.md).
- **"Story point + one focal point" is the spec a prompt must encode.** Because every panel serves exactly one beat with one intended focus, the [`Shot`](../../../sequitur/shot.py) → [prompt](../../../sequitur/prompt.py) pipeline should compose toward a single clear subject and focus, not a cluttered frame — declutter the prompt the way the artist strips elements to recover focus. The "why?" of the story point is the through-line the [`Director`](../../../sequitur/crew/director.py) reconciles across the [`Brief`](../../../sequitur/crew/role.py).
- **Emotion-through-composition is renderer-agnostic.** Line direction, shape language, and contrast produce feeling independent of medium, so the same compositional intent drives both an [`ImageStudio`](../../../sequitur/image.py) reference keyframe and the video render conditioned on it. Emotional beats also connect to performance — see [Directing Ch. 19 — Acting Fundamentals](../../directing/reference/ch19-acting-fundamentals.md).
