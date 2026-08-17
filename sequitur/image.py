"""The Sequitur Studios still-image renderer — a thin, correct wrapper over an
Azure Foundry ``gpt-image`` deployment for generating stills from the same
grammar the video studio uses.

This is the second render backend (alongside :class:`~sequitur.studio.Studio`),
and the first non-Google one — proof that the grammar is model-agnostic and the
renderer is a swappable seam. Its home department is the Production Designer
(concept art, look-dev); its higher-leverage use is producing a **reference
keyframe** the video studio can condition a shot on.
"""

from __future__ import annotations

import base64
import time
from contextlib import ExitStack
from pathlib import Path

from .config import OUTPUT_DIR, AzureImageConfig, get_azure_image_config
from .render import Medium, RenderResult
from .shot import Shot
from .prompt import build_image_prompt

# gpt-image supports a fixed set of sizes; map the studio's aspect ratios onto them.
_SIZE_BY_ASPECT = {
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "1:1": "1024x1024",
}


class ImageStudio:
    """A still-image render session backed by Azure Foundry ``gpt-image``.

    render() -> generate a still from a prompt or a Shot; returns (result, path).
    Pass ``references`` (locked cast keyframes) to *condition* the render on those
    images via the edits endpoint — the casting-consistency lock (storyline 0055).
    """

    medium = Medium.STILL

    def __init__(self, config: AzureImageConfig | None = None, *, client=None) -> None:
        # An injected ``client`` (tests / a custom transport) skips endpoint discovery
        # and credential setup — construction then needs no Azure deps or network.
        if client is not None:
            self.config = config or get_azure_image_config()
            self.client = client
            return

        # Imported lazily so --dry-run and the video path need no Azure deps.
        from openai import AzureOpenAI

        self.config = config or get_azure_image_config()

        if self.config.api_key:
            self.client = AzureOpenAI(
                azure_endpoint=self.config.endpoint,
                api_key=self.config.api_key,
                api_version=self.config.api_version,
            )
        else:
            from azure.identity import (
                DefaultAzureCredential,
                get_bearer_token_provider,
            )

            token_provider = get_bearer_token_provider(
                DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default",
            )
            self.client = AzureOpenAI(
                azure_endpoint=self.config.endpoint,
                azure_ad_token_provider=token_provider,
                api_version=self.config.api_version,
            )

    def render(
        self,
        shot: Shot | str,
        *,
        aspect_ratio: str | None = None,
        size: str | None = None,
        out_path: str | Path | None = None,
        references: list[str | Path] | None = None,
    ):
        """Generate a still image. Returns (result, saved_path).

        When ``references`` (paths to locked keyframes — e.g. a cast Actor's audition
        reference, storyline 0055) are given, the render is *conditioned* on those
        images through the gpt-image **edits** endpoint, so the same face/identity
        carries across frames — the consistency payoff a text prompt cannot guarantee.
        Without references it takes the plain generation path.
        """
        if isinstance(shot, Shot):
            prompt = build_image_prompt(shot)
            aspect_ratio = aspect_ratio or shot.aspect_ratio
            # The backend owns *how* it conditions on a Shot's cast (storyline 0057):
            # derive the locked references from the cast unless the caller overrides.
            if references is None:
                references = shot.locked_references() or None
        else:
            prompt = shot
            aspect_ratio = aspect_ratio or "16:9"

        size = size or _SIZE_BY_ASPECT.get(aspect_ratio, "1024x1024")

        if references:
            result = self._edit(prompt, references, size)
        else:
            result = self.client.images.generate(
                model=self.config.deployment,
                prompt=prompt,
                size=size,
                n=1,
            )
        return RenderResult(result, self._save(result, out_path))

    # -- internals ---------------------------------------------------------

    def _edit(self, prompt: str, references: list[str | Path], size: str):
        """Render conditioned on ``references`` via the gpt-image edits endpoint.

        A reference may be a local path *or* a durable share URL (a
        :class:`~sequitur.output.GraphOutputStore` ref); a URL is fetched to bytes first
        (fetch-then-condition, storyline 0058) so the edits endpoint always gets bytes.
        """
        import io

        from . import output

        with ExitStack() as stack:
            images = []
            for ref in references:
                s = str(ref)
                if s.startswith(("http://", "https://")):
                    handle = io.BytesIO(output.fetch_reference(s))
                    handle.name = s.rsplit("/", 1)[-1] or "reference.png"
                    images.append(handle)
                else:
                    images.append(stack.enter_context(open(Path(s), "rb")))
            return self.client.images.edit(
                model=self.config.deployment,
                image=images,
                prompt=prompt,
                size=size,
                n=1,
            )

    def _save(self, result, out_path: str | Path | None) -> Path:
        path = Path(out_path) if out_path else OUTPUT_DIR / f"still_{int(time.time())}.png"
        path.parent.mkdir(parents=True, exist_ok=True)

        b64 = result.data[0].b64_json
        if not b64:
            raise RuntimeError("Image generation returned no image data.")
        path.write_bytes(base64.b64decode(b64))
        return path
