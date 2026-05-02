from flask import Flask, request, jsonify, render_template
from lexer import tokenize
from parser import parse
from errors import RoyalProtocolViolation
import traceback
import os

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
    
    try:
        tokens = tokenize(code)
        tokens_list = [{"type": t.type, "value": t.value, "line": t.line, "col": t.column} for t in tokens]
        ast = parse(tokens)
        return jsonify({"success": True, "tokens": tokens_list, "ast": ast})
    except RoyalProtocolViolation as e:
        return jsonify({"success": False, "error": str(e), "line": e.line, "col": e.column})
    except Exception as e:
        return jsonify({"success": False, "error": f"Internal Error: {str(e)}\n{traceback.format_exc()}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
