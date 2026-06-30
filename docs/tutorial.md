# Prompt DSL Tutorial

This document explains the Prompt DSL project in a teaching style, so you can present it clearly to your teacher.

## 1. What is this project?

This repository implements a small domain-specific language (DSL) for prompt engineering. It converts a simple text-based DSL into a structured AI prompt.

It includes:
- a lexer to split the DSL into tokens
- a parser to build an AST (abstract syntax tree)
- a semantic validator to catch wrong or missing declarations
- a prompt generator to produce a final prompt string
- provider adapters for different AI backends
- a Streamlit UI to edit and visualize the DSL interactively

## 2. Why use a DSL here?

A DSL lets you describe an AI task in a compact, structured way. Instead of writing prompts as free-form text, you use fixed keywords such as `ROLE`, `TASK`, `INPUT`, and `OUTPUT`.

That makes the prompt easier to parse, validate, and generate consistently.

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

`samples/example.dsl`:

```
AGENT WasteBot

ROLE EnvironmentalExpert

TASK ClassifyWaste

INPUT waste_image.jpg

CONSTRAINT StepByStep
CONSTRAINT Brief

OUTPUT JSON
```

What this means:
- Agent name: `WasteBot`
- Role: `EnvironmentalExpert`
- Task: `ClassifyWaste`
- Input: `waste_image.jpg`
- Two constraints: `StepByStep` and `Brief`
- Desired output format: `JSON`

---

## 4. File-by-file explanation

### `README.md`
- Project summary and usage instructions.
- Explains how to run the Streamlit app and CLI.

### `requirements.txt`
- Contains Python dependencies needed to run the project.

### `prompt_dsl/__init__.py`
- Marks `prompt_dsl` as a Python package.
- Exports package modules: `lexer`, `parser`, `ast`, `semantic`, `generator`, `providers`, and `ui`.

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
- Writes the task, input, constraints, memory, tools, RAG, and output rules.
- Joins the parts into a readable prompt.

Example output from `samples/example.dsl`:

```
You are an Environmental Expert.

Task:
ClassifyWaste

Input: waste_image.jpg

Instructions:
- Provide step-by-step reasoning.
- Keep the response concise.

Return response as JSON.
```

Why this matters:
- Prompt generation is the main goal of the DSL: turn structured input into an AI-ready instruction.

### `prompt_dsl/providers/base_provider.py`
- Defines `BaseProvider`, a simple abstract interface.
- `generate(prompt)` is the method every provider should implement.

### `prompt_dsl/providers/openai_provider.py`
- Implements `OpenAIProvider` as a mock adapter.
- In this project, it returns a placeholder response string.
- Designed to be replaced later with a real OpenAI SDK call.

### `prompt_dsl/providers/gemini_provider.py`
- Implements `GeminiProvider` as another mock adapter.
- Also returns a placeholder response.

### `prompt_dsl/providers/ollama_provider.py`
- Implements `OllamaProvider` as a mock adapter.
- Returns a placeholder response.

Why this matters:
- Provider adapters decouple prompt creation from the backend that runs the model.
- This helps the project scale to multiple AI services.

### `prompt_dsl/ui/streamlit_app.py`
- Provides an interactive editor and viewer for the DSL.
- Shows:
  - token list
  - parsed AST
  - validation results
  - generated prompt
  - mock provider response
- Useful for teaching because it makes the pipeline visible step-by-step.

---

## 5. How the whole pipeline works

When you run the CLI or UI, the project follows this pipeline:

1. `Lexer.tokenize(text)`
   - reads DSL lines
   - converts them to tokens

2. `Parser(tokens).parse()`
   - builds a `ProgramNode` AST

3. `Validator.validate(program)`
   - checks if the program is semantically valid

4. `PromptGenerator.generate(program)`
   - creates the final prompt string

5. Provider (optional)
   - `OpenAIProvider.generate(prompt)` or another provider may produce a response

This is the simplest useful architecture for a DSL.

---

## 6. How to explain it in class

### Start with the idea
- "This code is a mini language for building AI prompts."
- "It lets us describe the prompt using fixed sections instead of free-form text."

### Walk through the layers
- "First, the lexer turns text into tokens."
- "Then the parser turns tokens into a structured program object."
- "The validator checks the rules."
- "The generator turns the structured data into a real prompt."

### Use the example
- Show the DSL source
- Show the generated prompt
- Emphasize that the same DSL would generate consistent prompts every time

### Mention the UI
- The Streamlit app is a teaching tool: it displays tokens, AST, validation, and prompt output.

---

## 7. Additional details to remember

- The current parser supports only one agent in practice.
- The validator is simple and can be extended with more rules.
- The provider classes are stubs for future real integrations.
- The AST is a clean separation point between parsing and generation.

---

## 8. Running the tutorial project

Use these commands:

- CLI: `python -m prompt_dsl.main samples/example.dsl`
- UI: `streamlit run prompt_dsl/ui/streamlit_app.py`

If you want to teach it, open `samples/example.dsl`, change the DSL text, and watch how the output changes.

---

## 9. Suggested way to present this

1. Show the DSL file.
2. Explain each keyword.
3. Describe the pipeline.
4. Show the generated prompt.
5. Mention where to add new keywords or new validation rules.

This gives your teacher a complete view of both the code and the design.
