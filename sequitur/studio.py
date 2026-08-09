"""The Sequitur Studios render engine — a thin, correct wrapper over the
Gemini Omni Flash Interactions API for generating and iteratively editing video.
"""

from __future__ import annotations

import base64
import re
import time
from pathlib import Path

from google import genai

from .config import OUTPUT_DIR, get_api_key
from .shot import Shot
from .prompt import build_prompt

MODEL = "gemini-omni-flash-preview"


class Studio:
    """A stateful film studio session.

    render()  -> generate a clip from a prompt or a Shot
    edit()    -> conversationally revise a previous clip (Omni is stateful)
    """

    def __init__(self, model: str = MODEL) -> None:
        self.client = genai.Client(api_key=get_api_key())
        self.model = model

    def render(
        self,
        shot: Shot | str,
        *,
        aspect_ratio: str | None = None,
        out_path: str | Path | None = None,
    ):
        """Generate a video clip. Returns (interaction, saved_path).

        The returned interaction id can be passed to :meth:`edit`.
        """
        if isinstance(shot, Shot):
            prompt = build_prompt(shot)
            aspect_ratio = aspect_ratio or shot.aspect_ratio
        else:
            prompt = shot
            aspect_ratio = aspect_ratio or "16:9"

        interaction = self.client.interactions.create(
            model=self.model,
            input=prompt,
            response_format={
                "type": "video",
                "aspect_ratio": aspect_ratio,
                "delivery": "uri",  # avoids the 4MB inline payload cap
            },
        )
        return interaction, self._save(interaction, out_path)

    def edit(
        self,
        previous_interaction_id: str,
        instruction: str,
        *,
        out_path: str | Path | None = None,
    ):
        """Revise a previous clip with a natural-language instruction.

        Keep instructions simple; add "Keep everything else the same." to hold
        continuity. Returns (interaction, saved_path).
        """
        interaction = self.client.interactions.create(
            model=self.model,
            previous_interaction_id=previous_interaction_id,
            input=instruction,
            response_format={"type": "video", "delivery": "uri"},
        )
        return interaction, self._save(interaction, out_path)

    # -- internals ---------------------------------------------------------

    def _save(self, interaction, out_path: str | Path | None) -> Path:
        path = Path(out_path) if out_path else OUTPUT_DIR / f"clip_{int(time.time())}.mp4"
        path.parent.mkdir(parents=True, exist_ok=True)

        video = interaction.output_video
        data = getattr(video, "data", None)
        uri = getattr(video, "uri", None)

        if data:
            path.write_bytes(base64.b64decode(data))
        elif uri:
            self._download_uri(uri, path)
        else:
            raise RuntimeError("Interaction returned no video output.")
        return path

    def _download_uri(self, uri: str, path: Path) -> None:
        match = re.search(r"files/([^:?/]+)", uri)
        if match:
            file_id = match.group(1)
            while True:
                info = self.client.files.get(name=f"files/{file_id}")
                state = info.state.name
                if state == "ACTIVE":
                    break
                if state == "FAILED":
                    raise RuntimeError("Video generation failed during processing.")
                time.sleep(5)
        path.write_bytes(self.client.files.download(file=uri))
