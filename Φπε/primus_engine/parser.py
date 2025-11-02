from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from .ast import Atom, Call, Infix, Loop, Final, Term, SYMBOLS, OPERATORS

# Lexer with strict UTF-8 symbol/operator enforcement

@dataclass
class Tok:
    kind: str
    text: str

GROUP = {'(', ')', '[', ']', ',',}\

OP_CHARS = {"→","+",":","/","|","=","^"}

HEADER_LINES = (
    "Φπε PRIMUS :: SYMBOL SET",
    "Φπε PRIMUS :: OPERATOR SET",
)

class Lexer:
    def __init__(self, src: str):
        self.s = src
        self.i = 0

    def peek(self) -> str:
        return self.s[self.i] if self.i < len(self.s) else ''

    def next(self) -> str:
        ch = self.peek()
        if ch:
            self.i += 1
        return ch

    def skip_ws(self):
        while self.peek() and self.peek().isspace():
            self.i += 1

    def read_atom(self) -> Optional[str]:
        ch = self.peek()
        if ch in SYMBOLS:
            self.i += 1
            return ch
        return None

    def read_op(self) -> Optional[str]:
        ch = self.peek()
        if not ch:
            return None
        if ch in OP_CHARS:
            self.i += 1
            return ch
        return None

    def tokens(self) -> List[Tok]:
        toks: List[Tok] = []
        while True:
            self.skip_ws()
            ch = self.peek()
            if not ch:
                break
            if ch in GROUP:
                toks.append(Tok(ch, ch))
                self.i += 1
                continue
            if ch == 'Σ':
                # Allow Σ in header call and body as Atom or Call head
                toks.append(Tok('ATOM', 'Σ'))
                self.i += 1
                continue
            if ch == 'Φ' and self.s[self.i:self.i+len(HEADER_LINES[0])] == HEADER_LINES[0]:
                # Consume header line token as a unit
                toks.append(Tok('HDR1', HEADER_LINES[0]))
                self.i += len(HEADER_LINES[0])
                continue
            if ch == 'Φ' and self.s[self.i:self.i+len(HEADER_LINES[1])] == HEADER_LINES[1]:
                toks.append(Tok('HDR2', HEADER_LINES[1]))
                self.i += len(HEADER_LINES[1])
                continue
            atom = self.read_atom()
            if atom is not None:
                toks.append(Tok('ATOM', atom))
                continue
            op = self.read_op()
            if op is not None:
                toks.append(Tok('OP', op))
                continue
            # Accept commas in lists
            if ch == ',':
                toks.append(Tok(',', ','))
                self.i += 1
                continue
            # Newlines ignored at lexer level; parser may segment statements per line externally
            if ch in {'\n', '\r'}:
                self.i += 1
                continue
            # Any other character is invalid per strict set
            raise SyntaxError(f"Invalid character '{ch}' at {self.i}")
        return toks

# Pratt parser with precedence

PRECEDENCE = {
    '→': 1,
    '+': 2,
    ':': 3,
    '/': 4,
    '|': 5,
    '^': 6,  # handled specially (prefix/infix)
}

