import sys
from prompt_dsl.lexer.lexer import Lexer
from prompt_dsl.parser.parser import Parser
from prompt_dsl.semantic.validator import Validator
from prompt_dsl.generator.prompt_generator import PromptGenerator


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: main.py <dsl-file>")
        return 2

    path = argv[0]
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tokens = Lexer.tokenize(src)
    parser = Parser(tokens)
    program = parser.parse()

    errors = Validator.validate(program)
    if errors:
        for e in errors:
            print("Semantic error:", e)
        return 1

    prompt = PromptGenerator.generate(program)
    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
