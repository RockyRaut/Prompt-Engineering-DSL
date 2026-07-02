# Prompt Engineering DSL — Project Overview

## Executive Summary

This project implements a **Domain-Specific Language (DSL) for Prompt Engineering** that enables declarative definition of AI agent prompts. Instead of writing verbose, unstructured prompts by hand, developers define agents using structured keywords (`AGENT`, `ROLE`, `TASK`, `INPUT`, `OUTPUT`, `CONSTRAINT`), and the system automatically generates consistent, well-formatted prompts ready for LLMs.

**Real-world use case:** Article summarization tool that takes a simple DSL file and outputs a polished, structured prompt for an AI summarizer agent.

---

## Problem Statement

When building AI applications, prompt engineering is critical but tedious:

- **Inconsistency:** Each prompt is written ad-hoc, leading to variation in structure and quality.
- **Maintenance:** Updating prompts across many agents is error-prone and time-consuming.
- **Lack of validation:** No way to catch missing required fields (e.g., roles, tasks) before passing to an LLM.
- **Repetition:** Common patterns (role descriptions, output formats) are rewritten over and over.

**The DSL solution:** Standardize prompt definition, validate semantically, and generate consistently formatted output.

---

## Architecture Overview

The system follows a classic compiler pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                    Input: example.dsl                        │
│  AGENT ArticleSummarizer                                    │
│  ROLE Summarizer                                            │
│  TASK Summarize the article in article.txt                  │
│  INPUT article.txt                                          │
│  CONSTRAINT Brief                                           │
│  OUTPUT TEXT                                                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Lexer         │  Tokenize input into keywords & values
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Parser (PLY)  │  Build Abstract Syntax Tree (AST)
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Validator     │  Check semantic constraints
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Generator     │  Convert AST → Prompt
        └────────┬───────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────┐
│          Generated Prompt (ready for LLM)             │
│  You are a helpful summarizer.                        │
│                                                       │
│  Task:                                                │
│  Summarize the article in article.txt                 │
│                                                       │
│  Input: article.txt                                   │
│                                                       │
│  Instructions:                                        │
│  - Keep the response concise.                         │
│                                                       │
│  Return response as TEXT.                             │
└──────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. **Lexer** (`prompt_dsl/lexer/lexer.py`)

**Role:** Convert raw text into tokens (keyword-value pairs).

**Key Features:**
- Line-by-line tokenization
- Keyword recognition: `AGENT`, `ROLE`, `TASK`, `INPUT`, `OUTPUT`, `CONSTRAINT`
- Handles comments (lines starting with `#`)
- Distinguishes between keywords, identifiers, and string values

**Example:**
```python
Input:  "AGENT ArticleSummarizer"
Output: Token(type='AGENT', value='ArticleSummarizer', line=1)
```

---

### 2. **Parser** (`prompt_dsl/parser/parser.py`)

**Role:** Build an Abstract Syntax Tree (AST) from tokens using PLY yacc.

**Key Features:**
- **PLY yacc-based** grammar with production rules for statements
- Builds `ProgramNode` and `AgentNode` objects
- Handles optional values and missing newlines gracefully
- Accumulates task/constraint lists per agent

**Grammar (simplified):**
```
program    → statements
statements → statement | statements statement
statement  → KEYWORD [VALUE] [NEWLINE] | VALUE [NEWLINE]
```

**Example AST:**
```python
ProgramNode(
  agents=[
    AgentNode(
      name='ArticleSummarizer',
      role='Summarizer',
      tasks=['Summarize the article in article.txt'],
      inputs=['article.txt'],
      constraints=['Brief'],
      output='TEXT'
    )
  ]
)
```

---

### 3. **Semantic Validator** (`prompt_dsl/semantic/validator.py`)

**Role:** Enforce business logic constraints on the AST.

