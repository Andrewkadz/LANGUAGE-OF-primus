# Time Crystals — Multi‑Scale Tau Crystal Simulator

Simulate a multi‑scale ensemble of synthetic “tau crystals” that generate a harmonic time field and a corresponding temporal anchor for AI‑style decision context. Includes a terminal‑friendly CLI with optional UDP telemetry and a matplotlib visualization demo.

## Quick Start

- Prerequisites: Python 3.9+ (tested on 3.11), pip
- Install core dependency:
  - `pip install numpy`
- Optional:
  - Visualization: `pip install matplotlib`
  - PDF tools (for `tools/pdf_tools.py`): `pip install pypdf` or `pip install PyPDF2` or `pip install pdfminer.six`

### Run the CLI (finite)

```
python time_crystal_cli.py --steps 300 --terminal-plot --encoded --ascii
```

### Run the CLI (infinite) with UDP telemetry

```
python time_crystal_cli.py --infinite --terminal-plot --encoded --udp 127.0.0.1:9999
```

UDP payload example (JSON per step):
```
{"t": 1726420377.123, "step": 42, "anchor": "SYNC", "harmonic": 0.208}
```

### Visualization demo (finite)

```
python multi_scale_tau_crystal.py
```

This generates a multi‑panel plot comparing per‑scale fields and the combined harmonic field, and shows derived anchor states. The script currently saves the image to `harmonic_time_fields.png` (see “Known Issues” for an absolute path note).

## Features

- Multi‑scale oscillator ensemble: `micro`, `meso`, `macro`, `ultra`
- Combined harmonic time field with tunable weights
- Temporal anchor mapping: `FLOW+`, `FLOW-`, `SYNC`, `INIT`
- Terminal sparkline plot with ASCII fallback for Windows consoles
- Optional UDP telemetry emitter for live integration
- Matplotlib visualization of per‑scale and combined dynamics

## Repository Layout

- `time_crystal_cli.py` — CLI runner with terminal plot and UDP publish
- `multi_scale_tau_crystal.py` — Core model, demo runner, visualization
- `synthetic_tau_crystal.py` — Minimal single‑crystal prototype
- `protoype.t.crystal` — Older prototype (duplicate of the minimal version)
- `tools/pdf_tools.py` — Lightweight PDF metadata/text extractor with pluggable backends
- `harmonic_time_fields.png` — An example generated plot (if previously run)

## CLI Arguments

- `--steps <int>`: Number of steps in finite mode (default 300)
- `--infinite`: Run until Ctrl+C
- `--encoded`: Print pattern with spaces (`+ + 0 0 - -`)
- `--terminal-plot`: Render sparkline plot in the console
- `--ascii`: Force ASCII characters for the plot (Windows‑safe)
- `--udp host:port`: Emit JSON state over UDP (e.g., `127.0.0.1:9999`)

## Environment Variables (demo script)

Used by `multi_scale_tau_crystal.py`:

- `TAU_INFINITE=1` — Run the demo loop indefinitely
- `TAU_STEPS=<int>` — Steps for finite demo (default 100)
- `TAU_STOP_PROB=<float>` — Ultra‑low termination probability per step (default `1e-15`)
- `TAU_SKIP_VIS=1` — Skip matplotlib visualization (useful on headless runs)
- `TAU_ASCII=1` — Force ASCII sparkline in demo output

## Known Issues and Notes

- Absolute path in visualization save: `multi_scale_tau_crystal.py` currently saves the plot using a hard‑coded absolute path. This should be changed to a relative path (e.g., `os.path.join(os.getcwd(), 'harmonic_time_fields.png')`).
- CLI docstring mentions `--skip-vis` but the parser doesn’t define it. Either remove the mention or add the flag.
- Unbounded history: `TemporalAnchorModule.harmonic_field` grows indefinitely in long/infinite runs; converting to a bounded `deque(maxlen=...)` is recommended.
- No `requirements.txt` or tests yet; see ROADMAP for planned improvements.

## Development Tips

- The model uses numpy and simple trigonometric updates; dynamics and weights are easy to tweak in `multi_scale_tau_crystal.py`.
- UDP payloads are tiny JSON blobs; a simple Python or Node consumer can visualize or log them in real time.
- `tools/pdf_tools.py` tries `pypdf`, falls back to `PyPDF2`, then `pdfminer.six`. It’s optional and independent from the simulator.

## Roadmap

See `ROADMAP.md` for proposed next steps and future pathways.

