from dataclasses import dataclass
from typing import List
import re
import sys
import ply.lex as lex

KEYWORDS = {
    "AGENT",
    "ROLE",
    "TASK",
    "INPUT",
    "OUTPUT",
    "CONSTRAINT",
}

tokens = [
    "AGENT",
    "ROLE",
    "TASK",
    "INPUT",
    "OUTPUT",
    "CONSTRAINT",
    "VALUE",
    "NEWLINE",
]

t_ignore = " \t"

@dataclass
class Token:
    type: str
    value: str
    line: int


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")
    t.type = "NEWLINE"
    return t


def t_COMMENT(t):
    r"\#[^\n]*"
    pass


def t_KEYWORD(t):
    r"\b(?:AGENT|ROLE|TASK|INPUT|OUTPUT|CONSTRAINT|MEMORY|RAG|TOOL)\b"
    t.type = t.value.upper()
    return t


def t_VALUE(t):
    r"[^\n]+"
    t.value = t.value.strip()
    return t


def t_error(t):
    raise SyntaxError(f"Illegal character {t.value[0]!r} at line {t.lineno}")


def build_lexer():
    return lex.lex(module=sys.modules[__name__], optimize=False, reflags=re.IGNORECASE)


class Lexer:
    """PLY-based lexer for the Prompt DSL."""

    @staticmethod
    def tokenize(text: str) -> List[Token]:
        lexer = build_lexer()
        lexer.input(text)

        tokens: List[Token] = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            if tok.type == "NEWLINE":
                continue
            tokens.append(Token(type=tok.type, value=tok.value, line=tok.lineno))

        return tokens
