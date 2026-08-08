# Appendix A — Aspect Ratios (abridged)

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Appendix A.
> **Scope:** why frame shapes differ, and what that means for `Shot.aspect_ratio`.

## The short history

- Classical Hollywood 35 mm settled near **1.33:1 (4:3)**; when TV boomed in the
  late 1940s–50s it adopted that same 1.33:1 to reuse the film libraries.
- To compete with TV, cinema went **wide**: VistaVision (1.5:1), CinemaScope
  (2.4:1 anamorphic), later IMAX (1.43:1 / 1.9:1), and the cheaper **1.85:1** that
  became the North American widescreen standard.
- The old 4:3 TV frame couldn't show those widths, forcing two fixes:
  - **Pan & scan** — crop the wide frame to 4:3; *destroys the original
    composition*.
  - **Letterbox** — keep the full width with black bars top/bottom; preserves
    intent.
- **HDTV 16:9 (1.78:1)** finally matches feature framing, so the pan-and-scan
  compromise largely disappeared. **Pillarboxing** is the inverse: a 4:3 image
  padded with bars left/right inside a 16:9 frame.

## Studio application

- `Shot.aspect_ratio` defaults to **16:9**; **9:16** is the vertical/social frame
  (see Ch. 1–2 on its compositional cost).
- The lesson that matters for generation: **shape is a compositional decision, not
  a crop after the fact** — pan-and-scan is the cautionary tale. Compose for the
  target ratio from the start.
