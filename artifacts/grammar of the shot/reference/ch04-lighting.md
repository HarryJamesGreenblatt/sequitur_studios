# Chapter 4 — Lighting Your Shots

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Ch. 4.
> **Scope:** the full lighting vocabulary — color temperature, exposure, hard vs
> soft quality, high/low-key contrast, three-point method, lighting direction,
> and motivation. This is the source for the lighting layers, and it's why
> "lighting" is modeled as *several orthogonal axes* (`LightQuality` ·
> `LightScheme` · `LightDirection` · `ColorTemperature`), not one enum.

## Core idea

Light is the most powerful (not the most expensive) creative tool. It builds
depth, guides the eye, sets mood, and carries subtext. Every lighting choice
lives on one of a few independent axes — **color, quantity (exposure), quality,
contrast/scheme, direction, and motivation** — which combine freely.

## Color temperature (the color axis)

Measured in **degrees Kelvin**. Two anchors:
- **~3200 K — tungsten / "warm" / amber-orange.** Firelight, candles, interiors.
  Warm tones *advance* toward the viewer.
- **~5600 K — daylight / "cool" / blue.** Noon sun, overcast, moonlight, morgues.
  Cool tones *recede*.

**White balance** tells the camera which temperature to treat as neutral; mismatch
tints the image (daylight on a tungsten setting → blue; tungsten on daylight →
amber). **Gels** (CTO/CTB) or tunable LEDs correct or intentionally mix — e.g. the
classic warm-practical / cool-moonlight-through-window contrast.

## Quantity of light (exposure)

Three exposure levers: **quantity on scene**, **aperture / f-stop** (open = more
light + shallower DOF), **shutter speed** (faster = crisper but needs more light).
**ISO / sensitivity** amplifies signal — high ISO rescues low light but adds noise.
- **Overexposure** → blown highlights (unrecoverable). **Underexposure** → crushed
  shadows + noise. "Proper" exposure is whatever the story needs.
- **More light → deeper DOF** (you stop down); less light → shallower DOF. Lighting
  and focus are coupled (see Ch. 3).

## Quality of light: hard vs soft

- **Hard** (point source — bare sun, spot, Fresnel): crisp-edged shadows,
  directional, controllable, makes objects "pop"; good for rims/kicks, noir,
  drama; unflattering top-front on faces. *Encoded as `LightQuality.HARD`.*
- **Soft** (diffused/bounced — overcast, softbox, bounce card, ring light): faint
  shadows, wraps around contours, flattering, natural for interiors; warmth /
  romance. *Encoded as `LightQuality.SOFT`.*

## Contrast & scheme

- **Low-key** — high contrast, deep shadows, **chiaroscuro**; moody, dramatic,
  adds 3D modeling. *Encoded as `LightScheme.LOW_KEY`.*
- **High-key** — low contrast, even, bright, flat; friendly, "safe", multi-cam TV
  (news, sitcom). *Encoded as `LightScheme.HIGH_KEY`.*
- **Lighting / contrast ratio** = key+fill : fill. `1:1` = flat/high-key; `8:1` =
  deep-shadow/low-key.
- **Color saturation** rises with light energy; saturated + high contrast = vivid
  "snap"; desaturated + low contrast = vintage/somber. Color also carries symbolic
  subtext (a character's signature hue, a location's palette).

## Three-point method (the standard build)

*Encoded as `LightScheme.THREE_POINT`.* Three **jobs**, not three fixtures:
- **Key** — main source; ~45° off lens axis (horizontal & vertical), above head.
- **Fill** — opposite side, ~45° off axis; controls contrast by filling the key's
  shadows (a bounce card works).
- **Back** (rim/kicker) — behind subject; edge-light that separates from the
  background and adds depth.

Not mandatory — start with *one* light, add only what the look needs.

## Direction (angle of incidence) — a distinct axis

- **Front** → flattens features, kills 3D (fashion/beauty).
- **Side** (90°) → splits the face bright/dark along the nose; mystery, duality.
- **Back / rim / kicker** → separation, halos; backlight rain/fog/wet surfaces.
- **Top** → "butterfly"; eyes fall into shadow → distrust.
- **Under** → ghoulish/unnatural; horror, or phone/screen glow.

## Motivation & practicals

Fiction lighting should be **motivated** — appear to come from a source in the
world (lamp, window, fire, screen), so film lights match that source's direction,
quality, and color. A **practical** is an in-frame working fixture (usually
accent-level, augmented by hidden film lights).

Named looks worth keeping: **`ColorTemperature.GOLDEN_HOUR`** (warm low sun),
**`LightScheme.SILHOUETTE`** (expose for bright BG, subject goes black),
**`LightScheme.NATURAL`** (motivated practical sources), plus the **eye light /
catch light** (a glint in the eye = "the spark of life"; its absence reads as
dead/evil) — carried by the `Shot.eye_light` flag.

## Studio application

- Lighting is encoded as **four orthogonal layers** on `Shot`, mirroring this
  chapter, so a shot can be soft + low-key + side-lit + warm all at once:
  **`LightQuality`** (hard/soft) · **`LightScheme`** (high/low-key, three-point,
  natural, silhouette) · **`LightDirection`** (front/side/back/top/under) ·
  **`ColorTemperature`** (warm/neutral/cool/mixed/golden-hour), plus the
  **`eye_light`** catch-light flag.
- Motivation and practicals matter most once the **sequence** layer needs
  scene-consistent light across shots — a future cross-shot concern, not a
  per-`Shot` field.
- Prompt-ready phrases the layers compose into: "warm 3200K practical lamplight,
  low-key, hard side light splitting the face", "soft high-key daylight, catch
  light in the eyes", "cool moonlight backlight rimming the subject".
