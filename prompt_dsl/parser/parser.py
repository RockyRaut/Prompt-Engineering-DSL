from typing import List
from prompt_dsl.lexer.lexer import Token
from prompt_dsl.ast.nodes import ProgramNode, AgentNode


class ParseError(Exception):
    pass


class Parser:
    """Parses token stream into an AST (ProgramNode)."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ProgramNode:
        program = ProgramNode()
        current_agent = None

        while self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            t = tok.type

            #Agent Declaration & Context Switching
            if t == "AGENT":
                name = tok.value or "Unnamed"
                current_agent = AgentNode(name=name)
                program.agents.append(current_agent)
                self.pos += 1
                continue

           # Implicit Default Agent Safety Net
            if current_agent is None:
                # If no agent declared yet, implicitly create a default agent
                current_agent = AgentNode(name="DefaultAgent")
                program.agents.append(current_agent)

            # State Attributes (Single Values)
            if t == "ROLE":
                current_agent.role = tok.value
            #  Boolean System Flags
            elif t == "TASK":
                if tok.value:
                    current_agent.tasks.append(tok.value)
            elif t == "INPUT":
                if tok.value:
                    current_agent.inputs.append(tok.value.strip('"'))
            elif t == "OUTPUT":
                current_agent.output = tok.value
            elif t == "CONSTRAINT":
                if tok.value:
                    current_agent.constraints.append(tok.value)
            # Boolean System Flags
            elif t == "MEMORY":
                v = tok.value.upper() if tok.value else "OFF"
                current_agent.memory = v == "ON"
            elif t == "RAG":
                v = tok.value.upper() if tok.value else "OFF"
                current_agent.rag = v == "ON"
            elif t == "TOOL":
                if tok.value:
                    current_agent.tools.append(tok.value)
            else:
                # Allow stray IDENTIFIER/STRING lines as informal input/task
                if t in ("STRING", "IDENTIFIER") and tok.value:
                    # Heuristic: if looks like a file, treat as input
                    if "." in tok.value:
                        current_agent.inputs.append(tok.value)
                    else:
                        current_agent.tasks.append(tok.value)

            self.pos += 1

        return program
