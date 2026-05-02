# 👑 The ShahiScript Compiler

Welcome to the **Royal Court of Computing**! 🏛️ 

ShahiScript is a fully-featured, retro-inspired compiler with an elegant Urdu/Persian theme. It was built as a final project for the **CS4031 Compiler Construction** course. Instead of writing mundane keywords, programmers issue royal decrees (`farmans`), request wealth (`daulat`), and structure logic using a regal vocabulary.

---

## ✨ Royal Features
- **📜 Full Compilation Pipeline**: Includes a custom Regex Lexer, a Recursive Descent Parser, a Scoped Semantic Analyzer, an AST Optimizer, and a Tree-Walk Interpreter.
- **🎨 The Visualizer Web App**: A stunning, royal-themed web dashboard built with Flask and D3.js. It allows you to write decrees and visualize the generated Abstract Syntax Tree (AST) dynamically!
- **⚔️ Advanced Language Rules**: 
  - Block-scoped variables with memory tracking
  - Complex conditionals (`agar`, `warna_agar`, `varna`)
  - Multi-variant loops (`har`, `jab_tak`, `dohrao`)
  - Functions (`hukam`) with scoped arguments and return statements (`waapsi`)
- **🚀 AST Optimization**: Features Dead Code Elimination and Constant Math Folding before execution.

---

## 🛠️ Quick Start (Command Line)

To issue a decree directly from your terminal, use the grand `compiler.py` executable.

```bash
# ⚔️ Execute a standard royal script
python compiler.py examples/01_hello.shahi

# 🔍 Execute a script and inspect the entire pipeline (Tokens, AST, Optimization)
python compiler.py examples/02_math_optimizer.shahi --debug

# 💬 Start the Interactive Royal Court REPL
python compiler.py --interactive
```

---

## 🌐 The Parsing Visualizer (Web Dashboard)

If you prefer a graphical view of the Royal Treasury (AST), you can launch the beautiful web interface!

1. Open your terminal and start the server:
   ```bash
   python app.py
   ```
2. Open your web browser and visit: **`http://127.0.0.1:5000`**
3. Select an example from the dropdown, hit **"Issue Decree"**, and click **"View Tree"** to explore the AST!

---

## 🏛️ Compiler Architecture (CS4031 Deliverables)

1. **Lexical Analysis** (`lexer.py`): Translates raw royal scripts into structured tokens.
2. **Syntax Analysis** (`parser.py`): A strict recursive descent parser that validates grammar and generates an Abstract Syntax Tree (AST).
3. **Semantic Analysis** (`semantic.py`): Traverses the AST to build scoped Symbol Tables and prevents unauthorized (undeclared) variables.
4. **Intermediate Optimization** (`optimizer.py`): Pre-computes constant math (e.g., `2 * 3` becomes `6`) and eliminates dead code automatically.
5. **Code Execution** (`interpreter.py`): The heart of the empire! A tree-walk interpreter that actually executes the optimized AST.

---
*Created for CS4031 Compiler Construction.* 🎓
