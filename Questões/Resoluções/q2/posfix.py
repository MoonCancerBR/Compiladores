def adicionar_concatenacoes(regex):
    resultado = ""
    operadores = set(['|', '*', '+', '?'])
    prev = ''
    for i, c in enumerate(regex):
        if prev:
            # Se prev é literal ou ), e c é literal ou (
            if ((prev not in operadores and prev != '(') or prev == ')') and (c not in operadores and c != ')' or c == '('):
                resultado += '.'
        resultado += c
        prev = c
    return resultado

def infixa_para_posfixa(regex):
    regex = adicionar_concatenacoes(regex)
    precedencia = {'*': 3, '.': 2, '|': 1}
    posfixa = ''
    pilha = []

    for c in regex:
        if c == '(':
            pilha.append(c)
        elif c == ')':
            while pilha and pilha[-1] != '(':
                posfixa += pilha.pop()
            pilha.pop()  # Remove '('
        elif c in precedencia:
            while pilha and pilha[-1] != '(' and precedencia.get(pilha[-1], 0) >= precedencia[c]:
                posfixa += pilha.pop()
            pilha.append(c)
        else:
            posfixa += c

    while pilha:
        posfixa += pilha.pop()

    return posfixa
