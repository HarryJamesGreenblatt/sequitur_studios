# Chapter 3 — Composition for Depth, Perspective, and Focus

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Ch. 3.
> **Scope:** faking the third dimension on a flat frame — lines, the FG/MG/BG
> depth stack, lens focal length & perspective, and focus / depth of field. This
> is the chapter that gives real vocabulary to the `lens` field.

## Core idea

A single-lens camera can't see in stereo like our two eyes, so **depth is an
illusion the filmmaker constructs** — via lines, layered planes, perspective, and
selective focus. "What is in focus is the thing the viewer is told to watch."

## Compositional lines

- **Horizon line** — keep it level (parallel to top/bottom edges) unless
  intending unease. Placement is expressive: push it *low* to feature sky, *high*
  to feature ground/water. Interiors have implicit horizons (floor/wall seams,
  tabletops). Horizontals → stability, order.
- **Vertical lines** → strength, height, rigidity; also *divide* the frame and
  *separate* subjects (doorways as frames-within-frames, fence posts as bars).
  Avoid a single vertical directly behind a head.
- **Dutch / canted angle** — deliberately tilted horizon → unease, disorientation,
  "something's not right" (sickness, intoxication, chaos). *Already encoded as
  `CameraAngle.DUTCH`.*
- **Diagonal lines** → the primary depth tool. Converging parallels meet at a
  **vanishing point** (linear perspective); roads, tracks, staircases, rows lead
  the eye *into* depth. A **flat** composition (subject against a wall, no
  diagonals) reads as trapped/boxed-in — depth's *absence* is also expressive.
- **Curved lines / S-curves** → smooth curves calm and guide the eye; jumbled
  curves confuse. Curves can be *implied* by arranging people/objects.

## The depth stack: FG / MG / BG

- **Foreground** — between lens and subject; an FG element (branch, railing,
  out-of-focus shoulder) adds depth and, in a POV, implies spying. A moving FG
  object that fully blocks frame = a **natural wipe** (a hidden edit point).
- **Middle ground** — where the main action usually lives; easiest to hold in
  wider shots.
- **Background** — everything behind, out to infinity (or the back wall). Don't
  let it overpower the MG.

**Depth cues:** *overlapping* (nearer objects occlude farther), *known object
size* + linear perspective (a small skyscraper reads as distant — exploitable for
forced-perspective/miniature tricks), and *atmospherics* (haze/fog/smoke
desaturate and soften distance → implies expanse; fog machines do this on set).

## The lens: focal length & perspective

- **Focal length (mm):** low mm = **wide-angle** (broad field of view); high mm =
  **long / telephoto** (narrow, magnified). **F-stop / aperture:** low number =
  wide opening (more light, shallower DOF); high number = small opening.
- **Primes** (single FL) — sharper, faster (wider max aperture), smaller/lighter.
  **Zooms** (FL range) — convenient, but usually softer & slower. **Digital zoom
  = quality-destroying crop; avoid.**
- **Perspective is the expressive payload:**

| Lens | Effect on space | Use / reads as |
|------|-----------------|----------------|
| Wide-angle | **Expands** depth; exaggerates near/far distance; fast apparent movement toward/from lens | Small spaces look bigger; vistas/XLS; vlog selfie (~10–16 mm); **distortion at extremes = fisheye** → surreal, nightmare, "not normal". |
| Normal | Neutral, "as if you were there" | Default, natural perspective. |
| Long / telephoto | **Compresses** depth; flattens near/far; magnifies BG | Flat/constrained/prison-like feel; safe distance for action/sports; **flattering CU portraiture** (slightly long lens from further back avoids enlarged-nose distortion). |

## Focus & depth of field (DOF)

- A lens holds crisp focus at one distance — the **plane of critical focus**. The
  acceptably-sharp zone around it is the **DOF**, roughly **⅓ in front, ⅔ behind**
  the plane.
- **What's in focus = what's important.** Shallow DOF isolates the subject and
  blurs distraction (the core "cinematic" look); deep DOF keeps everything sharp
  (viewer must hunt for the subject).
- **DOF is controlled by three levers:**

| | Large (deep) DOF | Small (shallow) DOF |
|---|---|---|
| Focal length | Short / wide | Long / telephoto |
| Camera-to-subject distance | Far | Near |
| Aperture | Small hole (high f-stop) | Large hole (low f-stop) |

  In bright light, an **ND filter** cuts light so you can open the aperture and
  *keep* DOF shallow. Low light forces the aperture wide → too-shallow DOF (subjects
  drift out of focus); add light to stop down.
- **Rack / pull focus** — shift the plane of focus mid-shot from one subject to
  another (redirects attention). **Following focus** — hold focus on a moving
  subject. Both need manual (or advanced AF) focus control.

## Studio application

- Lens perspective and focus are typed: **`FocalLength`** (fisheye/wide/normal/
  long) and **`DepthOfField`** (shallow/deep); `Shot.lens` remains for free-text
  extras (e.g. "35mm anamorphic", "rack focus from FG to BG").
- **Shallow DOF** is the single strongest lever for a cinematic CU — pair it with
  the shot size in prompts.
- **Lens perspective (wide vs long)** is a distinct axis from shot size: two shots
  can be the same MCU but feel expansive vs claustrophobic purely by lens choice.
- Depth staging (**FG/MG/BG**, diagonals, atmospherics) are composition cues that
  translate directly to prompt language and strengthen the 3D read of a generated
  frame.
