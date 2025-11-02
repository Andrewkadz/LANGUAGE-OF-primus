from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List
import re

# Canonical header blocks for Φπε files
HEADER = (
    "Φπε PRIMUS :: SYMBOL SET\n"
    "Σ(Φ, Π, Ε, ε, Δ, δ, Ψ, Λ, λ, Γ, Ω, ω, Σ, Ξ, ζ, Τ, Ρ, Θ, n, χ)\n"
    "Φπε PRIMUS :: OPERATOR SET\n"
    "Σ(→, +, :, /, |, [], =, ^)\n\n"
)

# Simple lexicon (rule-based)
LEX = {
    # core concepts
    "change": "Δ",
    "fusion": "Δ",
    "emerge": "Ξ",
    "emergence": "Ξ",
    "reason": "Ψ",
    "mind": "Ψ",
    "render": "Λ",
    "illuminate": "Λ",
    "private": "Π",
    "inside": "Π",
    "plural": "Σ",
    "many": "Σ",
    # operators (phrases)
    "pipeline": "→",
    "then": "→",
    "plus": "+",
    "and": "+",
    "interact": ":",
    "interaction": ":",
    "isolate": "|",
    "isolation": "|",
    "disrupt": "/",
    "disruption": "/",
    "lift": "^",
}

@dataclass
class MapResult:
    phi_body: str
    notes: List[str]


def _swap_delta_psi(expr: str) -> str:
    # Swap Δ and Ψ safely by temporary placeholders
    return expr.replace('Δ', '\u0001').replace('Ψ', 'Δ').replace('\u0001', 'Ψ')


def _wrap_isolate(expr: str) -> str:
    return f"({expr}) | ({expr})"


def _wrap_disrupt(expr: str) -> str:
    return f"{expr} / [{expr}]"


def english_to_phipe(text: str, prev_phi: str | None = None) -> str:
    """
    Map a short English request to a Φπε prompt body (no header).
    Heuristics (very small):
    - "test X ... with Y" -> Σ(X + Y)
    - Contains 'render' -> append → Λ
    - Contains 'inside'/'private' -> wrap in Π(...)
    - Otherwise map keywords and default to Σ(Δ + Ψ) if unknown
    """
    t = text.strip().lower()
    notes: List[str] = []

    # Detect key tokens
    def has(word: str) -> bool:
        return word in t

    symbols: List[str] = []
    # crude noun extraction by lexicon lookup
    for w, sym in LEX.items():
        if w in t and sym in {"Δ", "Ψ", "Λ", "Ξ", "Π", "Σ"}:
            symbols.append(sym)

    # Conversational references using previous expression
    if prev_phi:
        if any(w in t for w in ["again", "same", "as before", "repeat"]):
            expr = prev_phi
            # apply optional modifiers
            if any(w in t for w in ["reverse", "swap"]):
                expr = _swap_delta_psi(expr)
            if any(w in t for w in ["isolate", "isolation"]):
                expr = _wrap_isolate(expr)
            if any(w in t for w in ["disrupt", "disruption"]):
                expr = _wrap_disrupt(expr)
            if any(w in t for w in ["render", "illuminate"]):
                expr = f"{expr} → Λ"
            if any(w in t for w in ["private", "inside"]):
                expr = f"Π({expr})"
            return expr

    # Default pair if nothing found
    if not symbols:
        symbols = ["Δ", "Ψ"]
        notes.append("defaulted to Δ and Ψ")

    # Build core expression as Σ of plus-joined symbols
    core = ("Σ(" + " + ".join(symbols) + ")") if len(symbols) > 1 else symbols[0]

    # Optional wrappers/effects
    expr = core

    if has("interact") or has("interaction"):
        # Make a simple interaction Δ : Ψ if both present
        if "Δ" in symbols and "Ψ" in symbols:
            expr = "Δ : Ψ"
        else:
            expr = f"{core} : {core}"

    if has("isolate") or has("isolation"):
        expr = _wrap_isolate(expr)

    if has("disrupt") or has("disruption"):
        expr = _wrap_disrupt(expr)

    # Pipeline to render if asked
    if has("render") or has("illuminate"):
        expr = f"{expr} → Λ"

    # Private/inside wrapper
    if has("private") or has("inside"):
        expr = f"Π({expr})"

    return expr


def wrap_prompt_file(phi_body: str) -> str:
    """Attach canonical header to a Φπε body."""
    return HEADER + phi_body + "\n"


def phi_trace_to_english(trace_text: str, mode: str = "compact", markdown: bool = False) -> str:
    """
    Very lightweight summarizer for symbolic traces Σ[Λ[…]].
    - Extract Λ entries (best-effort via bracket scanning) and summarize rule + tick.
    - Report loop snapshot presence and count of '[Δ:Ψ]' motifs if visible.
    """
    # Count Λ entries
    lambda_entries = trace_text.count("Λ(") + trace_text.count("Λ[")

    # Extract approximate tick counts by counting 'ζ' per line (heuristic)
    tick_total = trace_text.count("ζ")

    # Loop motif count (heuristic): occurrences of "[Δ:Ψ]"
    motif_count = trace_text.count("[Δ:Ψ]")

    lines: List[str] = []
    header = "Trace summary" if not markdown else "## Trace summary"
    lines.append(header)
    lines.append(f"steps: {lambda_entries}")
    lines.append(f"tick_symbols(ζ): {tick_total}")
    if motif_count:
        lines.append(f"loop_motif_[Δ:Ψ]: {motif_count}")

    if markdown:
        return "\n\n".join(lines) + "\n"
    return "\n".join(lines) + "\n"