**Validation Rules:**
- ✅ At least one `AGENT` must be declared
- ✅ Each agent must have a `ROLE`
- ✅ Each agent must have a `TASK`
- ✅ `OUTPUT` must be one of: `TEXT`, `JSON`, `MARKDOWN`, `XML`

**Error Handling:**
```python
if not agent.role:
    errors.append(SemanticError("Missing ROLE declaration."))
```

---

### 4. **Prompt Generator** (`prompt_dsl/generator/prompt_generator.py`)

**Role:** Convert the validated AST into a human-readable, structured prompt.

**Template System:**
- **Role templates:** Map role names to persona descriptions
  ```python
  ROLE_TEMPLATES = {
      "SUMMARIZER": "You are a helpful summarizer.",
  }
  ```
- **Constraint templates:** Map constraint names to instructions
  ```python
  CONSTRAINT_TEMPLATES = {
      "BRIEF": "Keep the response concise.",
  }
  ```

**Generation Logic:**
1. Look up role template (fallback to `"You are an {role}."`)
2. Add task as main action
3. Include input file/data reference
4. Apply constraint instructions
5. Specify output format
6. Join with newlines

**Output:**
```
You are a helpful summarizer.

Task:
Summarize the article in article.txt

Input: article.txt

Instructions:
- Keep the response concise.

Return response as TEXT.
```

---

### 5. **CLI** (`prompt_dsl/main.py`)

**Role:** Orchestrate the full pipeline for command-line users.

**Flow:**
```python
main(argv):
    1. Load .dsl file
    2. Tokenize (Lexer)
    3. Parse (Parser)
    4. Validate (Validator)
    5. Generate (PromptGenerator)
    6. Print result
```

**Usage:**
```bash
python -m prompt_dsl.main samples/example.dsl
```

---

### 6. **Streamlit UI** (`prompt_dsl/ui/streamlit_app.py`)

**Role:** Interactive web interface for real-time DSL editing and visualization.

**Features:**
- **Live editor:** Paste or edit DSL code
- **Token viewer:** See tokenization output
- **AST inspector:** View the parsed syntax tree as JSON
- **Validation feedback:** Real-time semantic error detection
- **Prompt preview:** See the generated prompt instantly

**Run:**
```bash
streamlit run prompt_dsl/ui/streamlit_app.py
```

---

## Example Walkthrough

### Input DSL File (`samples/example.dsl`)
```dsl
AGENT ArticleSummarizer

ROLE Summarizer

TASK Summarize the article in article.txt

INPUT article.txt

CONSTRAINT Brief

OUTPUT TEXT
```

### Step 1: Tokenization
```
Token(type='AGENT', value='ArticleSummarizer', line=1)
Token(type='ROLE', value='Summarizer', line=3)
Token(type='TASK', value='Summarize the article in article.txt', line=5)
Token(type='INPUT', value='article.txt', line=7)
Token(type='CONSTRAINT', value='Brief', line=9)
Token(type='OUTPUT', value='TEXT', line=11)
```

### Step 2: Parsing (AST)
```python
ProgramNode(
  agents=[
    AgentNode(
      name='ArticleSummarizer',
      role='Summarizer',
      tasks=['Summarize the article in article.txt'],
      inputs=['article.txt'],
      constraints=['Brief'],
      output='TEXT'
    )
  ]
)
```

### Step 3: Validation
✅ All checks pass:
- Agent declared: `ArticleSummarizer`
- Role provided: `Summarizer`
- Task provided: `Summarize the article...`
- Output valid: `TEXT`

