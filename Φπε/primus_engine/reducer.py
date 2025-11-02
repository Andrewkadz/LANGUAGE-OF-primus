from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from .ast import Atom, Call, Infix, Loop, Final, Term, pretty

# Configurable thresholds (not fully used in this minimal reducer; present for SPEC parity)
@dataclass
class Config:
    theta_loop: int = 3
    theta_alt: int = 2
    theta_depth: int = 2
    alt_window: int = 5
    pi_blocks_final: bool = True

# Symbol atoms for convenience
A_XI = Atom('Ξ')
A_DELTA = Atom('Δ')
A_LAMBDA = Atom('Λ')
A_PSI = Atom('Ψ')
A_PI = Atom('Π')
A_SIGMA = Atom('Σ')
A_PHI = Atom('Φ')
A_ZETA = Atom('ζ')
A_OMEGA = Atom('Ω')

# Build symbolic trace entries: Λ[ rule : input : output : context : loop : tick ]

def repeat(term: Term, k: int) -> Call:
    # Σ(term, term, ..., term)
    return Call(A_SIGMA, tuple(term for _ in range(k)))

def loop_snapshot_empty() -> Call:
    # Empty Σ() when no snapshot is applicable
    return Call(A_SIGMA, tuple())

def loop_snapshot_state(tick: int, has_delta: bool, has_psi: bool) -> Call:
    # Build a symbolic snapshot of the loop as repetition of a simple motif inside []
    # If both Δ and Ψ are present, use the Δ:Ψ interaction as motif. Else, leave empty.
    if not (has_delta and has_psi) or tick <= 0:
        return Call(A_SIGMA, tuple())
    motif = Infix(':', A_DELTA, A_PSI)
    snaps = tuple(Loop(motif, 0) for _ in range(tick))
    return Call(A_SIGMA, snaps)

def tick_terms(k: int) -> Call:
    return repeat(A_ZETA, k)

def trace_entry(rule: Atom, inp: Term, out: Term, ctx: Term, loop: Term, tick_count: int) -> Call:
    return Call(Atom('Λ'), (rule, inp, out, ctx, loop, tick_terms(tick_count)))

# Helpers

def is_pi_node(t: Term) -> bool:
    return isinstance(t, Call) and isinstance(t.head, Atom) and t.head.sym == 'Π'

def ctx_term(in_pi: bool) -> Term:
    # context rendering; Φ if no extra context for now
    return A_PHI

# One small-step reduction and one trace entry

class LoopState:
    def __init__(self):
        self.tick: int = 0
        self.alt: int = 0
        self.depth: int = 0
        self.window: List[str] = []  # recent ops labels like 'Δ' or 'Ψ'


