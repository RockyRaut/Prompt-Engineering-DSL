from typing import List, Optional, Tuple
import ply.yacc as yacc
from prompt_dsl.lexer.lexer import build_lexer, tokens as lexer_tokens
from prompt_dsl.ast.nodes import ProgramNode, AgentNode


class ParseError(Exception):
    pass


tokens = lexer_tokens


def p_program(p):
    "program : statements"
    p[0] = p[1]


def p_statements_multiple(p):
    """statements : statements statement"""
    p[0] = p[1]
    if p[2] is not None:
        p[0].append(p[2])


def p_statements_single(p):
    """statements : statement"""
    p[0] = []
    if p[1] is not None:
        p[0].append(p[1])


def p_statement_keyword(p):
    """statement : AGENT optional_value NEWLINE
                 | ROLE optional_value NEWLINE
                 | TASK optional_value NEWLINE
                 | INPUT optional_value NEWLINE
                 | OUTPUT optional_value NEWLINE
                 | CONSTRAINT optional_value NEWLINE
                 | AGENT optional_value
                 | ROLE optional_value
                 | TASK optional_value
                 | INPUT optional_value
                 | OUTPUT optional_value
                 | CONSTRAINT optional_value"""
    p[0] = (p[1].upper(), p[2])


def p_statement_text(p):
    """statement : VALUE NEWLINE
                 | VALUE"""
    p[0] = ("VALUE", p[1])


def p_statement_blank(p):
    """statement : NEWLINE"""
    p[0] = None


def p_optional_value_value(p):
    """optional_value : VALUE"""
    p[0] = p[1].strip() if p[1] else ""


def p_optional_value_empty(p):
    """optional_value :"""
    p[0] = ""


def p_error(p):
    if not p:
        raise ParseError("Syntax error at end of input")
    raise ParseError(f"Syntax error at token {p.type!r} (value={p.value!r}) on line {p.lineno}")


parser = yacc.yacc()


class Parser:
    """Parses raw DSL text into an AST using PLY."""

    def __init__(self, source: str):
        self.source = source

    def parse(self) -> ProgramNode:
        try:
            statements = parser.parse(self.source, lexer=build_lexer(), tracking=True)
        except (SyntaxError, ParseError) as exc:
            raise ParseError(str(exc))

        return self._build_ast(statements)

    def _build_ast(self, statements: List[Tuple[str, str]]) -> ProgramNode:
        program = ProgramNode()
        current_agent: Optional[AgentNode] = None

        for statement in statements:
            if statement is None:
                continue

            token_type, value = statement

            if token_type == "AGENT":
                name = value or "Unnamed"
                current_agent = AgentNode(name=name)
                program.agents.append(current_agent)
                continue

            if current_agent is None:
                current_agent = AgentNode(name="DefaultAgent")
                program.agents.append(current_agent)

            if token_type == "ROLE":
                current_agent.role = value
            elif token_type == "TASK":
                if value:
                    current_agent.tasks.append(value)
            elif token_type == "INPUT":
                if value:
                    current_agent.inputs.append(value.strip('"'))
            elif token_type == "OUTPUT":
                current_agent.output = value
            elif token_type == "CONSTRAINT":
                if value:
                    current_agent.constraints.append(value)
            elif token_type == "VALUE":
                if value:
                    if "." in value:
                        current_agent.inputs.append(value)
                    else:
                        current_agent.tasks.append(value)

        return program
