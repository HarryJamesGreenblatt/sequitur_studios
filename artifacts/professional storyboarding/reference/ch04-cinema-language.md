# Chapter 4 — Cinema Language

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 4.
> **Scope:** the storyboard artist's compressed film grammar — aspect ratio, shot size, camera height/angle, eye line, camera movement, lens/perspective, screen direction and the 180° rule. The same vocabulary the cinematographer owns, but committed *before the shot exists*.

## Core idea

Every board is drawn *through a camera* — an imagined lens standing in for the audience's eye. The board artist looks through that lens in their mind and captures what it sees, which means they make the same framing, angle, lens and movement choices a DP makes on set, only earlier. This chapter is the artist's working subset of film grammar: enough camera vocabulary to draw a shot that a cinematographer can later realise, no more. The governing maxim — **you place the camera where you place your audience** — turns every technical choice into an emotional one, because proximity, height, and eye line decide how involved the viewer feels.

Two disciplines run underneath all of it. **Clarity**: however many grammar "layers" you stack (a wide lens *plus* a crane *plus* a Dutch tilt), the story point must read instantly. **Motivation**: deliberate camera acts — pans, tilts, reveals — should be prompted by something in the scene, or the viewpoint feels like it is drifting aimlessly.

## Aspect ratio — the frame contract

Decide first, then never change it: the ratio fixes the composition box for the whole project. Width is stated relative to a height of 1.

| Ratio | Also known as | Typical use |
|-------|---------------|-------------|
| 1.33:1 | 4:3, Academy | Legacy TV; classic-era film |
| 1.66:1 | European widescreen, Super 16 | Older Disney features |
| 1.78:1 | 16:9 | Video games, commercials, modern default |
| 1.85:1 | US/UK theatrical | Standard theatrical widescreen |
| 2.35:1 | Anamorphic, Panavision, Cinemascope | Epic scope (modern anamorphic is really 2.39) |

## Shot size (shot choice)

Three base families — **wide / medium / close** — subdivide into gradations named by where the frame cuts the figure. This is the same ladder the studio's `ShotSize` enum encodes.

| Shot | Cut / content | Reads as |
|------|---------------|----------|
| Extreme wide (EWS) | Subject tiny, part of the scenery | Establishing; environment over character |
| Wide / long (WS/LS) | Full figure, environment still prominent | Character *in* their world; action legible |
| Full shot (FS) | Head-to-feet, tight as possible on the figure | Broad body language and action |
| Cowboy | Head to mid-thigh | Gesture through arms/upper body (Western idiom) |
| Medium (MS) | Head to hips | Face expression *plus* gesture; intimate |
| Close-up (CU) | Head to base of neck | Important personal information; emotion |
| Choker | Above forehead to chin | Objectifies; surface of the face (noir) |
| Extreme close-up (ECU) | Lips to eyebrows or tighter | Pure attitude / surface detail |

Relational shots layered on top of size:
- **OTS** — a foreground head/shoulder anchors two people in one frame; keeps the listener present.
- **POV** — the camera *is* a character's eyes; usually cut in after a CU of that character.
- **Reverse** — the opposite viewpoint of the prior shot (mind screen direction).
- **Reaction** — cut to a character's response to new information.
- **Insert** — reveal a detail within the scene (keys, a note); usually CU.

## Camera height and angle

The drawn horizon line *is* the camera height, and small shifts change perceived importance.
- **High angle** (camera above eye level) — favours environment/situation over the character; the subject looks less in control. Extremes: **overhead** (straight down, no horizon) diminishes the subject; **bird's-eye** maps the geography from far above.
- **Low angle** (camera below eye level) — the subject reads powerful, in control; also speeds action because perspective scaling is exaggerated. Extreme: **worm's-eye** from ground level, maximally distorted.
- **Eye level** — neutral, equal footing.

These map directly onto `CameraAngle` in [camera.py](../../../sequitur/crew/camera.py).

## Eye line — engagement

The camera is the audience's viewpoint, so how directly a subject faces the lens sets how *involved* the viewer feels.
- **Frontal / into the lens** → maximum connection (used deliberately, e.g. *Silence of the Lambs*).
- **3/4 frontal, eyeline just off the lens** → the sweet spot: dimensional and engaging.
- **Near-profile** → the novice default; disengaged. Avoid unless intended.

This is the artist's version of the studio's split between `SubjectView` (horizontal angle on the face) and `ShootingStyle` (whether the subject acknowledges the lens).

## Camera movement

**Pivots** (camera turns in place): **pan** (horizontal), **tilt** (vertical). Little parallax — the whole image slides against the frame. Should be *motivated* (a bird, a walk) and bracketed by static start/end holds; don't cut into or out of the middle of one. Exception: a POV pan is "under the character's control".

**Travelling moves** (camera changes position; objects shift against each other — *parallax*):
- **Dolly / tracking** — horizontal travel on rails.
- **Push in / pull out** (truck in/out) — toward or away from the subject.
- **Boom** — camera on a pivoting arm that rises/falls; can ride a dolly.
- **Crane** — a bigger boom that extends and sweeps; CU↔EWS in one move.
- **Steadicam** — body-mounted; follows action through space, multiple setups in one take.

