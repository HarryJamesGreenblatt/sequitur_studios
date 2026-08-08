# Appendix D — Crew Positions (abridged)

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Appendix D.
> **Scope:** the roles that constitute a production studio — the taxonomy the
> studio's [workflow architecture](../../../context/architecture.md) is built on
> (role → department → grounding → code layer).

Roles grouped by department and the phase where they primarily work:

| Department | Role | Primarily does | Phase |
|-----------|------|----------------|-------|
| **Direction** | Director | interprets the script into shots; directs performance; owns the vision | pre → post |
| | Assistant Director (AD) | schedule, coverage, calls the roll | pre → prod |
| | Script Supervisor | continuity notes, take/scene logs for the edit | prod |
| **Producing** | Producer | financing, hiring, scheduling, logistics; often marketing/distribution | all |
| **Writing** | Screenwriter | writes/adapts the screenplay | pre |
| **Camera** | DP / Cinematographer | overall look; chooses shots & lighting scheme with the director | prod |
| | Camera Operator | runs the camera; framing & focus | prod |
| | Camera Assistant (AC) | camera gear, follow-focus, camera logs/slate | prod |
| | DIT / Data Wrangler | sensor calibration, on-set grade, media backup | prod → post |
| **Electric** | Gaffer | chief electric; sets the lighting fixtures with the DP | prod |
| | Electric / Lighting Tech | runs power; hoists & angles lights | prod |
| **Grip** | Key Grip | chief grip; camera/lighting support rigging | prod |
| | Grip / Dolly Grip | moves & supports things; assembles & moves the dolly/track | prod |
| **Sound** | Sound Mixer / Recordist | runs audio recording; maintains levels | prod |
| | Boom Operator | places/holds the mic with the mixer | prod |
| **Art** | Production Designer | sets, costume, make-up, overall design look | pre → prod |
| **Editorial** | Editor | cuts picture & sound into the final story | post |

## Studio application

- This taxonomy is the backbone of
  [`context/architecture.md`](../../../context/architecture.md): each department
  maps to a **grounding source** and a **code layer**. Today the studio implements
  the **Camera / Electric / Grip** departments (production phase) via
  `sequitur/grammar.py`; the rest are scaffolded as the intended shape.
- The **Editorial** department is the clear next layer — it needs *Grammar of the
  Edit* as grounding before the sequence/edit code layer can be built well.
