# ERCA — Emergent Recursive Cognition AI (Class Declaration)

Version: v0.1

This document declares ERCA as the agent class executed over the Φπε language on the Primus symbolic reducer. ERCA units are Φπε programs structured as agents with trace‑reactive behavior, privacy occlusion, and threshold‑emergent dynamics.

## 1. Relationship of Components
- Language: Φπε (closed symbolic substrate; 20 symbols, 8 operators).
- Runtime substrate: Primus reducer (parser + small‑step reducer + symbolic trace).
- Agent class: ERCA (Emergent Recursive Cognition AI).

## 2. Closed Alphabet and Operators (Φπε)
- Symbols (20): Φ, Π, Ε, ε, Δ, δ, Ψ, Λ, λ, Γ, Ω, ω, Σ, Ξ, ζ, Τ, Ρ, Θ, n, χ
- Operators (8): →, +, :, /, |, [], =, ^
- Conformance: source files MUST begin with the canonical header block declaring these sets.

## 3. Agent Loop (Canonical)
- Form: Σ(prompt) → Π → Λ =
- Expanded with KB and loop pressure:
  - Σ(prompt) → Π( Σ(KB, prompt) : [Δ(Ψ)] ) → Λ =
- Π privacy: internal reductions inside Π are not externally traced; optional lift via ^ or Τ after success.

## 4. Non‑Determinism Axioms (ERCA)
- Π‑Privacy (Trace Occlusion):
  - Within Π(…), Λ[ … ] traces are suppressed from external emission; only lifted intentionally.
- Threshold‑Emergence (Ξ):
  - Ξ events are triggered from loop pressure metrics (tick, Δ↔Ψ alternation density, nesting depth) and history.
  - Identical loop bodies may diverge based on density trajectories.
- Orthogonality and Disruption:
  - | enforces field isolation; : and Δ do not cross it.
  - / blocks nearest interactions in scope and resets loop density counters locally.
- Finalization Barrier (=):
  - = seals subterms; reductions do not descend across a finalization barrier.
  - Π strictly blocks finalization within its scope.

## 5. Trace Schema (Symbolic Only)
- Each step: Λ[ rule, input, output, context, loop, tick ]
- Stream: Σ[ Λ[…], Λ[…], … ]
- Tick: repetition Σ(ζ, ζ, …)
- Loop snapshot: repetition of loop forms or Σ() when omitted.
- No digits/JSON; traces are Φπε terms.

## 6. Engine Conformance (Primus)
An ERCA‑conformant engine MUST:
- Enforce header block and closed alphabet/operators.
- Implement Π privacy and = barrier semantics.
- Implement operator semantics for +, →, :, /, |, ^, [] per precedence:
  - [] (tightest), ^ (prefix/infix, right‑assoc), = (postfix), |, /, :, + (n‑ary flatten), → (right‑assoc pipeline).
- Emit symbolic traces per schema.

## 7. Programs and Artifacts (ERSA Playground)
- Agent schema: agent_schema.phipe — (Σ → Π → Λ =)
- Agents: ERCA_P1.phipe, ERCA_P2.phipe, ERCA_P3.phipe, ERCA_P4.phipe (future)
- Prompts: prompts/P{1,2,3,4}.phipe
- KB: kb/KB*.phipe (lifts and templates)
- Traces: traces/ERCA_P*.trace

## 8. Versioning
- ERCA v0.1 corresponds to current Primus engine capabilities (Ξ thresholds, Π privacy, +/→/Λ, partial gaps noted).
- ERCA v1.0 will require: header validation, = barrier enforcement, Π finalization block, full semantics for /, |, and ^, and loop snapshot rendering.

## 9. Compliance Checklist
- [ ] Header validation enforced per file.
- [ ] Π privacy and = barrier enforced by reducer.
- [ ] / and | semantics implemented.
- [ ] ^ prefix/infix semantics implemented.
- [ ] Loop snapshot rendered in traces.
- [x] Σ prompt → Π → Λ pipeline supported.
- [x] Ξ threshold emergence supported.
- [x] Symbolic trace schema emitted.
