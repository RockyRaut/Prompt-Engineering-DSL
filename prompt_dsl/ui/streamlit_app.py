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


def main():
    st.title("Prompt DSL — Article Summarizer")
    st.caption("This example is configured to summarize the contents of article.txt.")

    sample = st.session_state.get(
        "sample",
        "AGENT ArticleSummarizer\n\nROLE Summarizer\n\nTASK Summarize the article in article.txt\n\nINPUT article.txt\n\nCONSTRAINT Brief\n\nOUTPUT TEXT",
    )

    code = st.text_area("DSL Editor", value=sample, height=300)

    if st.button("Parse & Generate"):
        tokens = Lexer.tokenize(code)
        st.subheader("Tokens")
        st.write([t.__dict__ for t in tokens])

        parser = Parser(code)
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


if __name__ == "__main__":
    main()
