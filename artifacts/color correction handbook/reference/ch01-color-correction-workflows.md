# Chapter 1 — Color Correction Workflows

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 1.
> **Scope:** where the colorist sits in the postproduction pipeline (preproduction advice through finishing/mastering), the acquisition-format choices that determine grading latitude, the digital-dailies handoff, and the **round-trip** — locking the edit, reconforming to camera-original media, grading, and sending the graded timeline back for finish.

## Core idea

- Grade **every** project — cinema, broadcast, or web — the workflow is the same. Grading is **not** primarily curative (fixing problems / broadcast-safe); it exists to make a program **look as good as it can**: emphasize the important image detail and lend a sense of **style and occasion**.
- Color correction **ideally starts in preproduction**, not at the tail of post. Small decisions made early (format, metadata, timeline hygiene) are the difference between a five-minute conform and days of tedious work.

## Where the colorist fits in post

A staged pipeline; the colorist can meaningfully touch every stage, but the **grade** is the main event.

| Stage | Colorist's involvement |
|-------|------------------------|
| **Preproduction** | recommend shooting formats; run camera tests; bake looks into evaluation **LUTs** for on-set displays |
| **Production** | the **DIT** carries colorist skills on-set (evaluate images, manage video village, on-set grades, dailies); colorist↔DIT communication exchanges grade data |
| **Editing** | camera-original → editable **digital dailies**; sometimes an "offline color" pass for test screenings |
| **VFX** | grade/match greenscreen elements; re-grade finished VFX shots folded back into the cut |
| **Grading** | **the main event** — once the edit locks, the timeline is **reconformed** to camera-original media and every clip is graded |
| **Finishing** | titles, slate/bars/tone, last edits, audio mix layin, light paint/blur/comp (falls to colorist at smaller shops) |
| **Mastering** | tape/SSD/DCP output — increasingly built into the grading app itself |

- **Top-level colorists focus only on the grade**; small-boutique colorists inherit more of finishing/mastering. Know which you are.

## Acquisition formats → grading latitude

The **data format** of the recorded media matters more to the colorist than the camera model. More recorded image data = more latitude for adjustment before noise/artifacts appear.

- **Film (35mm)**: scanned frame-by-frame to 2K/4K **DPX** sequences; enormous latitude. Film-scan workflows persist for archive/remaster work.
- **Raw** (RED/ARRI raw, CinemaDNG): records linear sensor data; must be **debayered/demosaiced**. ISO/aperture are **metadata** you can re-decide in the grade — huge flexibility. Costs: large data, difficult to edit directly, needs a transcode/reconform.
- **"Mastering-quality" codecs** (QuickTime **ProRes**, MXF **DNxHD**): edit-ready straight off the camera, no reconform. Choose **log-encoded** over normalized when you can.
- **H.264** (DSLR/ENG/crash-cams): highly compressed, limited latitude; profiles × levels set the quality/size tradeoff. Abominable to purists, but a job is a job — light and expose well and grade hard.

### Two levers that set latitude

- **Chroma subsampling** — how much color is kept. **4:4:4** (100%, raw/ProRes 4444/DNxHD 444) → aggressive exposure moves stay clean; **4:2:2** (high-end HD, ProRes 422) → decent latitude, broadcast-suitable; **4:2:0** (consumer/DSLR H.264) → discards ¾ of chroma, contrast pushes get noisy, greenscreen suffers.
- **Log vs. normalized (Rec.709/BT.709)** — **log-encoding** compresses scene contrast to preserve latitude within the codec's bit-depth; treat it as a **"digital negative"** (flat, desaturated, but data-rich). Normalized BT.709 is simple to monitor but throws away significant latitude. *Friends don't let friends edit log without a correction.*

### Non-improvements (don't waste time)

- **Preemptively upconverting** 4:2:0→4:4:4 or 8-bit→10/12-bit does **not** improve an already-recorded image; discarded data is gone. Grading apps promote to 32-bit float internally anyway.
- **Do** render the *final* master to a high-quality subsampling/bit-depth to **preserve** the grade's image processing.
- **"Shooting flat"** (DSLRs without log): record low-contrast data to protect highlight/shadow detail — but light the scene however you want; "flat" means the *recording*, not the *lighting*. Don't shoot *too* flat (wastes 8-bit midtone range) and know it forces a grade later.

## Digital dailies — the start of post

Raw/log media and dual-system audio must be conditioned before editors can work: **sync**, **grade**, **transcode**.

- **Syncing**: timecode-synced dual-system sound is fast and near-flawless; waveform sync (PluralEyes-style) is the fallback; manual clapperboard sync is the last resort.
- **Grading dailies**: **one-light** (a single grade across a reel — fine for offline that will be replaced at reconform) vs. **best-light** (per-clip grades to show off the media, for pickier directors or online-finishing transcodes).
- **On-set vs. in the suite**: DITs set primary grades in video village (essential for log media that looks terrible uncorrected); facility colorists set looks in advance for the DIT to reference — an increasingly **bidirectional** workflow. On-set work still needs a **color-critical, glare-shielded display** or the handed-off grade won't translate.