**Specialised**:
- **Dutch tilt** — canted horizon; off-balance unease (even a few degrees adds interest).
- **Zolly / "Hitchcock effect"** — simultaneous zoom + dolly in opposite directions; subject size stays fixed while the background warps (*Vertigo*, *Goodfellas*).
- **Sleeper / corkscrew** — looking down while the camera rotates (*Psycho* shower coda).

Because drawing every perspective change over a move is impractical, boards indicate travel with **block arrows**. This whole vocabulary is the `CameraMovement` / `MotionSpeed` grammar in [grip.py](../../../sequitur/crew/grip.py).

## Lens and perspective

Lenses are noted in millimetres; ~50 mm ≈ the human eye is the baseline to distort from. In a drawing, **vanishing-point spacing encodes the lens**: far apart = long/narrow; close together = short/wide (never keep two VPs inside the picture — too much distortion).
- **Long / narrow (40–120 mm+)** — compresses and flattens space; shallow depth of field throws fore/background soft; can feel claustrophobic; lets far-apart actors read as touching.
- **Short / wide (15–40 mm)** — reveals fore- and background, exaggerates size change and speed as things approach; deep focus (hard edges front to back); low numbers distort (a big foreground hand, small body).
- **Fisheye (≤18 mm)** — extreme "bowl of water" distortion; comedic or uneasy.
- **Zoom** — magnifies without moving the camera; unnatural, little parallax; used sparingly.
- **Rack focus** — shift focus within one shot to redirect the eye between planes.

These map onto `FocalLength` and `DepthOfField` in [camera.py](../../../sequitur/crew/camera.py).

## Screen direction and the 180° rule

Placement is described as **screen left / screen right**; once a character is established on a side, keep them there for clarity as you cut closer. **Screen direction outranks physical geography** — it's fine to shuffle where actors really stand as long as their screen side holds.

The **180° rule** ("the line") draws an axis between interacting characters (or along a mover's path); keep every shot on one side of it so directions stay consistent. Crossing it uncut — "jumping the line" — makes characters appear to swap sides. With three characters there are three axes; **group two to one side** to collapse one axis, and use distinct backgrounds as geographic anchors (Leone's *Good, the Bad and the Ugly* standoff). Cross the line only for an emotional reason, via: a **neutral shot** (dead-centre, no favoured side — the more the smoother), **moving the characters** on screen, **moving the camera** across the line in shot, or **both**. This is the continuity contract the edit layer depends on — see [Grammar of the Edit Ch. 5 — When to Cut](../../grammar%20of%20the%20edit/reference/ch05-when-to-cut.md).

## Studio application

- **This chapter is the board-artist's copy of the studio's shot grammar — and the board is where that grammar is *first committed*.** Aspect ratio, shot size, angle, eye line, movement and lens map one-for-one onto the closed enums the camera and grip roles own: `ShotSize` / `CameraAngle` / `SubjectView` / `ShootingStyle` / `FocalLength` / `DepthOfField` in [camera.py](../../../sequitur/crew/camera.py) and `CameraMovement` / `MotionSpeed` in [grip.py](../../../sequitur/crew/grip.py). The overlap is deliberate: a storyboard panel encodes exactly the vocabulary the cinematographer later re-owns on set.
- **A board panel is a pre-rendered `Shot`, so it lands as an `ImageStudio` keyframe.** Because the panel already carries size/angle/lens/composition, it composes cleanly into a still that the video studio conditions on — see [image.py](../../../sequitur/image.py) and the [`Shot`](../../../sequitur/shot.py) aggregate. The board is upstream of the DP: the artist commits the framing; the [Cinematographer](../../../sequitur/crew/camera.py) role realises it.
- **Overlaps the sibling shot grammar — treat this as the same axes seen from the drawing board.** Cross-reference [Grammar of the Shot Ch. 1 — The Shots](../../grammar%20of%20the%20shot/reference/ch01-the-shots.md) (sizes), [Ch. 2 — Composition](../../grammar%20of%20the%20shot/reference/ch02-shot-composition.md) (eye line, screen placement), and [Ch. 6 — Dynamic Shots](../../grammar%20of%20the%20shot/reference/ch06-dynamic-shots.md) (movement). Screen direction / the 180° line is the continuity contract that the cut inherits — [Grammar of the Edit Ch. 5](../../grammar%20of%20the%20edit/reference/ch05-when-to-cut.md).
- **"You place the camera where you place your audience" is a default-picking heuristic.** Height, proximity and eye line are levers on emotional involvement, not neutral geometry — the same intent that biases the [Director](../../../sequitur/crew/director.py)'s and roles' `heuristic` defaults ([role.py](../../../sequitur/crew/role.py)). Which value a role reaches for is an emotional decision (see Ch. 6 — Emotion).
