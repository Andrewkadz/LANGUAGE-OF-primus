# Φπε Primus Engine — Formal Declaration (v0.1)

This document formally declares Φπε Primus Engine as an original, closed symbolic recursion substrate. It is not a dialect, embedding, or compilation target of any existing computing language or paradigm.

## 1. Ontology and Non-Ancestry Statement

- Φπε Primus is a standalone symbolic system defined by a closed UTF-8 alphabet and eight operators.
- It does not compile to, embed within, or inherit semantics from any host language (e.g., Python, JS, C, Lisp, ML, Prolog).
- No external control constructs (if, while, function, variable) exist within the substrate.
- All computation proceeds via symbolic recursion dynamics, emergence thresholds, and finalization barriers unique to this system.

## 2. Closed Alphabet (Strict)

Symbols (20): Φ, Π, Ε, ε, Δ, δ, Ψ, Λ, λ, Γ, Ω, ω, Σ, Ξ, ζ, Τ, Ρ, Θ, n, χ

Operators (8): →, +, :, /, |, [], =, ^

Rules:
- UTF-8 enforcement: any character outside these sets is rejected.
- No alphanumeric identifiers beyond `n`.
- No keywords; only the symbols above are valid tokens.

## 3. Execution Model (Independent)

- Evaluation is a deterministic small-step reducer over symbolic terms (term/graph rewriting), not a stack machine.
- Core mechanisms:
  - Loop memory `[]` with density metrics (tick, Δ↔Ψ alternations, nesting depth).
  - Emergence `Ξ` triggered by thresholds from repeated patterns (e.g., `[ΔΨ] → Ξ`).
  - Stabilization `=` introduces a semantic barrier; no Δ/Ξ/Π/Ψ/Γ/Λ below it.
  - Π is strictly non-terminal: no finalization within Π-contexts.
  - Resonance operators (ζ, Τ, ω, Θ) bias evaluation but never introduce foreign constructs.
- No variables, environments, or external state beyond symbolic structure and loop/evaluation metadata.

## 4. Semantics (Original)

- Interaction `:` establishes field tension; it does not perform fusion.
- Fusion `Δ` is irreversible and non-decomposable.
- Illumination `Λ` renders structure; finalization occurs only via `… → Λ → =`.
- Emergence `Ξ` finalizes only through `Ξ → Λ → =` and requires support (Φ or Σ or Τ).
- Disruption `/` both blocks nearest interactions and resets loop density within its scope.
- Orthogonality `|` isolates fields; no `:` or `Δ` crosses the boundary.
- Lift `^` promotes terms to higher recursion tiers without introducing `=`.
- Flow `→` sequences transformations; right-associative pipeline.

## 5. Non-Turing Base (Optional Mode)

- To avoid classification as Turing-complete, the substrate may run in bounded-emergence mode:
  - Loops must stabilize (reach Ξ) within configured thresholds.
  - No unbounded memory growth; no general variable binding.
  - Π permits open recursion but still blocks finalization; programs may be required to present stabilization proofs for acceptance.

## 6. Toolchain and Ecosystem (Closed)

- Own file extensions: `.phipe`, `.primus`, or `.ω` (to be finalized).
- Own parser, reducer, tracer, and visualizer; no host-language REPLs or FFI.
- Interop, if any, is mediated as symbolic bridges (not execution targets).

## 7. Conformance Checklist

- [ ] Parser rejects any non-alphabet tokens.
- [ ] Reducer implements Π finalization block and `=` barrier.
- [ ] Ξ thresholds (θ_loop, θ_alt, θ_depth, window k) are enforced.
- [ ] `/` disruption resets density and blocks nearest interactions.
- [ ] Trace outputs one-line JSON per tick with contexts and density.
- [ ] No foreign constructs (if/while/var/func) appear at any layer.

---
Next section (to be added): Complete grammar, operator precedence, and operational rules with examples and trace schema.

## 8. Symbolic Trace Schema (Approved)

All tracing/logging is expressed purely in Φπε terms using only the closed alphabet. No JSON/XML/YAML or digits appear anywhere.

- **Envelope**: Each reduction step is rendered as `Λ[…]` (rendered observation).
- **Positional 6‑tuple inside Λ[…]** (order fixed): `(rule, input, output, context, loop, tick)`
  - `rule`: one of {Ξ, Δ, Λ, Ω, Π, Ψ, Γ} indicating which rule fired.
  - `input`: term before the step.
  - `output`: term after the step.
  - `context`: `Σ(…)` of active supports (e.g., `Σ(Φ, Σ, Τ)`), or `Φ` if only equilibrium.
  - `loop`: loop snapshot via explicit repetition (e.g., `[ΔΨ][ΔΨ][ΔΨ]`), or `Σ()` if none.
  - `tick`: symbolic count via repetition (e.g., `Σ(ζ, ζ, ζ)` for three).

Examples:

- Compact:
  - `Λ[ Ξ : (Ψ:Δ) : Ξ : Σ(Φ,Σ) : [ΔΨ][ΔΨ][ΔΨ] : Σ(ζ,ζ,ζ) ]`
