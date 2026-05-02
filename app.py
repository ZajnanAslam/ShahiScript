from flask import Flask, request, jsonify, render_template
from lexer import tokenize
from parser import parse
from semantic import analyze_semantics
from optimizer import optimize_ast
from interpreter import interpret
from errors import RoyalProtocolViolation
import traceback
import os
import sys
import io
import builtins

app = Flask(__name__)

@app.route('/')
def index():
    examples = {}
    examples_dir = 'examples'
    if os.path.exists(examples_dir):
        for filename in sorted(os.listdir(examples_dir)):
            if filename.endswith('.shahi'):
                with open(os.path.join(examples_dir, filename), 'r', encoding='utf-8') as f:
                    examples[filename] = f.read()
    return render_template('index.html', examples=examples)

@app.route('/parse', methods=['POST'])
def parse_code():
    data = request.json
    code = data.get('code', '')
    stdin_str = data.get('stdin', '')
    
    try:
        tokens = tokenize(code)
        tokens_list = [{"type": t.type, "value": t.value, "line": t.line, "col": t.column} for t in tokens]
        ast = parse(tokens)
        
        analyze_semantics(ast)
        opt_ast = optimize_ast(ast)
        
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        old_input = builtins.input
        
        input_lines = stdin_str.replace('\r\n', '\n').split('\n')
        input_iter = iter(input_lines)
        
        def mock_input(prompt=""):
            print(prompt, end="")
            try:
                val = next(input_iter)
                print(val)
                return val
            except StopIteration:
                return ""
                
        builtins.input = mock_input
        
        try:
            interpret(opt_ast)
        finally:
            sys.stdout = old_stdout
            builtins.input = old_input
            
        output = new_stdout.getvalue()
        
        return jsonify({"success": True, "tokens": tokens_list, "ast": opt_ast, "output": output})
    except RoyalProtocolViolation as e:
        return jsonify({"success": False, "error": str(e), "line": e.line, "col": e.column})
    except Exception as e:
        return jsonify({"success": False, "error": f"Internal Error: {str(e)}\n{traceback.format_exc()}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
