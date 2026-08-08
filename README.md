# Sequitur Studios

A small film studio built on the Gemini **Omni Flash** video model — with a
twist: every shot is composed through the **grammar of the shot** (Christopher
J. Bowen), so the studio speaks proper cinematographic language instead of vague
prompts.

## Setup

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your key (never committed)
Copy-Item .env.example .env
#    then edit .env and paste your Sequitur Studios Gemini key
```

## First render

```powershell
# Preview the composed prompt without spending a call:
python scripts/generate.py "an old fisherman mending nets on a weathered dock" `
    --size mcu --view three-quarter-front --angle low --move dolly-in `
    --scheme low-key --quality soft --color-temp golden-hour `
    --mood "weathered, resolute" --audio "gulls, distant surf, no dialogue" --dry-run

# Drop --dry-run to actually render to output/clip_*.mp4
```

From Python / a chat session:

```python
from sequitur import Studio, Shot, ShotSize, CameraMovement, LightScheme

studio = Studio()
shot = Shot(
    scene="a lone astronaut drifting past a cracked visor reflection of Earth",
    size=ShotSize.CLOSE_UP,
    movement=CameraMovement.DOLLY_OUT,
    light_scheme=LightScheme.LOW_KEY,
    mood="awe, isolation",
    audio="only breathing and a faint radio hiss, no music",
)
interaction, path = studio.render(shot)
print(path)

# Iterate conversationally (Omni Flash is stateful):
_, path2 = studio.edit(interaction.id, "Add a slow blink. Keep everything else the same.")
```

## Layout

```
sequitur/
  grammar.py   Bowen's vocabulary as typed enums + the Shot dataclass
  prompt.py    Shot -> film-literate Omni Flash prompt
  studio.py    render() / edit() over the Interactions API
  config.py    .env loading and key handling
scripts/
  generate.py  CLI renderer (supports --dry-run)
artifacts/
  grammar of the shot/     the Bowen reference these types encode
    source/                full converted chapters (ground truth)
    reference/             abridged, session-ready references
output/        generated clips (gitignored)
```

## Roadmap

- **Sequences** — chain shots into scenes honouring the 180°/30° rules and
  match-on-action (see the continuity notes in the grammar doc).
- **Stills-first pipeline** — Nano Banana concept frames → image-to-video.
- **Shot library** — reusable named looks and camera moves.

## Model note

Built on `gemini-omni-flash-preview` (the current default video model:
native multimodal, conversational editing). Veo 3.1 remains available for
scene-extension and last-frame control when those become useful.
