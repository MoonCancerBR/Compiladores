class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def parse_expression(expression):
    stack = []
    current = ""
    i = 0
    
    while i < len(expression):
        char = expression[i]
        
        if char == '(':
            node = TreeNode(current.strip())
            stack.append(node)
            current = ""
            i += 1
        elif char == ')':
            if current:
                node = TreeNode(current.strip())
                stack[-1].children.append(node)
                current = ""
            
            if len(stack) > 1:
                child = stack.pop()
                stack[-1].children.append(child)
            i += 1
        elif char == ',':
            if current:
                node = TreeNode(current.strip())
                stack[-1].children.append(node)
                current = ""
            i += 1
        else:
            current += char
            i += 1
    
    if current and not stack:
        return TreeNode(current.strip())
    
    return stack[0] if stack else None

def print_tree(node, prefix="", is_last=True):
    if node is None:
        return
    
    print(prefix + ("└── " if is_last else "├── ") + node.value)
    prefix += "    " if is_last else "│   "
    
    for i, child in enumerate(node.children):
        print_tree(child, prefix, i == len(node.children) - 1)

def main():
    print("Digite a expressão desejada:")
    expression = input().strip()
    tree = parse_expression(expression)
    print("\nÁrvore de sintaxe da expressão enunciada:")
    print_tree(tree)

if __name__ == "__main__":
    main()