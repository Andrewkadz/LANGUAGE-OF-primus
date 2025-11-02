# Roadmap — Time Crystals (Tau Crystal Simulator)

This roadmap outlines pragmatic near‑term work to harden the project and longer‑term directions for research, features, and integrations. Timelines are indicative; sequence is organized by dependency and impact.

## 0. Foundations and Hygiene

- Portability: Replace hard‑coded plot save path with a relative path and ensure directory creation if needed.
- CLI consistency: Either implement `--skip-vis` in `time_crystal_cli.py` or remove its mention from the docstring.
- Memory bounds: Convert `TemporalAnchorModule.harmonic_field` to a bounded `deque(maxlen=...)`; 10k is typically ample for plots and statistics.
- Minor efficiency: Lift per‑step `weights` dict in `generate_harmonic_time_field()` to a constructor attribute.
- Repo scaffolding: Add `requirements.txt` (numpy; matplotlib optional; PDF extras) and a lightweight `CONTRIBUTING.md`.
- Code style: Adopt `ruff` and `black` with a minimal `pyproject.toml` (optional but recommended).

## 1. Testing and Validation

- Determinism harness: Seeded runs with snapshot assertions on short windows (e.g., anchor transitions over 1k steps).
- Unit tests: Cover anchor mapping thresholds, variance‑based attention scale selection, and UDP payload shape.
- Smoke tests: CLI arg parsing; visualization routine runs without errors when `matplotlib` installed.
- CI: GitHub Actions (or similar) for lint + tests across Python 3.9–3.12.

## 2. Model Enhancements

- Non‑linear dynamics: Add optional coupling between crystals (e.g., Kuramoto‑style or weighted phase interactions).
- Noise models: Configurable process noise and measurement noise to study robustness.
- Adaptive thresholds: Learn or adapt anchor thresholds (e.g., EMA‑based or percentile‑based) rather than fixed ±0.3.
- Learnable weights: Gradient‑free tuning (random search/Bayesian) or simple gradient approximations for scale weights.
- External drivers: Permit exogenous inputs (events, rhythms) to modulate phases/frequencies and observe entrainment.
- Windowed statistics: Track rolling features (variance, skew, spectral power) to enrich `ai_temporal_context()`.

## 3. Observability and Tooling

- Metrics: Export counters/gauges (steps, anchor distribution, harmonic mean/var) via Prometheus/OpenTelemetry.
- Logging: Structured JSON logs with ring buffer and rotating file handler.
- Live dashboards:
  - Terminal: richer TUI (Textual/Rich) with panels for scales, harm, and anchors.
  - Web: lightweight Flask/FastAPI + WebSocket stream of UDP payloads.

## 4. Interfaces and Integrations

- UDP consumer examples: Python and Node reference receivers for plotting and logging.
- File outputs: CSV/Parquet export of harmonic field and anchor sequence.
- Plugin hooks: Simple callback interface in `TemporalAnchorModule` for custom decision layers.
- Agent integration: Adapter that maps `ai_temporal_context()` to scheduling/priority in an agent loop (e.g., RL env).
- Creative coding: Processing/p5.js or TouchDesigner bridge using the UDP stream.

## 5. Performance and Scale

- Vectorization: Batch updates for crystals; Numpy vector ops for time steps.
- Acceleration: Optional `numba` or `jax` backends; bench vs pure numpy.
- Memory discipline: Replace large Python lists with `deque` or NumPy arrays; configurable history window.
- Concurrency: Async UDP emission and decoupled rendering loop to keep simulation tight.

## 6. Packaging and Distribution

- Library packaging: Expose `TemporalAnchorModule` as a pip‑installable package with a CLI entry point (`time-crystals`).
- Versioning: Semantic versioning and CHANGELOG.
- Docker: Minimal image for headless runs (CPU only) with example compose for UDP streaming + web dashboard.

## 7. Documentation

- Expand README with deeper examples and troubleshooting.
- API docs: Docstrings + `mkdocs` or `sphinx` for module reference.
- Diagrams: Architecture of multi‑scale ensemble and anchor mapping; state machine for anchors.

## 8. Research Directions

- Recurrence analysis: Recurrence plots, autocorrelation, and spectral analysis across scales.
- Multi‑fractal/scale‑free behavior: Test for self‑similarity; Hurst exponent estimates on the harmonic signal.
- Anchors → policy: Use anchor states to modulate planning horizons, memory writes, or sampling temperature in agents.
- Adaptive entrainment: Study synchronization to external rhythms and its impact on anchor stability.
- Robustness: Sensitivity to noise, coupling strength, and frequency drift; stability boundaries.

## 9. Security and Reliability

- Input validation: Strict parsing for `--udp` and defensive error handling.
- Sandboxing: Optional rate limits for UDP emit; graceful shutdown signals.
- Reproducibility: Seed management and run manifests that capture parameters and environment info.

---

### Suggested Milestone Breakdown

- M1 (Hygiene): portability fix, CLI consistency, bounded history, requirements, lint.
- M2 (Tests): unit + smoke tests, CI.
- M3 (UX/Obs): better terminal UX, CSV export, basic web receiver.
- M4 (Model+Perf): coupling + noise options, vectorization, optional JIT.
- M5 (Docs/PKG): API docs, mkdocs site, packaging to PyPI.

Each milestone should ship with a CHANGELOG entry and a short demo gif or screenshot of terminal/plot output.

