# Chapter 6 — Dynamic Shots: Subjects and Camera in Motion

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Ch. 6.
> **Scope:** motion — playback-speed (slow/fast), subject blocking, and every
> camera move (handheld, pan/tilt, dolly, zoom, gimbal, crane, drone) plus the
> long take. This is the source for the `CameraMovement` enum and surfaces a
> missing *temporal* axis (slow/fast motion).

## Core idea

"Movies should move." Motion is the medium's core strength and taps directly into
our response to movement. Two independent motion axes: **subject movement** (in a
static frame) and **camera movement** (the audience's proxy taking a ride). Every
move should be **motivated** and usually serve the story, not the toy.

## Playback speed (a temporal axis, not a camera move)

"Normal" ≈ 24 fps (cinema) / 30 fps (broadcast; 25 in Europe).
- **Slow motion / overcranking** — capture *above* normal fps (60/120/240), play at
  normal → slower, dramatic; needs more light, often lower resolution.
- **Fast motion / undercranking** — capture *below* normal (or drop frames in
  software) → time-lapse / hyper-lapse; condenses long events.

## Subject motion: blocking

**Blocking** = planned subject movement (vs **staging** = object placement).
Movement across frame varies composition in real time (audience **eye-trace**);
movement *into depth* reinforces 3D space. Direction can carry theme (e.g.
consistent right→left travel). Static, well-composed shots have their own energy
and contrast with moving ones.

## Camera moves

| Move | What it is | Reads as / notes |
|------|-----------|------------------|
| **Static** | Locked-off (tripod) | Stable, composed; cuts cleanly. |
| **Handheld** | Body-supported | Immediacy, energy, doc/news/amateur/vlog feel; risks shake & focus loss. Use *wide* lenses to reduce shake. |
| **Pan** | Swivel horizontally (y-axis) | Follows lateral action / reveals space. |
| **Tilt** | Pivot vertically (x-axis) | Reveals height / shifts attention up-down. |
| **Pan-tilt** | Simultaneous diagonal sweep | One-shot set-up→pay-off (eye-line reveal in-camera). |
| **Whip-pan** | Very fast pan | Editorial transition (blur A → blur B). |
| **Dolly (track/truck) in-out** | Camera physically moves toward/away | Growing intimacy (in) / reveal, release (out). Slow = "creep". |
| **Crab dolly** | Moves *parallel* to action, lens *perpendicular* | Travels alongside (lead=¾ front, level=profile, trail=¾ back). |
| **Pedestal (ped up/down)** | Whole camera rises/lowers | Vertical reposition through space. |
| **Zoom** | Optical focal-length change, camera still | Magnifies uniformly, *compresses* space; unnatural — hide within a pan/tilt or make very slow. |
| **Steadicam / gimbal** | Stabilized body/handheld rig (2-axis: pitch+roll; 3-axis: +yaw) | Dolly-smooth movement anywhere — stairs, terrain, long follows. |
| **Crane / jib** | Camera lifted & swept high | Grand reveals; establishing (open) or summation (close) shots. |
| **Drone (UAV)** | Aerial remote camera | Epic vistas + tracking; **very loud → no usable dialogue audio**; regulated. |
| **Arc / 360** | Orbit around subject | Dimensionality, drama (via gimbal/drone). |

**Dolly-in ≠ zoom-in (key distinction):** a dolly *moves the camera* → perspective
shifts, FG grows faster than BG (natural, like walking closer). A zoom *changes
optics only* → everything magnifies equally, space *compresses* (alien to human
vision). Countermoving them = the "vertigo"/dolly-zoom effect.

## Structure & motivation

- **Pan/tilt/dolly structure:** static **start frame** → smooth **movement** (lead
  the subject, hold headroom/look room) → static **end frame**. Static heads/tails
  give the editor clean cut points.
- **Motivate the move** — subject motion justifies the camera following. **Dolly-in**
  is natural (investigate/approach); **dolly-out** is less natural ("leading" a
  subject moving toward camera) — good for reveals, suspense, scene/film endings.
- **Developing shot** — combine moves (dolly + boom + pan + focal change) to cover
  much action in one shot; hard to execute, focus-critical.
- **Long take** — one unbroken mobile shot replacing cut coverage; immersive but
  demands many rehearsals/takes (or, for vloggers, is just a chopped single-cam
  clip with visible jump cuts).

## Studio application

- `CameraMovement` in `sequitur/grammar.py` covers the full move set —
  `STATIC/PAN/TILT/DOLLY_IN/DOLLY_OUT/TRUCK/PEDESTAL/ZOOM/CRANE/HANDHELD/
  STEADICAM/ARC` plus **`GIMBAL`**, **`DRONE`**, **`WHIP_PAN`**, **`PAN_TILT`**,
  and **`DOLLY_ZOOM`**.
- The **temporal axis** is its own `MotionSpeed` enum (slow-mo / fast-mo /
  time-lapse) on `Shot.speed` — orthogonal to `CameraMovement` and distinct from
  `Shot.timing` (timecodes), so the studio can request slow-motion directly.
- Encode the **dolly-vs-zoom** semantics in prompt phrasing ("slow dolly-in,
  perspective shift" vs "zoom-in, compressed space") — the model treats them
  differently and it matters.
- Movement is where **audio** couples to grammar (drone = no dialogue) — relevant
  since `Shot.audio` already directs sound design.
- The `single_scene` flag maps to the **long take** concept: one continuous move,
  no cuts.
