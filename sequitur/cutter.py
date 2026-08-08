"""The Cutter — executes an edit into a finished film with MoviePy.

Counterpart to :class:`~sequitur.studio.Studio` and
:class:`~sequitur.image.ImageStudio`: the edit grammar in :mod:`sequitur.edit`
*decides* the cuts; the Cutter *executes* them over the rendered coverage. It is a
deliberately **separate, swappable module** — the model layer (``edit.py``) stays
free of any rendering dependency so its decision state can live in a production
plan (a PM framework: Planner / ADO / GitHub Projects; see storyline 0005 / 0007),
while MoviePy lives only here on the data plane and is imported lazily.
"""

from __future__ import annotations

import time
from pathlib import Path

from .config import OUTPUT_DIR
from .edit import Sequence, Transition


class Cutter:
    """Assemble a :class:`~sequitur.edit.Sequence`'s coverage into one film.

    render() -> stitch each clip's rendered ``source`` at its timeline position,
    applying the edit's transitions; returns the saved path.
    """

    def render(
        self,
        sequence: Sequence,
        out_path: str | Path | None = None,
        *,
        fps: int = 24,
    ) -> Path:
        """Render the sequence to an .mp4. Raises if the edit is not renderable."""
        errors = [i for i in sequence.validate() if i.startswith("error")]
        if errors:
            raise ValueError(
                "Cannot render: the edit has blocking errors:\n  " + "\n  ".join(errors)
            )

        timeline = sequence.timeline()
        if not timeline:
            raise ValueError("Nothing to render: the sequence is empty.")

        missing = [e for e in timeline if not e.clip.source]
        if missing:
            raise ValueError(
                f"{len(missing)} of {len(timeline)} clip(s) have no rendered `source` to "
                "stitch — render the coverage (Studio) before cutting."
            )

        # Lazy import so edit.py and the model layer never require MoviePy.
        from moviepy import CompositeVideoClip, VideoFileClip, vfx

        placed = []
        for entry in timeline:
            vc = VideoFileClip(entry.clip.source)
            effects = self._transition_effects(entry.edit_in.transition, entry.edit_in.duration, vfx)
            if effects:
                vc = vc.with_effects(effects)
            # timeline() already offsets dissolves/wipes into the prior clip's tail.
            placed.append(vc.with_start(entry.start))

        film = CompositeVideoClip(placed)
        path = Path(out_path) if out_path else OUTPUT_DIR / f"film_{int(time.time())}.mp4"
        path.parent.mkdir(parents=True, exist_ok=True)
        film.write_videofile(str(path), fps=fps)
        return path

    @staticmethod
    def _transition_effects(transition: Transition, duration: float, vfx):
        """Map an edit transition onto MoviePy incoming-clip effects."""
        d = duration or 1.0
        if transition in (Transition.FADE_IN, Transition.DIP_TO_BLACK):
            return [vfx.FadeIn(d)]
        if transition is Transition.FADE_OUT:
            return [vfx.FadeOut(d)]
        # Dissolve (and, for now, wipe) read as a cross-fade of the overlapped clips.
        if transition in (Transition.DISSOLVE, Transition.WIPE):
            return [vfx.CrossFadeIn(duration)]
        return []  # a straight cut needs no effect