class Parser:
    def __init__(self, src: str):
        self.src = src
        self.toks = Lexer(src).tokens()
        self.i = 0
        self.loop_uid = 0

    def peek(self) -> Optional[Tok]:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def eat(self, kind: str) -> Tok:
        t = self.peek()
        if t is None or t.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {t}")
        self.i += 1
        return t

    def match(self, kind: str, text: Optional[str]=None) -> Optional[Tok]:
        t = self.peek()
        if t and t.kind == kind and (text is None or t.text == text):
            self.i += 1
            return t
        return None

    def parse_header(self):
        # Enforce canonical header at file start and consume it so it's not treated as program terms.
        # Header format (exact lines in source):
        # Φπε PRIMUS :: SYMBOL SET\n
        # Σ(Φ, ..., χ)\n
        # Φπε PRIMUS :: OPERATOR SET\n
        # Σ(→, +, :, /, |, [], =, ^)
        # We consume tokens corresponding to: HDR1, Σ(...), HDR2, Σ(...)
        t = self.peek()
        if t is None:
            raise SyntaxError("Empty source; header required")
        # Require HDR1
        if not (t.kind == 'HDR1' and t.text == HEADER_LINES[0]):
            raise SyntaxError("Missing canonical header: SYMBOL SET line not found at file start")
        self.i += 1
        # Expect Σ(...)
        self._consume_sigma_paren_block()
        # Require HDR2
        t2 = self.peek()
        if not (t2 and t2.kind == 'HDR2' and t2.text == HEADER_LINES[1]):
            raise SyntaxError("Missing canonical header: OPERATOR SET line not found after SYMBOL SET")
        self.i += 1
        # Expect Σ(...)
        self._consume_sigma_paren_block()

    def _consume_sigma_paren_block(self):
        # Expect ATOM 'Σ' then a balanced parenthesis block; contents are not parsed into AST
        t = self.peek()
        if not (t and t.kind == 'ATOM' and t.text == 'Σ'):
            raise SyntaxError("Header parse error: expected Σ(" )
        self.i += 1
        # Expect '('
        if not (self.peek() and self.peek().kind == '('):
            raise SyntaxError("Header parse error: expected '('")
        # Consume balanced parentheses
        depth = 0
        while True:
            tok = self.peek()
            if tok is None:
                raise SyntaxError("Header parse error: unclosed '(' in header Σ block")
            if tok.kind == '(':
                depth += 1
                self.i += 1
                continue
            if tok.kind == ')':
                depth -= 1
                self.i += 1
                if depth == 0:
                    break
                continue
            # For header blocks we simply consume tokens until parentheses close
            self.i += 1

    def parse_file(self) -> List[Term]:
        # Expect header block then statements separated by newlines in src; here we parse all terms greedily
        terms: List[Term] = []
        # Enforce and consume canonical header
        self.parse_header()
        # Parse until exhaustion
        while self.peek() is not None:
            # Skip extraneous commas or headers already consumed
            t = self.peek()
            if t.kind in {'HDR1','HDR2',',','(',')','[',']'}:
                # Let expression parser handle groupings; skip headers
                if t.kind in {'HDR1','HDR2'}:
                    self.i += 1
                    continue
            try:
                term = self.parse_expr()
                terms.append(term)
            except SyntaxError:
                # If cannot parse, advance one token to avoid infinite loop
                self.i += 1
        return terms

    def parse_expr(self) -> Term:
        left = self.parse_prefix()
        # Postfix '='
        if self.match('OP', '='):
            left = Final(left)
        return self.parse_infix_rhs(0, left)

    def parse_prefix(self) -> Term:
        t = self.peek()
        if t and t.kind == 'OP' and t.text == '^':
            self.i += 1
            right = self.parse_prefix()
            # Normalize prefix '^x' as Infix('^', x, Atom('n')) with 'n' as default tier symbol.
            return Infix('^', right, Atom('n'))
        return self.parse_postfix()

    def parse_postfix(self) -> Term:
        node = self.parse_primary()
        # Handle postfix '=' already in parse_expr to preserve precedence with infix
        return node

    def parse_primary(self) -> Term:
        t = self.peek()
        if t is None:
            raise SyntaxError("EOF")
        if t.kind == 'ATOM':
            self.i += 1
            head = Atom(t.text)
            # Call?
            if self.match('(', '('):
                args: List[Term] = []
                if not self.match(')', ')'):
                    while True:
                        args.append(self.parse_expr())
                        if self.match(',', ','):
                            continue
                        self.eat(')')
                        break
                return Call(head, tuple(args))
            return head
        if t.kind == '[':
            self.i += 1
            body = self.parse_expr()
            self.eat(']')
            self.loop_uid += 1
            return Loop(body, self.loop_uid)
        if t.kind == '(':
            self.i += 1
            inner = self.parse_expr()
            self.eat(')')
            return inner
        raise SyntaxError(f"Unexpected token {t}")

    def parse_infix_rhs(self, min_prec: int, left: Term) -> Term:
        while True:
            t = self.peek()
            if t is None or t.kind != 'OP':
                break
            op = t.text
            if op not in PRECEDENCE:
                if op == '=':
                    # handled at higher level
                    break
                break
            prec = PRECEDENCE[op]
            assoc_right = (op == '→') or (op == '^')
            if prec < min_prec:
                break
            self.i += 1
            right = self.parse_prefix()
            # Postfix '=' tightly binds to right core already handled there
            left = Infix(op, left, right)
            next_min = prec + (0 if assoc_right else 1)
            left = self.parse_infix_rhs(next_min, left)
        return left


def parse(src: str) -> List[Term]:
    return Parser(src).parse_file()
