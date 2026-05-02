from flask import Flask, request, jsonify, render_template
from lexer import tokenize
from parser import parse
from errors import RoyalProtocolViolation
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
