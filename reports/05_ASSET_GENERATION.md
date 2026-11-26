# Reproducing the observatory

Python 3.10+; run from repository root:

```sh
python scripts/generate_assets.py
python scripts/generate_telemetry.py
python scripts/assemble_readme.py
python scripts/validate_assets.py
python -m unittest discover -s tests -v
```

Static generation reads only versioned metadata, tokens and local icons. Telemetry rendering reads the committed snapshot. `fetch_github_data.py` is the separate network step. `vendor_icons.py` is an explicit maintenance command pinned to Devicon commit `32fe1d3b3f36ad11f90ab94f7db59738139c2bf6`; it is not run by refresh jobs. SVG originals are standalone, with no remote image/font references.

## Mathematical signature

Lorenz system: `dx/dt = σ(y−x)`, `dy/dt = x(ρ−z)−y`, `dz/dt = xy−βz`.

Parameters: σ=10, ρ=28, β=8/3. Initial state (0.1, 0, 0). Classical fourth-order Runge–Kutta, Δt=0.008, 6,000 integration steps. Discard first 700 transient points. The remaining 5,300 points are projected onto x–z, independently normalized into the artwork viewport and rendered as overlapping 181-point polyline segments. This is an illustrative trajectory, not a proof of long-time numerical accuracy or a research result. Every draw is deterministic; tests verify identical trajectories and reasonable state bounds.

Quant artwork is a deterministic family of Gaussian curves: `exp(-((i−55−3k)/(18+3k))²)`, k=0…6. Explicitly labelled illustration, never market performance. FORGE heatmap uses a sinusoidal schematic; VECTRA matrices and AXIOM/PRAXIS graphs are conceptual architecture motifs, not measured traces.

## Preview

`python scripts/build_preview.py` builds ignored local HTML under `reports/preview/`. It uses installed Python-Markdown and a small GitHub-like layout approximation. Committed PNG screenshots are review evidence, not runtime assets. Full GitHub sanitizer/Camo validation is a distinct live check and is reported separately. Concept SVGs regenerate with `python scripts/visual.py`.