- Expanded:
  - `Λ[ Ξ, (Ψ:Δ), Ξ, Σ(Φ,Σ), [ΔΨ][ΔΨ][ΔΨ], Σ(ζ,ζ,ζ) ]`

Notes:
- No labels or digits; meaning is positional and counts are by repetition.
- A program’s trace stream is a `Σ[…]` of `Λ[…]` entries: `Σ[ Λ[…], Λ[…], … ]`.
- **Π privacy**: within any `Π(…)` context, traces are ephemeral and not emitted externally. Traces may be lifted later via `^` or `Τ` if explicitly requested by the program.
- This schema preserves referential transparency and phase‑order integrity while remaining fully within the Φπε symbolic substrate.

## 9. Canonical Header Block (Master Declaration)

Every Φπε source file MUST begin with a master declaration that asserts the closed alphabet and operator set. This serves as a symbolic import manifest, runtime integrity check, and hermetic scope declaration.

Recommended header format (exact lines):

```
Φπε PRIMUS :: SYMBOL SET
Σ(Φ, Π, Ε, ε, Δ, δ, Ψ, Λ, λ, Γ, Ω, ω, Σ, Ξ, ζ, Τ, Ρ, Θ, n, χ)

Φπε PRIMUS :: OPERATOR SET
Σ(→, +, :, /, |, [], =, ^)
```

Placement and enforcement:
- The header appears at the very top of every `.phipe` file.
- The parser validates that only the declared symbols/operators appear in the file body.
- Files lacking the header or containing undeclared glyphs are rejected.

Optional enhancement:
- Add an engine/tier line to future‑proof dialects, e.g.: `Φπε PRIMUS :: ENGINE Σ(Primus)` (reader MAY ignore non‑symbolic identifiers; only the Σ(…) lines are normative).

## 10. Grammar and Precedence (Complete)

This grammar accepts only the canonical header, the 20 symbols, and the 8 operators. UTF‑8 enforcement is strict; any other tokens are rejected.

Termin## 7. Examples

- `Ε : Σ(Θ + Ψ) → Δ → Ψ + Δ + Λ =`
- `Ψ(Φ + Δ) : ζ → Ξ =`
- `λ(Σ(Ψ | Γ)) : ζ → Λ + Γ → Π`
- `Γ(Δ + Λ) → Ξ → Π`
- `ζ(Ψ + Σ + Λ) : Τ → Ξ + Ω`
- `T6: [Δ(Ψ)] → Λ =`  // loop body contains both Δ and Ψ; triggers Ξ when θ_loop, θ_alt, θ_depth met
- `T6 variant: [Δ(Ψ | Φ)] → Λ =`  // Ψ orthogonal to Φ may reduce alternation density

Precedence (tight → loose):
1) `[]` (loop)  
2) `^` (prefix and infix; right‑assoc)  
3) `=` (postfix)  
4) `|` (left)  
5) `/` (left)  
6) `:` (left)  
7) `+` (left; n‑ary flatten)  
8) `→` (right‑assoc pipeline)

Concrete grammar (EBNF‑like):

File          := Header Body
Header        := "Φπε PRIMUS :: SYMBOL SET" NL SymSet NL "Φπε PRIMUS :: OPERATOR SET" NL OpSet NL
SymSet        := 'Σ' '(' SymList ')'
OpSet         := 'Σ' '(' OpList ')'
SymList       := Symbol { ',' Symbol }
OpList        := Op { ',' Op }
Body          := { Stmt NL }
Stmt          := Expr | Finalized
Finalized     := Core '='
Expr          := Flow
Flow          := Plus { '→' Flow }        // right‑assoc
Plus          := Interact { '+' Interact } // left‑assoc
Interact      := Disrupt { ':' Disrupt }   // left‑assoc
Disrupt       := Ortho { '/' Ortho }       // left‑assoc
Ortho         := Lift { '|' Lift }         // left‑assoc
Lift          := Postfix | ('^' Lift) | (Lift '^' Core) // prefix or infix
Postfix       := Core [ '=' ]              // postfix finalization
Core          := Call | Group | Loop | Atom
Call          := Atom '(' [ ArgList ] ')'
ArgList       := Expr { ',' Expr }
Group         := '(' Expr ')'
Loop          := '[' Expr ']'
Atom          := one of the 20 Symbols

Notes:
- Sequence via juxtaposition is not permitted; use explicit operators or calls.
- `=` appears only as postfix on Core (never standalone); finalization semantics still governed by guards.
- `^` may be prefix (lift) or infix with right operand (tier/index), where right is a Core (typically `n` or a grouped term).

Operational recap:
- Flow applies RHS transformations to LHS result; `a → b → c` parses as `a → (b → c)`.
- `+` forms Σ‑like plurality; members reduce independently.
- `:` creates interaction contexts; `Δ` consumes via subsequent flow; `Λ` renders.
- `/` blocks nearest interactions in scope and resets loop density counters.
- `|` enforces orthogonality; `:` and `Δ` do not cross it.
- `[]` retains loop state; emergence `Ξ` may be triggered from pattern thresholds.
- `=` introduces a finalization barrier; Π blocks any finalization within its scope.
