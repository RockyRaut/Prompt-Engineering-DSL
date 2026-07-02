from prompt_dsl.lexer.lexer import Lexer
from prompt_dsl.parser.parser import Parser
from prompt_dsl.generator.prompt_generator import PromptGenerator


def test_example_dsl():
    dsl = """
AGENT ArticleSummarizer

ROLE Summarizer

TASK Summarize the article in article.txt

INPUT article.txt

CONSTRAINT Brief

OUTPUT TEXT
"""

    tokens = Lexer.tokenize(dsl)
    parser = Parser(dsl)
    program = parser.parse()

    prompt = PromptGenerator.generate(program)
    assert "helpful summarizer" in prompt.lower()
    assert "article.txt" in prompt
    assert "TEXT" in prompt.upper()


def test_parser_accepts_missing_final_newline():
    dsl = """AGENT WasteBot\nROLE EnvironmentalExpert\nTASK ClassifyWaste\nOUTPUT JSON"""

    parser = Parser(dsl)
    program = parser.parse()

    assert program.agents[0].name == "WasteBot"
    assert program.agents[0].role == "EnvironmentalExpert"
    assert program.agents[0].tasks == ["ClassifyWaste"]
    assert program.agents[0].output == "JSON"


def test_summarization_example_generates_a_helpful_summary_prompt():
    dsl = """
AGENT ArticleSummarizer

ROLE Summarizer

TASK Summarize the article in article.txt

INPUT article.txt

CONSTRAINT Brief

OUTPUT TEXT
"""

    parser = Parser(dsl)
    program = parser.parse()

    prompt = PromptGenerator.generate(program)

    assert "article.txt" in prompt
    assert "Summarize the article in article.txt" in prompt
    assert "helpful summarizer" in prompt.lower()
