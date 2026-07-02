# Prompt DSL — Article Summarizer

This project implements a domain-specific language (DSL) for prompt engineering, configured as an article summarization tool. It features a PLY-based lexer and parser, AST, semantic validator, prompt generator, and an interactive Streamlit UI.

The DSL enables you to define prompts using fixed keywords (`AGENT`, `ROLE`, `TASK`, `INPUT`, `OUTPUT`, `CONSTRAINT`) and generates consistent, structured AI prompts from them.

Install:

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Run Streamlit UI (interactive editor):

```bash
streamlit run prompt_dsl/ui/streamlit_app.py
```

Run CLI (parse and generate prompt):

```bash
python -m prompt_dsl.main samples/example.dsl
```

## Quick Start

The example DSL in `samples/example.dsl` is pre-configured to summarize `article.txt`:

```dsl
AGENT ArticleSummarizer
ROLE Summarizer
TASK Summarize the article in article.txt
INPUT article.txt
CONSTRAINT Brief
OUTPUT TEXT
```

This generates a prompt that instructs an AI to summarize the article concisely as text.
