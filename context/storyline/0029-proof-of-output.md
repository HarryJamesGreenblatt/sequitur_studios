# 0029 — Proof of Output (are we spinning yarn?)

> Date: 2026-08-13 · Focus: **verification** — stopped describing and *produced*. Rendered
> real bytes from both ends of the studio (a still and, for the first time ever, a video),
> and turned the un-deletable **Test** work-item types into the board's **QC / acceptance
> layer**. Verdict: **not spinning yarn** — the grammar → prompt → pixels chain genuinely
> works, on every backend.

---

## What happened

- **Rendered a real still.** A grammar-composed shot (long shot / low angle / wide / deep DoF
  / low-key / hard / cool) went through `ImageStudio` → Azure Foundry `gpt-image-1` and
  produced a genuine **2.0 MB PNG** whose every Bowen layer is legibly present on screen. The
  decision plane and the execution plane work *together*, not just in the abstract.

- **Rendered the first-ever video — the headline premise.** The studio's whole reason for
  being is **Gemini Omni Flash**, and it had *never been run*: the Gemini key has an odd format
  (`AQ.A…`, not the classic `AIzaSy…`) and had never made a live call. This session fired it —
  a motion shot (MCU / slow dolly-in / shallow DoF / low-key / cool) through `Studio` — and it
  **authenticated and returned a valid 2.1 MB MP4** (`ftyp isom`). The marquee feature is real.

- **Repurposed the Test types as QC.** The `Test Case` / `Test Plan` / `Test Suite` work-item
  types couldn't be disabled (`VS402805`) and had read as clutter. They are, in fact, the
  ADO-native home for **acceptance / QC testing** — which is a genuine finishing-department
  concept already in the grounding (`Sequence.validate`, Rose Ch. 18, the Color Correction
  Handbook broadcast-safe gate). Stood up a **Test Plan "Output Verification"** with a suite per
  renderer, each case passing only when *real bytes* are produced, executed as tracked test runs.

## Decisions

1. **Verify by producing, not by asserting.** The honest answer to "does this work?" is an
   artifact you can open, not a passing unit test over mocked seams. Both renders were inspected
   as real files (PNG/MP4 magic bytes) and, for the still, by eye against the grammar.

2. **The un-deletable becomes the QC department.** Rather than fighting the leftover Test types,
   give them the job the domain already has for them — acceptance testing of the studio's
   output — so the board now carries green, evidence-backed proof per renderer.

## Resulting state — the scorecard

| Renderer | Output | Status |
|---|---|---|
| Still — `gpt-image-1` | 2.0 MB PNG, grammar-legible | ✅ proven (this session) |
| **Video — Gemini Omni** | 2.1 MB MP4 (`ftyp isom`) | ✅ **proven (this session — first live call)** |
| Voice — Azure Speech | dry 48 kHz/16-bit/mono WAV | ✅ proven (`0011`) |
| Assemble — board-to-board | a graded `Sequence` | ✅ proven (`0027`) |

- Board QC: **Test Plan "Output Verification"** → suites *Still (Image)* and *Video (Omni)*, each
  with a passing Test Case and a completed test run recording the evidence. Render artifacts live
  in the gitignored `output/verification/`; **no `sequitur/` code changed** — this was a
  verification session.

## Open threads

- **QC suites for the rest** — add *Voice* and *Assemble* cases to the plan for completeness (both
  already proven, just not yet recorded as board runs).
- **Automate the gate** — wire an actual `validate()` (edit continuity, color broadcast-safe, sound
  levels) as the machine-checked half of these acceptance cases, so QC isn't only manual.
- The standing craft threads are unchanged: **per-shot grade matching** (Color Correction Handbook
  Ch. 9), scene-scoped board reads, and writing work-item **State** on a board-to-board run.
