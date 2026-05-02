class Optimizer:
    def optimize(self, ast):
        return self.visit(ast)

    def visit(self, node):
        if not node:
            return node
        if isinstance(node, list):
            optimized_list = []
            for n in node:
                opt_n = self.visit(n)
                if opt_n:
                    optimized_list.append(opt_n)
                if opt_n and isinstance(opt_n, dict) and opt_n.get('type') == 'Return':
                    break # Dead code elimination after return
            return optimized_list
            
        if not isinstance(node, dict):
            return node

        method_name = 'visit_' + node.get('type', '')
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        new_node = {}
        for key, value in node.items():
            new_node[key] = self.visit(value)
        return new_node

    def visit_BinaryExpression(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        
        if left.get('type') == 'NumberLiteral' and right.get('type') == 'NumberLiteral':
            op = node['operator']
            try:
                l_val = float(left['value']) if '.' in left['value'] else int(left['value'])
                r_val = float(right['value']) if '.' in right['value'] else int(right['value'])
                
                if op == '+': result = l_val + r_val
                elif op == '-': result = l_val - r_val
                elif op == '*': result = l_val * r_val
                elif op == '/': result = l_val / r_val if r_val != 0 else 0
                elif op == '>': return {"type": "BooleanLiteral", "value": "sach" if l_val > r_val else "ghalat"}
                elif op == '<': return {"type": "BooleanLiteral", "value": "sach" if l_val < r_val else "ghalat"}
                elif op == '==': return {"type": "BooleanLiteral", "value": "sach" if l_val == r_val else "ghalat"}
                elif op == '!=': return {"type": "BooleanLiteral", "value": "sach" if l_val != r_val else "ghalat"}
                else: return {"type": "BinaryExpression", "operator": op, "left": left, "right": right}
                
                return {"type": "NumberLiteral", "value": str(result)}
            except:
                pass
                
        return {"type": "BinaryExpression", "operator": node['operator'], "left": left, "right": right}

def optimize_ast(ast):
    return Optimizer().optimize(ast)
