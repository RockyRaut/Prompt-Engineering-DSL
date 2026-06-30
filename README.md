# Prompt DSL

This project implements a small Prompt Engineering DSL with a lexer, parser, AST, semantic validator, prompt generator, provider adapters and a Streamlit UI.

Install:

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Run Streamlit UI:

```bash
streamlit run prompt_dsl/ui/streamlit_app.py
```

Run CLI:

```bash
python -m prompt_dsl.main samples/example.dsl
```