### Step 4: Generation
```
You are a helpful summarizer.

Task:
Summarize the article in article.txt

Input: article.txt

Instructions:
- Keep the response concise.

Return response as TEXT.
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Custom Lexer** (not PLY lex) | Simpler line-based tokenization for DSL simplicity; no complex token patterns needed |
| **PLY yacc Parser** | Proven, standardized parser generator; leverages established grammar rules |
| **Template-Based Generation** | Enables customization and reuse of common prompt patterns without code changes |
| **Semantic Validator Separate Stage** | Decouples validation from parsing; allows better error messages and multi-error reporting |
| **Streamlit UI** | Rapid prototyping, zero JavaScript, works out-of-the-box for real-time feedback |

---

## Technology Stack

| Component | Purpose |
|-----------|---------|
| **Python 3** | Core language |
| **PLY** | Parser generator (yacc) |
| **Streamlit** | Interactive web UI |
| **pytest** | Unit testing |
| **dataclasses** | AST node definitions |

---

## Running the Project

### Prerequisites
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### CLI Mode
```bash
python -m prompt_dsl.main samples/example.dsl
```

### Interactive UI
```bash
streamlit run prompt_dsl/ui/streamlit_app.py
```

### Run Tests
```bash
pytest tests/
```

---

## Test Suite

The project includes pytest-based tests covering:

1. **test_example_dsl()** — Full pipeline with example DSL
2. **test_parser_accepts_missing_final_newline()** — Edge case handling
3. **test_summarization_example_generates_a_helpful_summary_prompt()** — Semantic correctness

**Run:**
```bash
pytest tests/test_parser.py -v
```

---

## Future Enhancements

### Short-term
- [ ] **Multi-agent DSL:** Support defining multiple agents in one file with dependencies
- [ ] **Custom templates:** Allow users to register custom role/constraint templates
- [ ] **Import/include:** Support `#include <file>` for modular DSL files
- [ ] **Error line numbers:** Improve error messages with source file positions

### Medium-term
- [ ] **DSL compiler:** Generate Python/JSON config instead of just prompts
- [ ] **LLM integration:** Direct integration with OpenAI/Claude APIs
- [ ] **Prompt versioning:** Track and compare prompt versions

### Long-term
- [ ] **Visual DSL editor:** Drag-and-drop agent builder
- [ ] **Benchmarking suite:** Compare prompt quality across versions
- [ ] **Domain-specific extensions:** SQL, REST API, knowledge graph support

---

## Educational Value

This project demonstrates:

1. **Language Design:** How to define a DSL with clear semantics
2. **Compiler Architecture:** Lexer → Parser → AST → Codegen pipeline
3. **Parser Technology:** PLY yacc for grammar-based parsing
4. **Semantic Analysis:** Validation layer for business constraints
5. **Web UI Development:** Rapid prototyping with Streamlit
6. **Test-Driven Development:** Pytest suite validating behavior

---

## Conclusion

The **Prompt Engineering DSL** bridges the gap between ad-hoc prompt engineering and structured, reproducible AI prompt management. By treating prompts as code—with grammar, validation, and generation—we gain consistency, maintainability, and the ability to scale prompt engineering across large AI applications.

**Key Takeaway:** Domain-specific languages aren't just for compilers; they're a practical tool for managing complex, repetitive tasks in modern AI systems.

---

## Quick Reference: DSL Keywords

| Keyword | Purpose | Required? | Example |
|---------|---------|-----------|---------|
| `AGENT` | Name the AI agent | ✅ Yes | `AGENT ArticleSummarizer` |
| `ROLE` | Define agent's persona | ✅ Yes | `ROLE Summarizer` |
| `TASK` | Specify the job | ✅ Yes | `TASK Summarize article.txt` |
| `INPUT` | Reference input data/files | ❌ No | `INPUT article.txt` |
| `CONSTRAINT` | Add instructions/limitations | ❌ No | `CONSTRAINT Brief` |
| `OUTPUT` | Specify response format | ❌ No | `OUTPUT JSON` |

**Valid OUTPUT formats:** `TEXT`, `JSON`, `MARKDOWN`, `XML`

---

## Project Links

- **Repository:** [github.com/RockyRaut/Prompt-Engineering-DSL](https://github.com/RockyRaut/Prompt-Engineering-DSL)
- **Sample DSL:** `samples/example.dsl`
- **Sample Article:** `article.txt`
- **Tests:** `tests/test_parser.py`

