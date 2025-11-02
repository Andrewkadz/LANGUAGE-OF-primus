from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
import re

# Very small PhiScript scaffold for composing Φπε fragments.
# Supported forms (line-based, order matters):
#   let NAME = EXPR            # bind a symbolic expression
#   run EXPR                   # set/return current expression
#   use last                   # reuse previous expression
#   use last → Λ               # reuse previous expression and render
#   if motif then EXPR [else EXPR]  # choose based on loop motif presence in last summary
#   Multiple commands can be chained on one line using ';'
# Names can be alphanum/_ and used inside EXPR as {name} placeholders.
# EXPR is a raw Φπε fragment like: Σ(Δ + Ψ), Π(Δ : Ψ), (Δ:Ψ) | (Δ:Ψ) / [Δ]

_BIND_RE = re.compile(r"^\s*let\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")
_RUN_RE = re.compile(r"^\s*run\s+(.+?)\s*$")
_USE_LAST_RE = re.compile(r"^\s*use\s+last\s*$")
_USE_LAST_RENDER_RE = re.compile(r"^\s*use\s+last\s*→\s*Λ\s*$")
_PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")

@dataclass
class PhiScriptState:
    bindings: Dict[str, str]
    last_expr: Optional[str]

    @classmethod
    def new(cls) -> 'PhiScriptState':
        return cls(bindings={}, last_expr=None)


def _substitute(expr: str, bindings: Dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        name = m.group(1)
        return bindings.get(name, m.group(0))
    return _PLACEHOLDER_RE.sub(repl, expr)


_IF_RE = re.compile(r"^\s*if\s+motif\s+then\s+(.+?)(?:\s+else\s+(.+))?\s*$")


def eval_line(line: str, st: PhiScriptState, last_summary: Optional[str]) -> Optional[str]:
    line = line.strip()
    if not line:
        return None

    m = _BIND_RE.match(line)
    if m:
        name, expr = m.group(1), m.group(2)
        st.bindings[name] = _substitute(expr, st.bindings)
        return None

    if _USE_LAST_RENDER_RE.match(line):
        if st.last_expr is None:
            return None
        st.last_expr = f"{st.last_expr} → Λ"
        return st.last_expr

    if _USE_LAST_RE.match(line):
        return st.last_expr

    # Conditional on motif presence in last summary
    m = _IF_RE.match(line)
    if m:
        then_expr = _substitute(m.group(1), st.bindings)
        else_expr = _substitute(m.group(2), st.bindings) if m.group(2) else None
        motif_present = bool(last_summary and "loop_motif_[Δ:Ψ]:" in last_summary and not last_summary.endswith(": 0\n"))
        chosen = then_expr if motif_present else (else_expr if else_expr is not None else st.last_expr)
        st.last_expr = chosen
        return st.last_expr

    m = _RUN_RE.match(line)
    if m:
        expr = _substitute(m.group(1), st.bindings)
        st.last_expr = expr
        return st.last_expr

    # Otherwise treat as a raw expression: set as last
    st.last_expr = _substitute(line, st.bindings)
    return st.last_expr


def eval_script(script: str, prev_expr: Optional[str] = None, last_summary: Optional[str] = None) -> str:
    """Evaluate a PhiScript; return the final Φπε expression (no header). Supports ';' chaining and simple conditional."""
    st = PhiScriptState.new()
    st.last_expr = prev_expr
    last: Optional[str] = prev_expr
    # Split by lines and ';' within lines for chaining
    raw_lines = []
    for line in script.splitlines():
        parts = [p for p in line.split(';') if p.strip()]
        raw_lines.extend(parts)
    for line in raw_lines:
        out = eval_line(line, st, last_summary)
        if out is not None:
            last = out
    return last or (prev_expr or "Σ(Δ + Ψ)")
