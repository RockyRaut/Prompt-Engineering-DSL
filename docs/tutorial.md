# Prompt DSL Tutorial — Article Summarizer

This document explains the Prompt DSL project in a teaching style, with a focus on the article summarization use case. You can present this to your teacher.

## 1. What is this project?

This repository implements a small domain-specific language (DSL) for prompt engineering, configured as an **article summarization tool**. It converts a simple text-based DSL into a structured AI prompt that can summarize text files.

It includes:
- a lexer to split the DSL into tokens
- a parser to build an AST (abstract syntax tree)
- a semantic validator to catch wrong or missing declarations
- a prompt generator to produce a final prompt string
- a Streamlit UI to edit and visualize the DSL interactively

## 2. Why use a DSL here?

A DSL lets you describe a text summarization task in a compact, structured way. Instead of writing prompts as free-form text, you use fixed keywords such as `ROLE`, `TASK`, `INPUT`, and `OUTPUT`.

That makes the prompt easier to parse, validate, and generate consistently. For example, you can define different summarization tasks by changing the `TASK` and `CONSTRAINT` values, while keeping the same DSL structure.

---

## 3. Key DSL concepts

### DSL keywords

The language uses these keywords:
- `AGENT` — names the agent
- `ROLE` — defines the AI role
- `TASK` — describes what the agent should do
- `INPUT` — specifies input data or file names
- `OUTPUT` — selects a desired output format
- `CONSTRAINT` — adds special instructions
- `MEMORY` — turns memory on/off
- `RAG` — turns retrieval-augmented generation on/off
- `TOOL` — lists tools the agent may use

### Example DSL file

`samples/example.dsl` (configured for article summarization):

```
AGENT ArticleSummarizer

ROLE Summarizer

TASK Summarize the article in article.txt

INPUT article.txt

CONSTRAINT Brief

OUTPUT TEXT
```

What this means:
- Agent name: `ArticleSummarizer`
- Role: `Summarizer` (AI acts as a helpful summarizer)
- Task: `Summarize the article in article.txt`
- Input: `article.txt` (the file containing the article to summarize)
- Constraint: `Brief` (keep the summary concise)
- Desired output format: `TEXT`

---

## 4. File-by-file explanation

### `README.md`
- Project summary and usage instructions.
- Explains how to run the Streamlit app and CLI.

### `requirements.txt`
- Contains Python dependencies needed to run the project.

### `prompt_dsl/__init__.py`
- Marks `prompt_dsl` as a Python package.
- Exports package modules: `lexer`, `parser`, `ast`, `semantic`, `generator`, and `ui`.

### `prompt_dsl/main.py`
- CLI entry point.
- Reads a `.dsl` file and runs the full pipeline.
- Steps in `main()`:
  1. Load DSL source text
  2. Tokenize with `Lexer.tokenize()`
  3. Parse with `Parser(tokens).parse()`
  4. Validate with `Validator.validate(program)`
  5. Generate prompt with `PromptGenerator.generate(program)`
  6. Print the final prompt

### `prompt_dsl/lexer/lexer.py`
- Defines `Token` objects and the `Lexer`.
- `Lexer.tokenize(text)` does simple line-based scanning.
- It ignores blank lines and comments starting with `#`.
- Recognizes DSL keywords and stores the rest of the line as the token value.
- If a line does not start with a known keyword, it becomes `IDENTIFIER` or `STRING`.

Why this matters:
- Lexing turns raw text into structured pieces the parser can understand.

### `prompt_dsl/parser/parser.py`
- Converts tokens into a `ProgramNode` AST.
- Uses `AgentNode` to represent a single agent and its properties.
- Handles the main keywords and also a fallback for stray text lines.
- If no `AGENT` line appears, the parser creates a default agent automatically.

Important behavior:
- `AGENT` starts a new agent
- `ROLE` assigns a role
- `TASK`, `INPUT`, `CONSTRAINT`, `TOOL` append values to lists
- `MEMORY` and `RAG` become boolean flags
- `OUTPUT` stores output type

### `prompt_dsl/ast/nodes.py`
- Contains the AST node definitions.
- `AgentNode` holds all agent-related fields.
- `ProgramNode` holds a list of agents.
- `ProgramNode.to_dict()` converts the AST into a normalized dictionary for display.

