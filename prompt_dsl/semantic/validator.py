from typing import List
from prompt_dsl.ast.nodes import ProgramNode


class SemanticError(Exception):
    def __init__(self, message: str, line: int = None):
        super().__init__(message)
        self.line = line


class Validator:
    VALID_OUTPUTS = {"TEXT", "JSON", "MARKDOWN", "XML"}

    @staticmethod
    def validate(program: ProgramNode) -> List[SemanticError]:
        errors: List[SemanticError] = []

        if len(program.agents) == 0:
            errors.append(SemanticError("No agent declared."))
            return errors

        agent = program.agents[0]

        if not agent.role:
            errors.append(SemanticError("Missing ROLE declaration."))

        if not agent.tasks:
            errors.append(SemanticError("Missing TASK declaration."))

        if agent.output and agent.output.upper() not in Validator.VALID_OUTPUTS:
            errors.append(SemanticError(f"Invalid OUTPUT: {agent.output}. Must be one of {', '.join(Validator.VALID_OUTPUTS)}."))

        return errors
