import re
from .models import Node

def create_rule(rule_string):
    if not isinstance(rule_string, str):
        raise ValueError("Invalid rule string")

    # Tokenize the input rule string
    tokens = re.findall(r'\(|\)|\w+|[><=!]+|\band\b|\bor\b', rule_string.lower())
    
    # We’ll use a stack to handle nested parentheses and nodes
    stack = []
    current = None

    for token in tokens:
        if token == '(':  
            # Push current node to stack if starting a new sub-expression
            stack.append(current)
            current = None
        elif token == ')':  
            # Pop from stack when finishing a sub-expression
            last = current
            current = stack.pop()
            if current:
                if last:  # Attach the sub-expression as the left child of the current node
                    current.left = last
        elif token in ['and', 'or']:  
            # Create a new operator node
            operator_node = Node(type='operator', operator=token.upper())
            if current:  
                operator_node.left = current
            current = operator_node
        else:  
            # This is an operand node
            condition_node = Node(type='operand', value=token)
            if current and current.type == 'operator' and not current.right:
                current.right = condition_node
            else:
                current = condition_node  

    # Now, save the root node and its children
    def save_node(node):
        if node is None:
            return None
        if node.left:
            node.left_id = save_node(node.left)  # recursively save left subtree
        if node.right:
            node.right_id = save_node(node.right)  # recursively save right subtree
        node.save()
        return node.id

    # Start saving from the root node
    if current:
        save_node(current)
    
    return current



def combine_rules(rules):
    root = None
    for rule in rules:
        new_node = create_rule(rule)
        if root is None:
            root = new_node
        else:
            combined_node = Node(type='operator', operator='OR', left=root, right=new_node)
            combined_node.save()
            root = combined_node
    return root


def evaluate_rule(node, data):
    if node.value:
        match = re.match(r'(\w+)\s*([><=!]+)\s*(\d+|\'?\w+\'?)', node.value)
        if match:
            key, operator, value = match.groups()
            value = int(value) if value.isdigit() else value.strip("'")
            data_value = data.get(key)
            print(f"Evaluating: {key} {operator} {value} against {data_value}")
            if data_value is None:
                return False
            return {
                '>': data_value > value,
                '<': data_value < value,
                '==': data_value == value,
                '>=': data_value >= value,
                '<=': data_value <= value,
                '!=': data_value != value
            }.get(operator, False)

    left_result = evaluate_rule(node.left, data) if node.left else None
    right_result = evaluate_rule(node.right, data) if node.right else None

    if node.operator == 'AND':
        return left_result and right_result
    elif node.operator == 'OR':
        return left_result or right_result

    return False

