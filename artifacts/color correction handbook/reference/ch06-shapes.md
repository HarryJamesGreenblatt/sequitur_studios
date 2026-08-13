# Chapter 6 — Shapes

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 6.
> **Scope:** the second family of **secondary** corrections — isolating a region **by geometry**. Covers **shapes** (a.k.a. vignettes / masks / Power Windows / Spot Corrections): drawing and feathering a shape, inside/outside grades, combining shapes, digital relighting, and — critically — **tracking / keyframing / rotoscoping** a shape to motion. Companion to Ch. 5 (isolation **by colour**).

## Shapes vs qualifiers

- A **shape** (oval, rectangle, gradient, or Bezier/B-spline custom) draws a **grayscale matte** limiting a correction to the region **inside or outside** it. Same secondary tier as HSL, different matte source: **mask-by-region**, not mask-by-colour.
- **Prefer simple shapes** — think in **pools of light and shadow**, not traced outlines.
- **Shapes win** for digital relighting and large, cleanly-demarcated regions (sky vs forest). **Qualifiers win** for detailed or moving subjects with a distinguishable hue/luma. They're not either/or — a **shape can limit a qualifier** (and vice versa).

## Shape UI and controls

- **Simple shapes:** **Ovals** (most common — vignettes, face brightening, edge masks), **Rectangles** (windows, geometric falloff, stand-in gradients), **Gradients** (linear falloff for skies/shadows).
- Universal params: **size, aspect, position, rotation, softness** — all drivable from a control surface or on-screen handles.
- **Custom shapes:** two control-point flavours — **B-splines** (points *pull* the shape indirectly; simple, but need more points) and **Bezier** (handles set curve type/sharpness; precise). Keep points **few** — excess points make later adjustment and animation miserable.

## Feathering and softness

- **Feathering** blurs the matte edge relative to the shape — the key to an invisible border.
- Simple = one **softness slider**. Advanced = **inside / outside / master** feathering points per segment (move inner & outer apart to feather more), plus **contour** controls (Exponent/Weight) or a **Matte Curve** to shape the falloff.
- Feather so the edge is undetectable but not so wide it **halos**. Tight contrast changes ("opening up shadows") need tighter edges; even-shadow adjustments tolerate very wide feathering.

## Inverting and combining shapes

- **Invert** to flip inside/outside, or grade both sides independently (as with HSL).
- **Boolean ops** combine shapes: **join** (union / "Matte" mode), **subtract** ("Mask" mode), **intersect**. Subtract to **protect** part of a region from a background correction (e.g. keep one actor out of a darkening rectangle).
- No shape tools? Superimpose a duplicate clip + drawn mask, or apply a mask to an **adjustment layer**.

## Highlighting subjects (vignettes)

- A **vignette** darkens around a subject to draw the eye — a virtual **flag** cutting ambient light, a directional **shadow gradient** adding dimension, or a deliberate lens-vignette look.
- The **best vignette is invisible** — it masquerades as shadow justified by the scene. Real lighting control is the DP's job; the colorist imitates it.
- **Add light to faces:** a very soft oval, then **stretch contrast** (raise Gamma, lower Lift) — like adding a bounce card. Match shadow levels inside/outside and feather carefully to avoid a tell-tale **halo**.
- **Deepen shadows:** for an **equiluminant** image (subject and background at near-identical luma — test by desaturating or viewing luma-only in peripheral vision), a soft oval darkening the surround guides the eye. **Ovals often beat custom shapes** — abstract falloff reads like a practical light; a traced shape gives itself away. Feather well; avoid solid black.
- **Composited shadows:** superimpose a soft black→white gradient and **Multiply**; shifting the darkest shade toward gray changes opacity without touching layer opacity.

## Creating depth

