# 👑 ShahiScript — The Royal Compiler

<p align="center">
  <i>A fully-featured, Urdu/Persian themed programming language and compiler, built for CS4031 Compiler Construction.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-ShahiScript-gold?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-Web%20UI-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/CS4031-Compiler%20Construction-crimson?style=for-the-badge" />
</p>

---

Welcome to the **Royal Court of Computing**! 🏛️

ShahiScript is a complete, custom-built programming language with a full compilation pipeline. Instead of ordinary keywords, programmers issue royal **decrees** (`farman`), declare **wealth** (`daulat`), and structure logic using a regal Urdu vocabulary. It comes with both a **Command-Line Interface (CLI)** and a beautiful **web-based AST visualizer**.

---

## ✨ Feature Overview

### 🔤 Language Features
| ShahiScript Keyword | Meaning | Purpose |
|---|---|---|
| `Bismillah` | In the name of God | Program start |
| `AllahHafiz` | God be with you | Program end |
| `daulat` | Wealth | Variable declaration |
| `farman` | Decree | Print / output |
| `darkhwast` | Request | User input |
| `agar` | If | Conditional |
| `warna_agar` | Else if | Else-if branch |
| `varna` | Otherwise | Else branch |
| `phir` | Then | Block opener |
| `khatam` | Finished | Block closer |
| `jab_tak` | As long as | While loop |
| `dohrao` | Repeat | Do-while loop |
| `har` | For every | For loop |
| `hukam` | Command | Function declaration |
| `waapsi` | Return | Return statement |
| `sach` / `ghalat` | True / False | Boolean literals |

### 📐 Data Types
| Keyword | Type |
|---|---|
| `adad` | Integer |
| `ashariya` | Float / Decimal |
| `jumla` | String |
| `haqeeqat` | Boolean |
| `fehrist` | Array / List |

---

## 🏛️ Compiler Architecture

ShahiScript implements a complete **5-stage compilation pipeline**:

```
Source Code (.shahi)
        │
        ▼
┌─────────────────┐
│  1. Lexer        │  lexer.py     — Regex-based tokenizer
│  (Tokenization)  │               — Handles keywords, identifiers, literals
└────────┬────────┘               — Line & column tracking for error reporting
         │
         ▼
┌─────────────────┐
│  2. Parser       │  parser.py    — Recursive Descent Parser
│  (Syntax)        │               — Produces a full JSON Abstract Syntax Tree
└────────┬────────┘               — Validates grammar via formal EBNF rules
         │
         ▼
┌─────────────────┐
│  3. Semantic     │  semantic.py  — Scoped Symbol Table (parent → child)
│     Analyzer     │               — Catches undeclared variables
└────────┬────────┘               — Validates function parameters and scopes
         │
         ▼
┌─────────────────┐
│  4. Optimizer    │  optimizer.py — Constant Math Folding (2 * 3 → 6)
│  (AST Opt.)      │               — Dead Code Elimination after return
└────────┬────────┘               — Compile-time boolean expression reduction
         │
         ▼
┌─────────────────┐
│  5. Interpreter  │  interpreter.py — Tree-walk interpreter
│  (Execution)     │                — Scoped runtime environments
└─────────────────┘                — Full function call stack with returns
```

---

## 🛠️ Quick Start (CLI)

### Prerequisites
```bash
pip install flask
```

### Running a Script
```bash
# Execute a standard royal script
python compiler.py examples/01_hello.shahi

# Execute with full pipeline debug output (Tokens, AST, Optimization, Execution)
python compiler.py examples/02_math_optimizer.shahi --debug

# Launch the Interactive REPL (type 'khatam' to exit)
python compiler.py --interactive
```

### CLI Flags
| Flag | Description |
|---|---|
| `<file>` | Path to a `.shahi` source file to execute |
| `--debug` | Print all 5 compiler phases with full output |
| `--interactive` | Launch the interactive Read-Eval-Print Loop (REPL) |

---

## 🌐 Web Visualizer (Flask + D3.js)

ShahiScript includes a royal-themed web dashboard for visually exploring the AST.

### Launch the Web App
```bash
python app.py
```
Then open your browser at **`http://127.0.0.1:5000`**

