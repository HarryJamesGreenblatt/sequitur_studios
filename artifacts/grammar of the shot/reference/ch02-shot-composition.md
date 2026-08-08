# Chapter 2 — Basic Motion Media Shot Composition

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Ch. 2.
> **Scope:** how to *arrange* subjects inside the frame — headroom, look room,
> the rule of thirds, the two camera-angle axes (horizontal & vertical), and
> multi-subject framings (two-shots, OTS, groups). Where Ch. 1 sized the shot,
> Ch. 2 composes it.

## Core idea

**Composition** = the purposeful placement of visual elements in the frame.
Balance is read as **weighted masses**: a subject's body and the empty
**negative space** each carry visual "weight"; a good frame balances them.

## Framing a human subject — the three guidelines

- **Headroom** — space between the head and the top edge. Tighter shots (MS/CU)
  cut *just above* the head; excess headroom wastes the frame and drops the face
  too low. **When in doubt, err to *less* headroom** — too much forces the chin
  to break the bottom edge as the subject speaks. Keep it *consistent* across
  coverage so cuts don't jump the eyeline height.
- **Look room / nose room / lead room** — empty space in front of the direction
  the subject faces or gazes. The **eye-line** has direction and implied energy;
  the void invites the audience to want to see what's looked at. *No* look room
  (face against the near edge) reads as trapped, claustrophobic, suspenseful —
  a void behind the head "cries out to be filled." Vertical (9:16) easily loses
  look room.
- **Rule of thirds** — divide the frame in thirds H & V; place interest on the
  lines or their intersections (heads at upper-third crossings). Related:
  Golden Ratio, Fibonacci.

## Shooting style: subjective vs objective

- **Subjective / direct address** — subject looks *into the lens*, addressing the
  viewer. News, hosts, vlogs, music videos, UGC. Feels connected / authoritative.
- **Objective** — subject never looks at the lens; camera is an unseen observer /
  audience proxy. The default for fiction. Looking into the lens in fiction =
  **breaking the fourth wall**. Objective framing invites the viewer to wonder
  and participate.

## Camera angle — two orthogonal axes

**Horizontal** (camera orbits the subject; describe via degrees, clockface, or
named positions):

| Position | Reads as |
|----------|----------|
| Frontal (0°/12 o'clock) | Full face, both eyes; factual but can be flat. |
| **3/4 front** | **The narrative default** — dimensional, both eyes, contoured face. |
| Profile (±90°/3 or 9 o'clock) | Only half the face; aloof, secret, "leader on a coin"; efficient for two-shots. |
| 3/4 back | Shades into an OTS; shares the subject's POV, face hidden. |
| Full back / reverse (180°/6 o'clock) | Face fully hidden; mystery, suspense, leads audience into a reveal. |

**Vertical** (lens height & tilt relative to the subject):

| Angle | On a person | On an environment |
|-------|-------------|-------------------|
| **Neutral** (lens at subject's eye height) | Equals; the default. | — |
| **High** (above, tilt down) | Small, weak, trapped/foreshortened; a *slight* down-angle flatters (the selfie angle). | Maps geography; bird's-eye / "God view" reads otherworldly. |
| **Low** (below, tilt up) | Dominant, heroic, looming, "larger than life". | Grand, imposing. |

Distinguish a **low angle** (lens *tilted up*) from a neutral shot merely taken
from ground level (lens level). Angle = the tilt, not just the height.

## Multi-subject framings

- **Profile two-shot (50–50)** — both faces in profile; LS–MLS for meetings, MCU
  forces intimacy or aggression. Both faces visible; viewer chooses focus.
- **Direct-to-camera two-shot** — side by side, open to camera (news pairs, the
  fiction **walk & talk**, car front seats). Tighter than MS overlaps bodies,
  giving **favor** to the forward subject.
- **Over-the-shoulder (OTS)** — shoot past subject A's shoulder (an "L" shape) onto
  B's face; usually MCU. Filmmaker controls who gets attention; shoot the matching
  reverse. A **dirty single** keeps just a sliver of the other character for
  orientation; a **clean single** removes them entirely.
- **Power-dynamic two-shot ("up/down")** — one head higher, one lower, even at a
  neutral angle → the higher character has the upper hand; forces high/low
  answering shots.
- **Three-shot / group** — linear across the widescreen; three heads form a
  triangle of energy. Beyond ~5, it's a group shot — rely on **blocking** (talent
  placement) and **staging** (set arrangement) so the most important, best-lit,
  in-focus face draws the eye.

## Studio application

- The **vertical** angle is `CameraAngle` (+ Dutch); Ch. 2's *orthogonal*
  **horizontal axis** is now its own `SubjectView` enum (frontal / 3-4-front /
  profile / 3-4-back / reverse), with 3/4 front as the fiction default.
- **Subjective vs objective** (direct-to-lens or not) is encoded as the
  `ShootingStyle` enum on `Shot`.
- Composition guidelines (**headroom, look room, rule of thirds**) are captured by
  the `Composition` enum (centered vs rule-of-thirds); finer cues still translate
  cleanly to prompt language ("head on the left third, gazing across open frame
  right").
- Two-shot / OTS / power-dynamic / group framings are inherently multi-subject —
  out of scope for the single-subject `Shot` today, but the vocabulary the future
  **sequence** planner needs for dialogue coverage.