- **Six/seven depth cues.** Three you **can't** touch in grading: **perspective**, **occlusion**, **relative motion**. Four you **can**: **luma/colour contrast**, **hue/saturation** (more-saturated and warmer subjects read **closer**), **haze/airlight** (distant = lower-contrast/bluer), **texture/depth of field**. Plus **stereopsis**.
- **Gradient/shape depth:** a soft dark-to-light ramp (rectangle feathered toward the subjects) fakes light falloff and adds depth.
- **Saturation-only depth:** boost near subjects' colour, desaturate/cool the far background — separation without touching contrast.
- **Lighting control:** flag off edge light to focus attention and deepen a night look (don't over-crush the shadows).
- **Artificial focus:** isolate the subject with a soft oval, **invert**, and **blur** the background for fake shallow depth of field.

## Shapes + HSL qualifiers

- Enabling a shape **and** a qualifier together preserves the key **only where it overlaps the shape** (an intersection) — the clean way to drop hard-to-key background fringe while keeping a detailed matte on the subject.
- **Preserve highlights:** when a darkening shape dulls a practical light, isolate that light with an **HSL key** and **subtract** it from the shape matte to restore its brightness.

## Digital relighting & image segmentation

- **Draw light and shadow:** lighten the focal subject (raise midtones, spare true blacks), darken foreground with a soft gradient shape, push competing background elements back — one region at a time.
- **Image segmentation:** mentally break a scene into discrete regions, each best served by one correction. But use the **fewest** secondaries that work — faster, lighter to render, more naturalistic. Degree of segmentation is set by the project (documentary vs stylized spot).
- **Flagging a set:** darken ambient spill on walls/ceilings to concentrate light — always work **with** the existing light/shadow, leaving space so the feathered edge stays hidden.

## Shapes and motion

- A **stationary, well-feathered shape** is fine if the subject barely moves — it can even read as a natural pool of light. Only match it to motion when the movement gives the shape away.
- **Tracking masks** (preferred): pick a feature and let the app build a **motion path** to animate the shape.
  - Point trackers: **reference pattern** (the feature) inside an **analysis region** (search area). **1-point** = position, **2-point** = +rotation, **4-point** = corner-pin, **multi-point** = per-control-point.
  - **Area trackers** (Resolve, SpeedGrade, Baselight): draw the shape, auto-analyze a **point cloud**, apply a chosen mix of **Pan/Tilt/Zoom/Rotate**; disable unwanted transforms or override bad points.
  - Track a **high-contrast, angular** feature at the **same depth** as the subject (parallax breaks distant-vs-near tracks). **Occlusion** (subject passes behind something) is the classic failure — track each side and **interpolate** between. **Mocha**/planar & 3D trackers handle the hard cases.
- **Animating masks** (when tracking fails): **keyframe** the shape; the app **interpolates** between keyframes (don't key every frame — it stutters).
- **Rotoscoping** = manually animating a shape to follow a subject that **changes shape**. Keep shapes **simple**; draw the initial shape at the subject's most complex frame; keyframe at motion **extremes**, then refine with the **divide-by-half** rule; break a subject into **overlapping shapes** that track independently. Watch feathered edges for haloing throughout.

## Studio application

Provisional leads for a future **Colorist** role and **grade renderer** (neither built yet):

- **Mask-by-region completes the secondary tier.** With Ch. 5 (mask-by-colour) this pins down the Colorist's **two-tier grade vocabulary**: a **primary** (whole-image, Ch. 3–4) grade plus **secondary** corrections whose matte source is either a **Qualifier** (colour) or a **Shape** (region). A provisional `Shape` matte (oval / rect / gradient / bezier + softness + invert) drops straight into the same `Correction.matte` seam proposed in the Ch. 5 leads.
- **Shape tracking is the animation overlap — flag it.** A shape's `position/rotation/size` become **time-varying** the moment the subject or camera moves. That is a **keyframed/animated** concern that belongs to **Ch. 7 (Animating Grades)** and maps onto the edit layer's **time model** ([sequitur/edit.py](../../../sequitur/edit.py)) — the same absolute-seconds timeline the `Cutter` flattens. Provisional lead: a static shape needs no time model, but a **tracked** shape must resolve against the clip's timeline, so the Colorist's animated-mask work should *reuse* the edit layer's keyframe/time machinery rather than grow its own.
- **Region conditioning already exists upstream.** Geometric region isolation parallels **`ImageStudio` region conditioning** ([sequitur/image.py](../../../sequitur/image.py)) and the **Editor / edit layer** compositing masks. A grade-time `Shape` and a generation-time region mask are the **same geometry, different stage** — worth a shared shape/matte primitive across the image and colour layers.
- **Grade renderer stays transform-flavor.** Shape mattes, inside/outside grades, and blurred-background DoF are all **transforms over already-rendered clips** — execute on the **`Cutter`** plane (MoviePy/ffmpeg, [sequitur/cutter.py](../../../sequitur/cutter.py)), not at image-generation time.
- **"Fewest secondaries" is a design constraint, not just craft advice.** Van Hurkman's preference for minimal segmentation argues the Colorist should emit a **short, ordered correction stack**, keeping the grade renderer's transform chain cheap — mirroring how the studio already favours a flat, explicit edit `Sequence` over deep nesting.
