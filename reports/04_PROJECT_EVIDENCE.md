# Canonical inventory and claim boundaries

Reviewed 2026-11-26. `data/projects.json` is the display inventory; `data/evidence.json` preserves reviewed README text and blob SHAs; `data/repositories.json` contains only public metadata. Descriptions paraphrase project documentation; project benchmarks were not rerun in this profile task. No benchmark numbers are promoted into posters.

| Project | Evidence | Display scope and limitation |
|---|---|---|
| AXIOM | [README](https://github.com/Zylus08/Axiom/blob/master/README.md), [v0.1.0](https://github.com/Zylus08/Axiom/releases/tag/v0.1.0) | C++20 analytical SQL, batch operators and external sorting; read-only, restricted SQL, single-threaded |
| PRAXIS | [README](https://github.com/Zylus08/PRAXIS/blob/main/README.md), [v0.1.0](https://github.com/Zylus08/PRAXIS/releases/tag/v0.1.0) | Typed AST, RAII and validated handles; restricted C++ dialect |
| FORGE | [README](https://github.com/Zylus08/FORGE/blob/master/README.md), [release](https://github.com/Zylus08/FORGE/releases/tag/v0.1.0) | AVX2 kernels and native autograd. Release tag says v0.1.0 but title/body classify RC1 experimental; keep the more conservative RC1 label. Acceleration goal not achieved |
| VECTRA | [README](https://github.com/Zylus08/VECTRA/blob/main/README.md), [RC1](https://github.com/Zylus08/VECTRA/releases/tag/v0.1.0-rc1) | Quantized GGUF CPU inference; sustained target partial. No peak-throughput headline |
| NOMOS | [README](https://github.com/Zylus08/NOMOS/blob/master/README.md) | Sparse discovery and symbolic physical-law recovery; M1 investigation |
| JANUS | [README](https://github.com/Zylus08/Project-Janus/blob/master/README.md) | Search/UCI baseline with handcrafted evaluation. Neural evaluator is roadmap in this source |
| RoadVision | [README](https://github.com/Zylus08/RoadVision/blob/main/README.md) | Segmentation and weather robustness; small pilot rather than full Cityscapes evaluation |
| Aerospace RUL | [main.py](https://github.com/Zylus08/Rolls-Royce-Aerospace-RUL/blob/main/main.py) | Imports LSTM, GRU, TCN and comparison pipeline; no root README. Independent experiment, no employer association |
| Thermodynamic Evolution | [deployment source](https://github.com/Zylus08/Thermodynamic-Evolution-UCS503/blob/main/README_DEPLOY.md) | Rust analysis engine, Go API, sandbox boundaries. Current source is broader software-analysis infrastructure; do not claim autonomous discovery |
| Collision Lab | [README](https://github.com/Zylus08/Neural-Surrogate-Monte-Carlo-Collision-Simulator/blob/main/README.md) | Simplified collision Monte Carlo and surrogate investigation; not validated detector physics |
| Satoshi Flow | [README](https://github.com/Zylus08/Satoshi_Flow/blob/main/README.md) | Event-driven research, execution costs and walk-forward evaluation; no profitability claim |
| TradeCore | [README](https://github.com/Zylus08/TradeCore/blob/main/README.md) | Matching/replay and preallocated hot path; latency contracts are targets, not reproduced measurements |
| Regime Shift | [README](https://github.com/Zylus08/Regime-Shift/blob/main/README.md) | HMM regime detection and CVXPY allocation research |
| RiskLab | [README](https://github.com/Zylus08/RiskLab/blob/main/README.md) | Risk/stress research infrastructure; no production certification |
| DeepHedge-RL | [README](https://github.com/Zylus08/DeepHedge-RL/blob/main/README.md) | RL hedging investigation, simulated environment |
| AQC | [README](https://github.com/Zylus08/AQC/blob/main/README.md) | Quantitative research workspace; no publication claim |

SleepApnea was inspected but omitted: its root README attributes a dataset to other named researchers. This does not establish the owner's authorship or publication status. Existing scheduler work is preserved in the additional-work link. Other public repositories remain discoverable through the repository navigation.

## Technology evidence

- Python, NumPy and SciPy: [NOMOS pyproject](https://github.com/Zylus08/NOMOS/blob/master/pyproject.toml).
- C++ and CMake: AXIOM/PRAXIS source and build instructions; PyTorch/native autograd: FORGE and Aerospace RUL.
- Rust, Go and Docker: Thermodynamic deployment documentation; [Go manifest](https://github.com/Zylus08/Thermodynamic-Evolution-UCS503/blob/main/api/go.mod).
- pandas, scikit-learn, Jupyter: [RiskLab dependencies](https://github.com/Zylus08/RiskLab/blob/main/requirements.txt).
- React, TypeScript: [portfolio package](https://github.com/Zylus08/SakshamKumarMishra-Portfolio/blob/main/package.json).
- JavaScript/Vite: [analysis portal package](https://github.com/Zylus08/Thermodynamic-Evolution-UCS503/blob/main/admin-portal/package.json).
- Git and GitHub Actions: public version-controlled repositories and this profile's existing workflow.
- Reinforcement learning: DeepHedge-RL; time-series modelling: Regime Shift. No numerical proficiency is implied.

## Identity and licensing

The portfolio explicitly describes B.E. computer engineering study at TIET. Contact destinations were read from its public HTML, not guessed. Devicon originals are MIT licensed; full license and exact source hashes are bundled in `assets/technology/icons/`. Logos are third-party trademarks; no affiliation is implied. No reference-profile artwork, fonts or prose was copied. Original diagrams are generated from local code. Runtime code has no third-party Python dependencies; local preview uses the environment's Python-Markdown and PyYAML. Browser QA uses the connected Playwright browser.