### Web UI Features
- 📋 **Example Dropdown** — Instantly load any of the 6 bundled example programs
- ▶️ **Issue Decree** — Compile and run the script right in the browser
- 🌳 **View Tree** — Render the full AST as an interactive, zoomable D3.js graph
- 📤 **Execution Output** — See the program's output directly in the UI
- 🖥️ **Two-Page Layout** — Code + I/O on Page 1, AST visualization on Page 2

---

## 📜 Example Programs

Six fully-working example scripts are included in the `examples/` folder:

| File | Demonstrates |
|---|---|
| `01_hello.shahi` | Hello World, basic output with `farman` |
| `02_math_optimizer.shahi` | Constant folding optimization at compile time |
| `03_loops.shahi` | `jab_tak` (while), `dohrao` (do-while), `har` (for) loops |
| `04_functions.shahi` | `hukam` declarations, arguments, `waapsi` (return) |
| `05_scopes.shahi` | Block-scoped variables, nested scope resolution |
| `06_interactive.shahi` | User input via `darkhwast`, string concatenation output |

### Hello World in ShahiScript
```
Bismillah
  farman "Aadaab Duniya!" ;
AllahHafiz
```

### Functions Example
```
Bismillah
  hukam jama(a, b) {
    waapsi a + b ;
  }
  daulat adad natija = jama(10, 20) ;
  farman natija ;
AllahHafiz
```

### Loops Example
```
Bismillah
  har (daulat adad i = 0 ; i < 5 ; i = i + 1) phir
    farman i ;
  khatam ;
AllahHafiz
```

---

## ⚙️ Semantic Analysis Details

The `SemanticAnalyzer` performs a **two-pass scope-aware validation**:

- **Block Scoping**: Every `agar`, `jab_tak`, `har`, and `hukam` block gets its own child `SymbolTable` that inherits from its parent.
- **Undeclared Variable Detection**: Using the `SymbolTable.lookup()` chain, any reference to an undeclared `daulat` throws a `RoyalProtocolViolation`.
- **Redeclaration Prevention**: Re-declaring a variable in the same scope raises an error immediately.
- **Function Parameter Injection**: Function parameters are injected into the function's own scope automatically.

---

## ⚡ Optimizer Details

The `Optimizer` performs two transformations on the AST **before** execution:

1. **Constant Math Folding**: Any `BinaryExpression` with two `NumberLiteral` nodes is pre-computed at compile time into a single literal. This includes `+`, `-`, `*`, `/`, `>`, `<`, `==`, `!=`.
2. **Dead Code Elimination (DCE)**: Any statements appearing after a `waapsi` (return) inside a function body are silently removed from the AST, as they can never be reached.

---

## 🚨 Error Handling

ShahiScript uses a unified `RoyalProtocolViolation` exception class (in `errors.py`) that provides:
- Clear, human-readable error messages
- Stage identification (Lexer / Semantic / Runtime)
- Line and column numbers for lexer-level errors

---

## 📁 Project Structure

```
ShahiScript/
├── compiler.py          # CLI entry point — orchestrates the full pipeline
├── lexer.py             # Regex-based tokenizer with line/column tracking
├── parser.py            # Recursive descent parser → JSON AST
├── semantic.py          # Scoped symbol table & semantic validator
├── optimizer.py         # Constant folding + dead code elimination
├── interpreter.py       # Tree-walk interpreter (runtime execution)
├── errors.py            # Unified RoyalProtocolViolation error class
├── app.py               # Flask web server for the AST visualizer
├── grammar.ebnf         # Formal EBNF grammar specification
├── Language_Reference_Manual.md  # Language reference documentation
├── examples/            # 6 example .shahi programs
│   ├── 01_hello.shahi
│   ├── 02_math_optimizer.shahi
│   ├── 03_loops.shahi
│   ├── 04_functions.shahi
│   ├── 05_scopes.shahi
│   └── 06_interactive.shahi
├── templates/           # Flask HTML templates (web UI)
└── static/              # CSS, JS, D3.js assets (web UI)
```

---

## 👥 Team

| Name | Student ID |
|---|---|
| Muhammad Zajnan Aslam | 23K0880 |
| Ali Aamir Khan | 23K0844 |
| Arsal bin Mohsin | 23K0037 |

---

*Created for **CS4031 Compiler Construction** — FAST-NUCES.* 🎓
