"""The Grader — executes a grade into a graded clip with ffmpeg.

Colour counterpart to :class:`sequitur.cutter.Cutter`: the grade grammar in
:mod:`sequitur.grade` *decides* the colour operations; the Grader *executes* them
over a rendered artifact. It is a **medium-preserving Transform** (storyline 0022):
it consumes one already-rendered clip or still and returns the *same* medium,
decorating a producer's output rather than generating from scratch — so re-grading
never re-invokes the (expensive, non-deterministic) generative backend.

Like the Cutter, the model layer (:mod:`sequitur.grade`) stays free of any render
dependency; ffmpeg lives only here and is resolved lazily. The stack -> filtergraph
compilation (:meth:`Grader.filtergraph`) is a pure function, so it is unit-testable
without invoking ffmpeg.
"""

from __future__ import annotations

import time
from pathlib import Path

from .config import OUTPUT_DIR
from .crew.colorist import TonalRange
from .grade import ColorBalance, Contrast, Grade, Saturation
from .render import Operation, RenderResult

#: ffmpeg ``colorbalance`` per-zone suffix for each tonal range.
_ZONE = {TonalRange.SHADOWS: "s", TonalRange.MIDTONES: "m", TonalRange.HIGHLIGHTS: "h"}


class Grader:
    """Apply a :class:`~sequitur.grade.Grade` to a rendered artifact via ffmpeg.

    apply() -> compile the reified op stack into an ffmpeg filtergraph and run it
    over the input, writing a graded artifact of the same medium (extension).
    """

    operation = Operation.GRADE

    def apply(
        self,
        artifact,
        grade: Grade,
        *,
        out_path: str | Path | None = None,
    ) -> RenderResult:
        """Grade ``artifact`` (a path, str, or :class:`RenderResult`). Raises on a
        blocking grade error or a non-zero ffmpeg exit."""
        errors = [i for i in grade.validate() if i.startswith("error")]
        if errors:
            raise ValueError(
                "Cannot grade: the grade has blocking errors:\n  " + "\n  ".join(errors)
            )

        src = Path(getattr(artifact, "ref", artifact))
        if not src.exists():
            raise ValueError(f"Nothing to grade: source artifact {src} does not exist.")

        out = Path(out_path) if out_path else OUTPUT_DIR / f"graded_{int(time.time())}{src.suffix}"
        out.parent.mkdir(parents=True, exist_ok=True)

        # Lazy import so the model layer and --dry-run never require ffmpeg.
        import subprocess

        from imageio_ffmpeg import get_ffmpeg_exe

        cmd = [get_ffmpeg_exe(), "-y", "-i", str(src)]
        graph = self.filtergraph(grade)
        if graph:
            cmd += ["-vf", graph]
        cmd.append(str(out))

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"ffmpeg failed to apply the grade:\n{proc.stderr}")
        return RenderResult(proc, out)

    @staticmethod
    def filtergraph(grade: Grade) -> str:
        """Compile a grade's ordered op stack into an ffmpeg ``-vf`` filter chain.

        Contrast maps to ``eq`` (lift->brightness, gamma->gamma, gain->contrast — a
        documented approximation of true lift/gamma/gain); colour balance maps
        exactly onto ``colorbalance`` per-zone RGB; saturation onto ``eq``. Ops that
        are neutral contribute nothing, so an identity grade compiles to ``""``.
        """
        filters: list[str] = []
        for op in grade.ops:
            if isinstance(op, Contrast):
                parts = []
                if op.lift:
                    parts.append(f"brightness={op.lift:g}")
                if op.gamma != 1.0:
                    parts.append(f"gamma={op.gamma:g}")
                if op.gain != 1.0:
                    parts.append(f"contrast={op.gain:g}")
                if parts:
                    filters.append("eq=" + ":".join(parts))
            elif isinstance(op, ColorBalance):
                z = _ZONE[op.range]
                parts = []
                if op.r:
                    parts.append(f"r{z}={op.r:g}")
                if op.g:
                    parts.append(f"g{z}={op.g:g}")
                if op.b:
                    parts.append(f"b{z}={op.b:g}")
                if parts:
                    filters.append("colorbalance=" + ":".join(parts))
            elif isinstance(op, Saturation):
                if op.amount != 1.0:
                    filters.append(f"eq=saturation={op.amount:g}")
        return ",".join(filters)
