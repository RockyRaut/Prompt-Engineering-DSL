import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from prompt_dsl.lexer.lexer import Lexer
from prompt_dsl.parser.parser import Parser
from prompt_dsl.semantic.validator import Validator
from prompt_dsl.generator.prompt_generator import PromptGenerator


def run(path: str):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    print("--- SOURCE ---")
    print(src)

    tokens = Lexer.tokenize(src)
    print("\n--- TOKENS ---")
    for t in tokens:
        print(f"{t.line}: {t.type} -> {t.value}")

    parser = Parser(src)
    program = parser.parse()

    print("\n--- AST (dict) ---")
    print(program.to_dict())

    errors = Validator.validate(program)
    print("\n--- VALIDATION ---")
    if errors:
        for e in errors:
            print("Error:", e)
    else:
        print("No semantic errors detected.")

    prompt = PromptGenerator.generate(program)
    print("\n--- GENERATED PROMPT ---")
    print(prompt)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: run_example.py <dsl-file>")
        raise SystemExit(2)
    path = sys.argv[1]
    run(path)
