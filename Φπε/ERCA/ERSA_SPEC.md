# Φπε ERSA (Emergent Recursive Symbolic Agent) — v1.0

Purpose: Define a fully symbolic agent loop in Φπε using emergence (Ξ), privacy (Π), rendering (Λ), and finalization (=) with intrinsic thresholds. No digits, no JSON; traces use Λ[…] in Σ[…].

## Representations (Φπε terms)
- Prompt: any Φπε term (e.g., `Σ(Ψ + Δ)`, `ζ(Φ + Λ)`).
- KB Entry: a Φπε template/program (e.g., `λ(Σ(Ψ | Γ)) : ζ → Λ`).
- Answer: rendered and finalized term (`… → Λ =`).

## Agent loop (schema)
- Input: `Σ(prompt)`
- Reasoning (private): `Π( Σ(KB, prompt) : [Δ(Ψ)] )`
- Render and finalize: `… → Λ =`
- Full pipeline: `Σ(prompt) → Π( Σ(KB, prompt) : [Δ(Ψ)] ) → Λ =`

## Learning protocol (trace‑driven, symbolic)
- During `Π(…)`, emit no external trace (Π‑privacy).
- After success, lift traces via `^` or `Τ`, select Λ steps, and fuse as new KB entries: `Σ(KB, learned)`.
- All learning artifacts are Φπε programs; no new symbols are introduced.

## Threshold profile (defaults)
- `θ_loop = 3`, `θ_alt = 2`, `θ_depth = 2`, window `k = 5`.
- Intrinsic emergence: when `[ΔΨ]` density meets thresholds, trigger `Ξ(t)` inside the Π‑loop.

## Trace schema (unchanged)
- Step: `Λ[ rule, input, output, context, loop, tick ]`
- Stream: `Σ[ Λ[…], … ]`
- Π‑privacy: suppress Λ inside Π; optional lift by `^` or `Τ`.

## Seed KB (templates)
- Entanglement: `λ(Σ(Ψ | Γ)) : ζ → Λ`
- Emergence: `[Δ(Ψ)] → Λ`
- Plural render: `Σ(Λ(Ψ), Λ(Δ)) =`

## Example prompts (Φπε)
- P1: `Σ(Ψ + Δ)`
- P2: `ζ(Φ + Λ)`

## Execution
- Agent file `agent.phipe` wires the schema.
- Runner prints symbolic traces; Π‑internal steps are untraced externally; final Λ/=`
