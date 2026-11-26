# Rendering and functional validation

Local browser preview uses Python-Markdown and GitHub-like image wrapping, content width, typography and light/dark colors. It does not emulate GitHub's sanitizer or Camo proxy; live rendering is checked separately when the branch is available.

Executed matrix: viewports 1100, 850, 600 and 375 px, both themes. All eight loaded every image and showed no horizontal document overflow. At narrow widths the hero, quant plate, skyline and research plate use recomposed picture sources. Intrinsic-width module images wrap into a single column. Browser text-bounds inspection found no clipped text in the hero variants, four flagship posters, longest research name, four technology panels, both telemetry panels, both skyline variants, quant/research variants and footer.

Visual inspection: full desktop dark and mobile light screenshots reviewed. The original wide skyline clipped its first corner; the projection origin/spacing was corrected before final capture. Windows default text decoding initially corrupted bullet glyphs in project highlights; explicit UTF-8 reads corrected it. These were observed and repaired, not waived. Small metadata labels are supplementary; core identity and project descriptions have text alternatives and ordinary Markdown context.

Initial test run: 13/16 passed; three atomic-file tests hit Windows virtual-temp WinError 650. Tests were moved to workspace-volume temporary directories, retaining the real atomic replacement operation. All 16 then passed. Tests cover live-snapshot schema, malformed/missing dates, private metadata, missing counts, changed HTML, mocked 403/429/offline behavior, no-change commits, last-good preservation, streak boundaries, valid all-zero calendars, deterministic rendering, bounded Lorenz integration and REST pagination. Mocked failure cases are not live service tests.

PNG evidence is in `screenshots/`; concept PNGs in `concepts/`. Full live integration and final validation outputs are summarized in the final release report. Structural SVG/XML checks cannot prove aesthetic quality; the browser captures and human-readable review supplement them.
