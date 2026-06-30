from prompt_dsl.lexer.lexer import Lexer
from prompt_dsl.parser.parser import Parser
from prompt_dsl.generator.prompt_generator import PromptGenerator


def test_example_dsl():
    dsl = """
AGENT WasteBot

ROLE EnvironmentalExpert

TASK ClassifyWaste

INPUT waste_image.jpg

CONSTRAINT StepByStep
CONSTRAINT Brief

OUTPUT JSON
"""

    tokens = Lexer.tokenize(dsl)
    parser = Parser(tokens)
    program = parser.parse()

    prompt = PromptGenerator.generate(program)
    assert "Environmental Expert" in prompt or "EnvironmentalExpert" in prompt
    assert "ClassifyWaste" in prompt or "Classify Waste" in prompt or "ClassifyWaste" in prompt
    assert "JSON" in prompt.upper()
