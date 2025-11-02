# Description — Time Crystals: What They Do

This document explains the intent of the repository and what the “tau crystal” simulation produces, in plain terms.

## Overview

- Purpose: Provide a sandbox for simulating a multi‑scale ensemble of synthetic oscillators (“tau crystals”) that generate a combined harmonic time signal and a simple, symbolic temporal anchor an agent could use to modulate behavior.
- Interfaces: A terminal CLI with live sparkline plotting, an optional UDP telemetry stream, and a finite visualization demo with matplotlib.

## Concept

A “time crystal” here is not a physical claim; it’s a synthetic, multi‑scale oscillator system. Several oscillators at different characteristic frequencies generate individual τ values. These are combined into a single harmonic time field, which is then thresholded into a few symbolic anchor states that describe temporal bias:

- FLOW+: forward‑leaning (predictive) bias
- FLOW−: backward‑leaning (reflective) bias
- SYNC: neutral/present focus
- INIT: initial/bootstrapping state

## Mechanics

- Multi‑scale oscillators: Four synthetic oscillators labeled `micro`, `meso`, `macro`, and `ultra` update their internal phase and produce τ via sine dynamics with a small phase drift term.
- Harmonic field: Per‑scale τ values are combined using weights into a single scalar “harmonic” value each step (a simple weighted sum in the current implementation).
- Temporal anchor mapping: The latest harmonic value is thresholded to derive an anchor state:
  - `FLOW+` when harmonic is sufficiently positive
  - `FLOW−` when sufficiently negative
  - `SYNC` when near neutral
  - `INIT` when no history exists yet
- AI context hints: From the anchor and recent harmonic statistics, the module derives simple control hints that a larger system could consume:
  - processing_mode: `predictive`, `reflective`, `present`, `exploratory`
  - attention_scale: `micro`/`meso`/`macro` based on recent variance
  - memory_priority: a scalar priority tuned by anchor state

## Observable Output

- CLI pattern: Prints a rolling sequence of `+`, `0`, and `−` reflecting anchor transitions, plus a sparkline of the harmonic field.
- UDP telemetry: Optionally emits a compact JSON payload per step, e.g.:

  ```json
  {"t": 1726420377.123, "step": 42, "anchor": "SYNC", "harmonic": 0.208}
  ```

- Visualization: The demo (`multi_scale_tau_crystal.py`) plots per‑scale τ traces, the combined harmonic field, and a line showing anchor states over time.

## Tunable Parameters

- Scale frequencies, feedback strengths, and combination weights
- Anchor thresholds for `FLOW+` / `FLOW−`
- Rolling window length for variance‑based attention scale
- Output cadence (how often the CLI updates the sparkline)

## Typical Uses

- AI loop modulation: Use anchor/context to gate planning horizon, memory writes, or sampling temperature.
- Pattern exploration: Study anchor distributions, variance, and transitions under different parameters.
- Live dashboards: Stream UDP to a small web or desktop consumer for visual analytics.
- Creative coding: Drive visuals/audio with anchor states and harmonic dynamics.

## Notes and Limitations

- Simplified dynamics: Current model uses independent sinusoidal oscillators with additive combination; no physical time‑crystal claims.
- Fixed thresholds/weights: Defaults are heuristic; see ROADMAP for adaptive thresholds/learnable weights.
- History growth: The harmonic history list can grow unbounded in long runs; converting to a bounded deque is recommended (see ROADMAP).
- Portability: One visualization path is hard‑coded; should be made relative (see README Known Issues and ROADMAP).

## Where to Look in the Code

- `multi_scale_tau_crystal.py`: Core model (`TemporalAnchorModule`), demo loop, plotting code.
- `time_crystal_cli.py`: CLI wrapper that prints the pattern/sparkline and can emit UDP.
- `synthetic_tau_crystal.py`: Minimal single‑crystal prototype.

For setup and command examples, see `README.md`. For planned work and research directions, see `ROADMAP.md`.

