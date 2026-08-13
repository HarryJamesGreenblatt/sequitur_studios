"""The Grader — executes a grade into a graded clip via a 3D LUT + ffmpeg.

Colour counterpart to :class:`sequitur.cutter.Cutter`: the grade grammar in
:mod:`sequitur.grade` *decides* the colour operations; the Grader *executes* them
over a rendered artifact. It is a **medium-preserving Transform** (storyline 0022):
it consumes one already-rendered clip or still and returns the *same* medium,
decorating a producer's output rather than generating from scratch — so re-grading
never re-invokes the (expensive, non-deterministic) generative backend.

Execution is the industry-standard **3D-LUT** path (storyline 0024): the grade's
primaries are baked into a spec-correct ``.cube`` by :mod:`sequitur.lut`
(colour-science, so the ASC CDL maths and the LUT format are not hand-cooked), then
ffmpeg's ``lut3d`` applies it. The bake (:func:`sequitur.lut.bake`) is a pure
function, unit-testable without an ffmpeg binary; only the fast application shells
out.
"""

from __future__ import annotations

import re
import subprocess
import time
from pathlib import Path

from .config import OUTPUT_DIR
from .grade import Grade
from .render import Operation, RenderResult


class Grader:
    """Apply a :class:`~sequitur.grade.Grade` to a rendered artifact via a 3D LUT.

    apply() -> bake the grade's primaries into a ``.cube`` (colour-science) and apply
    it with ffmpeg's ``lut3d``, writing a graded artifact of the same medium.
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

        # An identity grade is a copy — no needless re-encode.
        if grade.is_identity:
            import shutil

            shutil.copyfile(src, out)
            return RenderResult(None, out)

        # Author the LUT (colour-science) beside the output for provenance, then
        # apply it with ffmpeg. Run ffmpeg in the LUT's directory and reference it by
        # a sanitised bare filename, sidestepping filtergraph path-escaping (Windows
        # drive colons / spaces break `-vf lut3d=file=...`).
        from imageio_ffmpeg import get_ffmpeg_exe

        from .lut import write_cube

        cube = out.parent / f"{re.sub(r'[^A-Za-z0-9_.-]', '_', out.stem)}.cube"
        write_cube(grade, cube)
        cmd = [
            get_ffmpeg_exe(),
            "-y",
            "-i",
            str(src.resolve()),
            "-vf",
            f"lut3d=file={cube.name}",
            str(out.resolve()),
        ]
        proc = subprocess.run(cmd, cwd=str(cube.parent), capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"ffmpeg failed to apply the grade:\n{proc.stderr}")
        return RenderResult(proc, out)
