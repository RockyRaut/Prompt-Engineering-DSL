import sys
import os
import streamlit as st
import json

# Ensure project root is on sys.path so `prompt_dsl` package imports work when
# Streamlit runs from a different CWD/environment.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from prompt_dsl.lexer.lexer import Lexer
from prompt_dsl.parser.parser import Parser
from prompt_dsl.semantic.validator import Validator
from prompt_dsl.generator.prompt_generator import PromptGenerator
from prompt_dsl.providers.openai_provider import OpenAIProvider


def main():
    st.title("Prompt DSL — Editor")

    sample = st.session_state.get("sample", "AGENT WasteBot\n\nROLE EnvironmentalExpert\n\nTASK ClassifyWaste\n\nINPUT waste_image.jpg\n\nCONSTRAINT StepByStep\nCONSTRAINT Brief\n\nOUTPUT JSON")

    code = st.text_area("DSL Editor", value=sample, height=300)

    if st.button("Parse & Generate"):
        tokens = Lexer.tokenize(code)
        st.subheader("Tokens")
        st.write([t.__dict__ for t in tokens])

        parser = Parser(tokens)
        program = parser.parse()

        st.subheader("AST")
        st.json(program.to_dict())

        st.subheader("Validation")
        errors = Validator.validate(program)
        if errors:
            for e in errors:
                st.error(str(e))
        else:
            st.success("No semantic errors detected.")

        st.subheader("Generated Prompt")
        prompt = PromptGenerator.generate(program)
        st.code(prompt)

        st.subheader("Run (mock)")
        provider = OpenAIProvider()
        resp = provider.generate(prompt)
        st.text_area("Provider Response", value=resp, height=200)


if __name__ == "__main__":
    main()
