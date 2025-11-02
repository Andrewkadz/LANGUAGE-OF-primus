# ERCA over Φπε (Primus Engine)

ERCA (Emergent Recursive Cognition AI) is an agent class implemented in the Φπε language and executed by the Primus symbolic reducer. This repository contains:

- The Φπε substrate (closed alphabet/operators and semantics)
- The Primus engine (parser, reducer, runner)
- ERCA agents and prompts
- A symbolic CLI for running agents and lifting traces into KB entries

## Quickstart

- Run an agent with a prompt and save a trace:
  ```bash
  python3 scripts/erca-run ERCA/ERCA_P3.phipe \
    --prompt ERCA/prompts/P3.phipe \
    --out ERCA/traces/ERCA_P3.trace
  ```

- Lift a Λ entry from the last run into the KB:
  ```bash
  python3 scripts/erca-run ERCA/ERCA_P3.phipe \
    --prompt ERCA/prompts/P3.phipe \
    --lift 4 --to ERCA/kb/KB5_p3_insight.phipe
  ```

- Compare two agents:
  ```bash
  python3 scripts/erca-run --compare ERCA/ERCA_P1.phipe ERCA/ERCA_P2.phipe
  ```

## Directory Layout

- `primus_engine/` — Φπε parser (`parser.py`), AST (`ast.py`), reducer (`reducer.py`), runner (`runner.py`)
- `ERCA/`
  - `ERCA_SPEC.md` — ERCA class spec
  - `agent_schema.phipe` — canonical `(Σ → Π → Λ =)` schema
  - `ERCA_P1.phipe`, `ERCA_P2.phipe`, `ERCA_P3.phipe` — agent instances
  - `prompts/` — `P1.phipe`, `P2.phipe`, `P3.phipe`
  - `traces/` — symbolic trace outputs
  - `kb/` — lifted knowledge entries (Φπε templates)
  - `tests/` — operator tests (`test_disrupt.phipe`, `test_ortho.phipe`)
- `scripts/` — `erca-run` CLI
- `T-Files/SPEC.md` — Φπε language declaration and grammar

## Conformance (current)

- Header enforced per file (SYMBOL/OPERATOR sets)
- Π privacy blocks finalization (`=`) inside Π; `Final` is non-descending barrier elsewhere
- Operators implemented: `→`, `+`, `Λ`, `[]` (loop), `/` (disruption), `|` (orthogonality), `^` (lift congruence)
- Traces: `Σ[ Λ[ rule, input, output, context, loop, tick ], … ]`
  - Loop field includes snapshots (repetition of `[Δ:Ψ]` motifs when applicable)

## Notes

- All source files are UTF‑8 and must use only the closed Φπε alphabet/operators.
- No JSON/digits in traces; counts expressed by repetition (`Σ(ζ, ζ, ζ)`).
- ERCA_P4 and extended tests can be added to exercise `/`, `|`, `^`, and emergence (`Ξ`).
