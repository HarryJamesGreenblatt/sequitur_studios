"""The Director — the reconciler that assembles the crew's contributions.

The Director is itself a :class:`~sequitur.crew.role.Role`, but its job is not to
own a vocabulary — it is to reconcile the rest of the crew into a single decision
(storyline 0008: "agency lives in a component, never the container"). In the shoot
phase that decision is a :class:`~sequitur.shot.Shot`: each department fills its
*owned* fields and the Director merges them. Because the departments own disjoint
slices of the shot, the merge is conflict-free.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ..render import Medium, renderer_for
from ..shot import Shot
from .role import Department, Role

if TYPE_CHECKING:
    from ..edit import Sequence
    from ..render import RenderResult
    from .role import Brief, Contribution


class Director(Role):
    """Reconciles the crew's contributions into a single decision (a Shot)."""

    title = "Director"
    department = Department.DIRECTION

    def reconcile(self, brief: Brief, contributions: list[Contribution]) -> Shot:
        """Merge the crew's owned fields into a complete :class:`Shot`."""
        fields: dict = {}
        for contribution in contributions:
            for key, value in contribution.fields.items():
                if value is not None:
                    fields[key] = value
        return Shot(
            scene=brief.scene,
            mood=brief.mood,
            audio=brief.audio,
            aspect_ratio=brief.aspect_ratio,
            **fields,
        )

    def execute(
        self,
        shot: Shot,
        *,
        medium: Medium = Medium.VIDEO,
        out_path: str | Path | None = None,
    ) -> RenderResult:
        """Close decision -> pixels: render a greenlit :class:`Shot`.

        Reconciling chooses the shot; this hook *executes* it. It resolves the
        producer for ``medium`` from the renderer registry (storyline 0021) and hands
        it the Shot, which the backend composes through
        :func:`~sequitur.prompt.build_prompt`. Video (Gemini Omni) and still
        (``gpt-image``) are the media that render a Shot; the default is video, the
        studio's headline medium. The Director stays backend-agnostic — it holds a
        renderer *by medium*, never a concrete class.
        """
        return renderer_for(medium).render(shot, out_path=out_path)

    def assemble(self, brief: Brief, contributions: list[Contribution]) -> Sequence:
        """Reconcile the assemble crew into a graded edit :class:`~sequitur.edit.Sequence`.

        The Editor contributes the cut structure (``cut``), the Colorist a base
        ``grade``; the Director lays the coverage into one scene, attaching a copy of
        the base grade to each clip (the anchor look — per-shot matching, Ch. 9, is a
        later refinement).
        """
        from ..edit import Act, Beat, Clip, Edit, Scene, Sequence
        from ..grade import Grade
        from .editorial import EditReason, Transition

        fields: dict = {}
        for contribution in contributions:
            for key, value in contribution.fields.items():
                if value is not None:
                    fields[key] = value
        cut = fields.get("cut", [])
        base = fields.get("grade")

        scene = Scene()
        for i, shot in enumerate(brief.shots):
            transition, reason = (
                cut[i] if i < len(cut) else (Transition.CUT, EditReason.INFORMATION)
            )
            grade = Grade(ops=list(base.ops), name=base.name) if base is not None else None
            scene.beats.append(
                Beat(Clip(shot, grade=grade), Edit(transition=transition, reason=reason))
            )
        return Sequence(acts=[Act(scenes=[scene])], aspect_ratio=brief.aspect_ratio)
