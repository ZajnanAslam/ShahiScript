import argparse
import sys
import json
from lexer import tokenize
from parser import parse
from semantic import analyze_semantics
from optimizer import optimize_ast
from interpreter import interpret
from errors import RoyalProtocolViolation

def execute_code(code, debug=False):
    try:
        if debug: print("\n--- [1/5] Lexical Analysis ---")
        tokens = tokenize(code)
        if debug: 
            for t in tokens: print(f"  {t.type}: {t.value}")
            
        if debug: print("\n--- [2/5] Syntax Analysis (Parsing) ---")
        ast = parse(tokens)
        if debug: print(json.dumps(ast, indent=2))
        
        if debug: print("\n--- [3/5] Semantic Analysis ---")
        analyze_semantics(ast)
        if debug: print("  Semantic check passed. Scopes and variables are valid.")
        
        if debug: print("\n--- [4/5] Optimization ---")
        ast = optimize_ast(ast)
        if debug: print("  AST Optimized (Constant folding & DCE applied).")
        
        if debug: print("\n--- [5/5] Execution Output ---\n")
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