Why this matters:
- The AST is the structured representation of the DSL after parsing.
- It separates parsing from generation and validation.

### `prompt_dsl/semantic/validator.py`
- Performs semantic checks on the parsed program.
- Ensures required fields exist and values are valid.
- Rules in the current validator:
  - At least one `AGENT` must exist
  - Only one `AGENT` is allowed right now
  - `ROLE` is required
  - `TASK` is required
  - `OUTPUT`, if present, must be one of `TEXT`, `JSON`, `MARKDOWN`, or `XML`

Why this matters:
- Validation catches logical mistakes before prompt generation.
- It enforces the DSL contract.

### `prompt_dsl/generator/prompt_generator.py`
- Builds the final prompt text from the AST.
- Takes only the first agent in the current implementation.
- Converts known roles into nicer role descriptions using `ROLE_TEMPLATES`.
- For the Summarizer role, it produces: `"You are a helpful summarizer."`
- Writes the task, input, constraints, memory, tools, RAG, and output rules.
- Joins the parts into a readable prompt.

Example output from `samples/example.dsl`:

```
You are a helpful summarizer.

Task:
Summarize the article in article.txt

Input: article.txt

Instructions:
- Keep the response concise.

Return response as TEXT.
```

Why this matters:
- Prompt generation is the main goal of the DSL: turn structured input into an AI-ready instruction.

### `prompt_dsl/ui/streamlit_app.py`
- Provides an interactive editor and viewer for the DSL.
- Title: "Prompt DSL — Article Summarizer"
- Pre-loaded with the article summarization example.
- Shows:
  - token list
  - parsed AST
  - validation results
  - generated prompt
- Useful for teaching because it makes the pipeline visible step-by-step.

---

## 5. How the whole pipeline works

When you run the CLI or UI, the project follows this pipeline:

1. `Lexer.tokenize(text)`
   - reads DSL lines
   - converts them to tokens

2. `Parser(source).parse()`
   - builds a `ProgramNode` AST

3. `Validator.validate(program)`
   - checks if the program is semantically valid

4. `PromptGenerator.generate(program)`
   - creates a prompt for article summarization

5. The project is self-contained.
   - It generates prompts locally and does not call any external AI backend.

This is the simplest useful architecture for a self-contained DSL.

---

## 6. How to explain it in class

### Start with the idea
- "This code is a mini language for defining AI summarization tasks."
- "It lets us describe what we want summarized using fixed sections instead of free-form text."

### Walk through the layers
- "First, the lexer turns text into tokens."
- "Then the parser turns tokens into a structured program object."
- "The validator checks the rules."
- "The generator turns the structured data into a real prompt."

### Use the example
- Show the DSL source from `samples/example.dsl`
- Show the generated summarization prompt
- Emphasize that changing the TASK or CONSTRAINT updates the generated prompt automatically
- Demo: edit the DSL in the Streamlit UI and watch the prompt regenerate in real-time

### Mention the UI
- The Streamlit app is a teaching tool: it displays tokens, AST, validation, and prompt output.

---

## 7. Additional details to remember

- The current parser supports only one agent in practice.
- The project is focused on article summarization as its primary use case.
- The validator is simple and can be extended with more rules.
- The AST is a clean separation point between parsing and generation.
- The `article.txt` file in the project root is the input that the example DSL references.

---

## 8. Running the tutorial project

Use these commands:

- CLI: `python -m prompt_dsl.main samples/example.dsl`
- UI: `streamlit run prompt_dsl/ui/streamlit_app.py`

If you want to teach it, try editing `article.txt` or the DSL in `samples/example.dsl`, and watch how the generated prompt changes.

---

## 9. Suggested way to present this

1. Show the article text in `article.txt`.
2. Show the DSL file `samples/example.dsl`.
3. Explain each keyword and its role in the summarization task.
4. Describe the pipeline (lex → parse → validate → generate).
5. Show the generated prompt.
6. Run the example in Streamlit and demonstrate editing the DSL live.
7. Mention where to add new keywords or new validation rules.

This gives your teacher a complete view of both the code and the design, and demonstrates the end-to-end workflow.
