import argparse
import sys
import json
from Phase1_Lexical.lexer import tokenize
from Phase2_Syntax.parser import parse
from Phase3_Semantic.semantic import analyze_semantics
from Phase4_ICG.icg import generate_icg
from Phase5_Optimization.optimizer import optimize_ast
from Phase6_CodeGeneration.codegen import generate_target_code
from Interpreter.interpreter import interpret
from errors import RoyalProtocolViolation

def execute_code(code, debug=False):
    try:
        if debug: print("\n--- [1/6] Lexical Analysis ---")
        tokens = tokenize(code)
        if debug: 
            for t in tokens: print(f"  {t.type}: {t.value}")
            
        if debug: print("\n--- [2/6] Syntax Analysis (Parsing) ---")
        ast = parse(tokens)
        if debug: print(json.dumps(ast, indent=2))
        
        if debug: print("\n--- [3/6] Semantic Analysis ---")
        analyze_semantics(ast)
        if debug: print("  Semantic check passed. Scopes and variables are valid.")

        if debug: print("\n--- [4/6] Intermediate Code Generation ---")
        tac = generate_icg(ast)
        if debug: 
            for line in tac: print(f"  {line}")
        
        if debug: print("\n--- [5/6] Optimization ---")
        ast = optimize_ast(ast)
        if debug: print("  AST Optimized (Constant folding, DCE, Algebraic Simplification).")

        if debug: print("\n--- [6/6] Target Code Generation ---")
        asm = generate_target_code(ast)
        if debug:
            for line in asm: print(f"  {line}")
        
        if debug: print("\n--- Execution Output ---\n")
        interpret(ast)
        
    except RoyalProtocolViolation as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\nInternal Compiler Error: {e}")

def repl():
    print("ShahiScript Interactive REPL")
    print("Type 'khatam' to exit.")
    while True:
        try:
            line = input("shahi> ")
            if line.strip() == "khatam":
                break
            code = f"Bismillah\n{line}\nAllahHafiz"
            execute_code(code)
        except KeyboardInterrupt:
            break
        except EOFError:
            break

def main():
    parser = argparse.ArgumentParser(description="ShahiScript Compiler")
    parser.add_argument("file", nargs="?", help="Source file to compile (.shahi)")
    parser.add_argument("--debug", action="store_true", help="Print all compiler phases output")
    parser.add_argument("--interactive", action="store_true", help="Start the interactive REPL")
    
    args = parser.parse_args()
    
    if args.interactive:
        repl()
    elif args.file:
        with open(args.file, 'r') as f:
            code = f.read()
        execute_code(code, debug=args.debug)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
