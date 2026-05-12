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

ShahiScript is a complete, custom-built programming language with a full **6-phase compilation pipeline**. Instead of ordinary keywords, programmers issue royal **decrees** (`farman`), declare **wealth** (`daulat`), and structure logic using a regal Urdu vocabulary. It comes with both a **Command-Line Interface (CLI)** and a beautiful **web-based AST visualizer**.

---

## 👥 Team Member Contributions

- **[Member 1 Name - ID]** - Phase 1 (Lexical), Phase 2 (Syntax), Integration Testing
- **[Member 2 Name - ID]** - Phase 3 (Semantic), Phase 4 (ICG), Target Code Gen
- **[Member 3 Name - ID]** - Phase 5 (Optimization), Visualizer Dashboard, Documentation

---

## ✨ Language Features

### 🔤 Keywords
| ShahiScript Keyword | Meaning | Purpose |
|---|---|---|
| `Bismillah` | In the name of God | Program start |
| `AllahHafiz` | God be with you | Program end |
| `daulat` | Wealth | Variable declaration |
| `farman` | Decree | Print / output |
| `darkhwast` | Request | User input |
| `agar` / `phir` / `khatam` | If / Then / End | Conditionals |
| `jab_tak` | As long as | While loop |
| `har` | For every | For loop |
| `hukam` / `waapsi` | Command / Return | Functions |

### 📐 Data Types
- `adad` (Integer), `ashariya` (Float), `jumla` (String), `haqeeqat` (Boolean), `fehrist` (Array).

---

## 🏛️ Compiler Architecture (CS4031 Deliverables)

ShahiScript implements a complete **6-stage compilation pipeline** to meet all course requirements:

1. **Lexical Analysis** (`Phase1_Lexical/lexer.py`): Regex-based tokenizer with line/column tracking.
2. **Syntax Analysis** (`Phase2_Syntax/parser.py`): Recursive Descent Parser producing a JSON AST.
3. **Semantic Analysis** (`Phase3_Semantic/semantic.py`): Scoped Symbol Table and variable validation.
4. **Intermediate Code Gen** (`Phase4_ICG/icg.py`): Generates **Three Address Code (TAC)**.
5. **Optimization** (`Phase5_Optimization/optimizer.py`): Constant Folding, DCE, and Algebraic Simplification.
6. **Target Code Gen** (`Phase6_CodeGeneration/codegen.py`): Generates **Stack Machine Assembly**.

---

## 🛠️ Individual Phase Execution (Mandatory)

Each phase can be executed independently from the root directory:

| Phase | Command | Output |
|-------|---------|--------|
| **1. Lexical** | `python Phase1_Lexical/lexer.py TestCases/01_hello.shahi` | Tokens |
| **2. Syntax** | `python Phase2_Syntax/parser.py TestCases/01_hello.shahi` | AST (JSON) |
| **3. Semantic** | `python Phase3_Semantic/semantic.py TestCases/01_hello.shahi` | Semantic Check |
| **4. ICG** | `python Phase4_ICG/icg.py TestCases/01_hello.shahi` | TAC |
| **5. Optimization** | `python Phase5_Optimization/optimizer.py TestCases/01_hello.shahi` | Optimized AST |
| **6. Code Gen** | `python Phase6_CodeGeneration/codegen.py TestCases/01_hello.shahi` | Stack ASM |

---

## 🚀 Complete Compiler Execution

```bash
# Execute a standard royal script
python compiler.py TestCases/01_hello.shahi

# Execute with full pipeline debug output
python compiler.py TestCases/02_math_optimizer.shahi --debug

# Launch the Interactive REPL
python compiler.py --interactive
```

---

## 🌐 Web Visualizer (Flask + D3.js)

Launch the web app to visualize the AST dynamically:
```bash
python app.py
```
Visit **`http://127.0.0.1:5000`** to see:
- 🌳 **Interactive AST Tree** (Zoomable D3.js graph)
- ▶️ **Live Execution** of royal decrees
- 📋 **Example Library** for quick testing

---

## 📸 Screenshots & Outputs

> [!IMPORTANT]
> Please include your actual screenshots here for the final submission.

1. **Tokens Output**: Phase 1 console screenshot.
2. **AST Visualization**: Web Dashboard `View Tree` screenshot.
3. **TAC & Assembly**: Phase 4 and Phase 6 console output.
4. **Final Execution**: Output of a complex test case.

---

## 📁 Project Structure

```text
ShahiScript/
├── Phase1_Lexical/       # Tokenization
├── Phase2_Syntax/        # Parsing
├── Phase3_Semantic/      # Scoping & Symbols
├── Phase4_ICG/           # Intermediate Code (TAC)
├── Phase5_Optimization/  # Code Optimization
├── Phase6_CodeGeneration/# Target Code (Assembly)
├── Interpreter/          # Tree-Walk Runtime
├── TestCases/            # .shahi test scripts
├── Documentation/        # Manuals & Grammar
├── app.py                # Web Server
├── compiler.py           # CLI Main
└── README.md             # This Document
```

---
*Created for **CS4031 Compiler Construction** — FAST-NUCES.* 🎓
