from functools import lru_cache

# 1. Definição dos padrões da Jouette 

PATTERNS = [
    ("TEMP", ("VAR",), 0),
    ("TEMP", ("CONST",), 0),

    ("ADD", ("ADD",  "X",  "Y"), 1),
    ("MUL", ("MUL",  "X",  "Y"), 1),
    ("SUB", ("SUB",  "X",  "Y"), 1),
    ("DIV", ("DIV",  "X",  "Y"), 1),

    ("ADDI", ("ADD",  "X", ("CONST",)), 1),
    ("SUBI", ("SUB",  "X", ("CONST",)), 1),

    ("LOAD", ("LOAD", ("VAR",), ("CONST",)), 1),

    ("STORE", ("STORE", ("VAR",), ("CONST",)), 1),

    ("MOVEM", ("MOVEM", ("VAR",), ("VAR",)), 2),
]

# 2. Monta AST a partir de prefixa
class Node:
    def __init__(self, op, children=None, token=None):
        self.op = op  
        self.children = children or []
        self.token = token 

def parse_prefix(tokens):
    tok = tokens.pop(0)
    # Os números aqui são tratados como constantes
    if tok.isnumeric():
        return Node("CONST", token=tok)

    upper = tok.upper()
    # As strings aqui são tratadas como operadores binários:
    if upper in {"ADD", "MUL", "SUB", "DIV", "MOVEM"}:
        left  = parse_prefix(tokens)
        right = parse_prefix(tokens)
        return Node(upper, [left, right])

    return Node("VAR", token=tok)


# 3. Programação dinâmica para cobertura mínima
@lru_cache(None)
def cover(node):

    # I. Calcula os custos dos filhos
    filhos_info = [cover(child) for child in node.children]
    custo_filhos = sum(info[0] for info in filhos_info)

    melhor = (float('inf'), None, None)

    # II. Tenta cada padrão
    for instr, forma, custo_instr in PATTERNS:
        if forma[0] != node.op:
            continue
        if len(forma)-1 != len(node.children):
            continue
        total = custo_filhos + custo_instr
        if total < melhor[0]:
            melhor = (total, instr, filhos_info)

    if melhor[1] is None:
        raise RuntimeError(f"Sem padrão para o nó {node.op}")
    return melhor

# 4. Percorre a árvore e gera instruções
def emit(node):
    custo, instr, filhos_info = cover(node)

    for child in node.children:
        emit(child)

    print(instr)

# 5. Função principal
def main():
    linha = input("Expressão em prefixa: ").strip()
    tokens = linha.split()
    ast = parse_prefix(tokens)
    total, _, _ = cover(ast)
    print("Instruções geradas (padrões selecionados):")
    emit(ast)
    print(f"Custo total: {total}")

if __name__ == "__main__":
    main()