### Grade-data interchange (portable grade decisions)

Grades handed off from set to final finish as a starting point / reference:

- **Camera metadata** — ISO/exposure baked into raw files, re-readable at debayer time.
- **LUTs** — saved image-processing operations; load onto production displays *and* into the grading app.
- **CDL (Color Decision List)** — ASC-standard file carrying **SOP (Slope/Offset/Power)** + **SAT (Saturation)** as portable primary-grade metadata across shots and locations.

## The round-trip

Grading apps import an **EDL/XML/AAF** from the NLE and export one back — the **round-trip**:

1. **Lock the edit** (a *scheduling milestone*, not just a tech limit — unlocked edits multiply reconform hours and cost).
2. **Prep the timeline** for handoff.
3. **Export** the edit + organize its media.
4. **Grade** the project.
5. **Reconform** last-minute VFX/stock changes.
6. **Render** the final graded media.
7. **Export** the graded timeline back to the NLE/finishing app.

### Timeline prep (on a *duplicate* sequence)

- **Move all non-composited clips to V1** — grades are far easier to manage and copy on one track; leave genuine composites/transparency stacks alone.
- **Isolate unsupported effects** (long stills, freeze frames, NLE generators, exotic comps) to a superimposed track; **bake** any you must grade to a self-contained mastering-quality file, re-edit onto V1.
- **Resolve speed effects** — bake variable-speed clips (optical-flow) before handoff if the grading app won't honor them.
- **Strip editor grades/looks** the colorist can do better — but first render a **reference movie** of the whole sequence so the colorist can see edit alignment, conform order, and temp looks (beware **"temp love"**: clients bond to temp grades/music).

### Media prep, reconform, import, render

- High-quality-media edits: just export the EDL/XML/AAF + media-manage the media.
- **Offline-media edits**: **reconform** — substitute proxy clips (ProRes Proxy / DNxHD 36) with camera-original or online transcodes, matched on **filename + UUID + timecode + reel name**. Manage this metadata carefully from production onward.
- **Automatic edit detection**: notch a single master file to an EDL, or auto-detect cuts by color/contrast change — useful for archival masters with no project.
- **Render** either **individual graded clips** (reconstruct the timeline; supports eleventh-hour changes) or a single **graded master** (usually text-less, for final titling/finish).
- **Grading↔finishing** is an increasingly gray boundary; more finishing tools live inside grading apps every year, but most workflows still return to the NLE of origin.

## Studio application

*Provisional leads — the Colorist role and grade renderer are not built yet; these tie Ch. 1 to Sequitur's existing seams.*

- **A `grade` phase/department seat, downstream of the locked edit.** This chapter puts the grade *after* a locked cut and *before* finishing/mastering. In Sequitur that cut is the [`Sequence`](../../../sequitur/edit.py) the **Editor** owns; a future **Colorist** (post department, a new grade phase) would consume the **locked, rendered** `Sequence` and transform each clip. The Colorist reads the Editor's output — it does not re-decide the cut.
- **"Lock the edit" ≈ `Sequence.validate()` clean + a rendered cut.** The chapter's lock milestone maps onto the existing gate in [`Cutter.render`](../../../sequitur/cutter.py), which already **refuses to render** while `Sequence.validate()` reports blocking `error:` issues and while any clip lacks a rendered `source`. That "no blocking errors + all coverage rendered" state is the natural **lock signal** the Colorist waits on before grading.
- **Grade renderer = transform-flavor over already-rendered clips.** Grading operates on rendered media (LUT/curve/primary over each clip), which is the **execution plane** [`Cutter`](../../../sequitur/cutter.py) already occupies (MoviePy/ffmpeg over clip `source` files) — or an image model. This fits the forthcoming common **`Renderer` protocol** (`render(decision) -> (result, ref)`): the Colorist holds a grade renderer that takes a grade **decision** and returns the transformed clip + a reference.
- **CDL / LUT = a portable grade *decision object*.** SOP+SAT (and LUTs) are exactly the kind of scoped, serializable primary-grade vocabulary a Colorist role would **own** and a `HeuristicJudgment`/`PersonaJudgment` would emit as its `Contribution` — the grade analogue of how shoot roles emit shot vocabulary today.
- **Capture-vs-grade overlap to flag.** Looks/LUTs are first set at **capture** (DIT/Gaffer, on-set) and then *handed to* the **grade** (Colorist, finish) as a starting point. This mirrors the existing seam where the **Gaffer** owns `ColorTemperature` as a **capture-time light** property ([`sequitur/crew/lighting.py`](../../../sequitur/crew/lighting.py)); the Colorist will own **grade** color vocabulary. Same domain (color), two seats (capture vs. grade) — like POV living in both the Cinematographer's coverage and the Screenwriter's Taxonomy.
