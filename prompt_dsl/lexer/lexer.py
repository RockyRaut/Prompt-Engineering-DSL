from dataclasses import dataclass
from typing import List


KEYWORDS = {
    "AGENT",
    "ROLE",
    "TASK",
    "INPUT",
    "OUTPUT",
    "CONSTRAINT",
    "MEMORY",
    "TOOL",
    "RAG",
}


@dataclass
class Token:
    type: str
    value: str
    line: int


class Lexer:
    """Simple line-based lexer for the Prompt DSL."""

    @staticmethod
    def tokenize(text: str) -> List[Token]:
        tokens: List[Token] = []
        lines = text.splitlines()
        for i, raw in enumerate(lines, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split(maxsplit=1)
            kw = parts[0]
            rest = parts[1].strip() if len(parts) > 1 else ""

            if kw.upper() in KEYWORDS:
                tokens.append(Token(type=kw.upper(), value=rest, line=i))
            else:
                # Lines that don't start with a keyword are treated as IDENTIFIER or STRING
                # If the line contains spaces treat as STRING
                ttype = "STRING" if " " in line or "." in line or rest.startswith('"') else "IDENTIFIER"
                tokens.append(Token(type=ttype, value=line, line=i))

        return tokens