def step(t: Term, tick: int, in_pi: bool, loops: Dict[int, LoopState], cfg: Config, disrupt: bool = False) -> Tuple[Term, Optional[Call]]:
    # Priority: Loop (no-op here), Δ, Ψ, Γ(congruence), Λ, + to Σ, → pipeline
    # 1) Reduce inside parentheses / calls / infix recursively (outermost-first congruence)
    # Normalize plus: Infix('+', a, b) -> Σ(a,b)
    if isinstance(t, Infix) and t.op == '+':
        # flatten right if already Σ
        left = t.left
        right = t.right
        items: List[Term] = []
        if isinstance(left, Call) and isinstance(left.head, Atom) and left.head.sym == 'Σ':
            items.extend(left.args)
        else:
            items.append(left)
        if isinstance(right, Call) and isinstance(right.head, Atom) and right.head.sym == 'Σ':
            items.extend(right.args)
        else:
            items.append(right)
        out = Call(A_SIGMA, tuple(items))
        tr = None if in_pi else trace_entry(Atom('+'), t, out, ctx_term(in_pi), loop_snapshot_empty(), tick)
        return out, tr

    # → pipeline: apply RHS operator to LHS term
    if isinstance(t, Infix) and t.op == '→':
        lhs, rhs = t.left, t.right
        # If rhs is an Atom operator, wrap lhs accordingly
        if isinstance(rhs, Atom):
            if rhs.sym in {'Ξ','Δ','Λ','Ψ','Π','Ω'}:
                # In disruption context, block immediate Δ application
                if disrupt and rhs.sym == 'Δ':
                    # fall through to try reducing children instead of applying Δ
                    pass
                else:
                    out = Call(rhs, (lhs,))
                    tr = None if in_pi else trace_entry(rhs, t, out, ctx_term(in_pi), loop_snapshot_empty(), tick)
                    return out, tr
        # Prefer to reduce lhs first (e.g., loop emergence) before applying rhs
        lhs2, tr = step(lhs, tick, in_pi, loops, cfg, disrupt)
        if tr is not None:
            out = Infix('→', lhs2, rhs)
            return out, tr
        # Then reduce rhs if lhs cannot progress
        rhs2, tr = step(rhs, tick, in_pi, loops, cfg, disrupt)
        if tr is not None:
            out = Infix('→', lhs, rhs2)
            return out, tr
        return t, None

    # Λ render: Λ(x) stays but trace the rendering intent
    if isinstance(t, Call) and isinstance(t.head, Atom) and t.head.sym == 'Λ' and len(t.args) == 1:
        # We consider Λ(x) a rendering step; produce trace but do not rewrite further
        tr = None if in_pi else trace_entry(A_LAMBDA, t.args[0], t, ctx_term(in_pi), loop_snapshot_empty(), tick)
        return t, tr

    # Σ member reduction (left-to-right)
    if isinstance(t, Call) and isinstance(t.head, Atom) and t.head.sym == 'Σ':
        for i, it in enumerate(t.args):
            # enter Π-context if member is Π(...)
            next_in_pi = in_pi or is_pi_node(it)
            it2, tr = step(it, tick, next_in_pi, loops, cfg, disrupt)
            if tr is not None:
                args2 = list(t.args)
                args2[i] = it2
                return Call(A_SIGMA, tuple(args2)), tr
        return t, None

    # Call: reduce inside
    if isinstance(t, Call):
        # Reduce argument first
        if len(t.args) > 0:
            a0 = t.args[0]
            # If head is Π, we enter Π-context for its body
            next_in_pi = in_pi or (isinstance(t.head, Atom) and t.head.sym == 'Π')
            a02, tr = step(a0, tick, next_in_pi, loops, cfg, disrupt)
            if tr is not None:
                args2 = list(t.args)
                args2[0] = a02
                return Call(t.head, tuple(args2)), tr
        return t, None

    # Loop: reduce inside
    if isinstance(t, Loop):
        # Get or init state
        st = loops.setdefault(t.uid, LoopState())
        # Reduce inside body to gather ops and depth
        b2, tr = step(t.body, tick, in_pi, loops, cfg, disrupt)
        # Update depth heuristically: +1 if body contains nested Σ, Δ, or Ψ
        # Simple syntactic check
        if isinstance(t.body, Infix) and t.body.op in {'+', ':'}:
            st.depth = max(st.depth, 2)
        elif isinstance(t.body, Call) and isinstance(t.body.head, Atom) and t.body.head.sym in {'Δ','Ψ','Σ'}:
            st.depth = max(st.depth, 2)
        else:
            st.depth = max(st.depth, 1)
        # Alternation detection: if body contains both Δ and Ψ anywhere, increase alternation density
        def contains_op(x: Term, syms: set) -> bool:
            if isinstance(x, Call):
                if isinstance(x.head, Atom) and x.head.sym in syms:
                    return True
                return any(contains_op(a, syms) for a in x.args)
            if isinstance(x, Infix):
                return contains_op(x.left, syms) or contains_op(x.right, syms)
            if isinstance(x, Loop):
                return contains_op(x.body, syms)
            if isinstance(x, Final):
                return contains_op(x.term, syms)
            return False

        has_delta = contains_op(t.body, {'Δ'})
        has_psi = contains_op(t.body, {'Ψ'})
        if has_delta and has_psi:
            # increase alternation per pass up to window limit
            st.alt = min(cfg.alt_window, st.alt + 1)
        # Increment tick when body changed or per pass
        st.tick += 1
        # Trigger Ξ if thresholds met
        if st.tick >= cfg.theta_loop and st.alt >= cfg.theta_alt and st.depth >= cfg.theta_depth:
            xi = Call(A_XI, (t.body,))
            # Emit loop snapshot based on current state
            snap = loop_snapshot_state(st.tick, has_delta, has_psi)
            tr2 = None if in_pi else trace_entry(A_XI, t, xi, ctx_term(in_pi), snap, tick)
            return xi, tr2
        # Otherwise, propagate body change and possible trace from inside
        if tr is not None:
            return Loop(b2, t.uid), tr
        return t, None

    # Final: enforce Π finalization block; otherwise, do not descend
    if isinstance(t, Final):
        if in_pi:
            # Strip finalization inside Π to block '=' within Π-context
            return t.term, None
        return t, None

    # Orthogonality: reduce fields independently; no cross-field interactions
    if isinstance(t, Infix) and t.op == '|':
        l2, tr = step(t.left, tick, in_pi, loops, cfg, disrupt)
        if tr is not None:
            return Infix('|', l2, t.right), tr
        r2, tr = step(t.right, tick, in_pi, loops, cfg, disrupt)
        if tr is not None:
            return Infix('|', t.left, r2), tr
        return t, None

    # Lift '^': reduce operands congruently; no rewrite or trace (non-finalizing structural lift)
    if isinstance(t, Infix) and t.op == '^':
        l2, tr = step(t.left, tick, in_pi, loops, cfg, disrupt)
        if tr is not None:
            return Infix('^', l2, t.right), tr
        r2, tr = step(t.right, tick, in_pi, loops, cfg, disrupt)
        if tr is not None:
            return Infix('^', t.left, r2), tr
        return t, None

    # Disruption: block nearest interactions and reset loop density in right scope
    if isinstance(t, Infix) and t.op == '/':
        l2, tr = step(t.left, tick, in_pi, loops, cfg, disrupt)
        if tr is not None:
            return Infix('/', l2, t.right), tr
        # Right side evaluated under disruption with fresh loop state
        r2, tr = step(t.right, tick, in_pi, {}, cfg, True)
        if tr is not None:
            return Infix('/', t.left, r2), tr
        return t, None

    return t, None

# Evaluate a term to weak normal form with trace Σ[Λ[…], …]

def reduce_with_trace(t: Term, max_steps: int = 256, cfg: Optional[Config] = None) -> Call:
    if cfg is None:
        cfg = Config()
    tick = 0
    traces: List[Call] = []
    cur = t
    loops: Dict[int, LoopState] = {}
    while tick < max_steps:
        # Determine if current root is a Π node
        root_in_pi = is_pi_node(cur)
        nxt, tr = step(cur, tick+1, root_in_pi, loops, cfg)
        if tr is None:
            break
        traces.append(tr)
        cur = nxt
        tick += 1
    # Σ[ Λ[…], … ]
    return Call(A_SIGMA, tuple(traces))
