from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List, Union, Optional

# Closed symbol set (20) and operators (8)
SYMBOLS = {"Φ","Π","Ε","ε","Δ","δ","Ψ","Λ","λ","Γ","Ω","ω","Σ","Ξ","ζ","Τ","Ρ","Θ","n","χ"}
OPERATORS = {"→","+",":","/","|","[]","=","^"}

@dataclass(frozen=True)
class Atom:
    sym: str  # one of SYMBOLS

@dataclass(frozen=True)
class Call:
    head: Atom
    args: Tuple['Term', ...]

@dataclass(frozen=True)
class Infix:
    op: str  # → + : / | ^
    left: 'Term'
    right: 'Term'

@dataclass(frozen=True)
class Loop:
    body: 'Term'
    uid: int

@dataclass(frozen=True)
class Final:
    term: 'Term'

Term = Union[Atom, Call, Infix, Loop, Final]

# Pretty printer (symbolic only)

def pretty(t: Term) -> str:
    if isinstance(t, Atom):
        return t.sym
    if isinstance(t, Call):
        return f"{t.head.sym}(" + ", ".join(pretty(a) for a in t.args) + ")"
    if isinstance(t, Infix):
        if t.op == "^" and isinstance(t.left, Atom):
            return f"{pretty(t.left)} ^ {pretty(t.right)}"
        return f"{pretty(t.left)} {t.op} {pretty(t.right)}"
    if isinstance(t, Loop):
        return "[" + pretty(t.body) + "]"
    if isinstance(t, Final):
        return pretty(t.term) + " ="
    return "?"
