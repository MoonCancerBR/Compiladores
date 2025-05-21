def adicionar_concatenacoes(regex):
    resultado = ""
    operadores = set(['|', '*', '+', '?'])
    prev = ''
    for i, c in enumerate(regex):
        if prev: #prev literal ou ')', c é literal ou '('
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
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Estado:
    def __init__(self):
        self.transicoes = {}  # ex: "a": [estado1, estado2]
        self.epsilon = []     # [estadox, estadoy]

class AFN:
    def __init__(self, inicio, finais):
        self.inicio = inicio
        self.finais = finais

def converter_er_para_afn(posfixa):
    pilha = []

    for simbolo in posfixa:
        if simbolo == '*':
            afn1 = pilha.pop()
            inicio = Estado()
            fim = Estado()
            inicio.epsilon.extend([afn1.inicio, fim])
            for estado in afn1.finais:
                estado.epsilon.extend([afn1.inicio, fim])
            pilha.append(AFN(inicio, [fim]))
        elif simbolo == '.':
            afn2 = pilha.pop()
            afn1 = pilha.pop()
            for estado in afn1.finais:
                estado.epsilon.append(afn2.inicio)
            pilha.append(AFN(afn1.inicio, afn2.finais))
        elif simbolo == '|':
            afn2 = pilha.pop()
            afn1 = pilha.pop()
            inicio = Estado()
            fim = Estado()
            inicio.epsilon.extend([afn1.inicio, afn2.inicio])
            for estado in afn1.finais:
                estado.epsilon.append(fim)
            for estado in afn2.finais:
                estado.epsilon.append(fim)
            pilha.append(AFN(inicio, [fim]))
        else:
            inicio = Estado()
            fim = Estado()
            inicio.transicoes[simbolo] = [fim]
            pilha.append(AFN(inicio, [fim]))

    if len(pilha) != 1:
        raise ValueError("Expressão malformada. Pilha final: ", pilha)

    return pilha[0]

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def _main__():
    if True:
        token_specs_simplificadas = {
            'WHITESPACE':  's*',
            'KEYWORD':     'num|text|show|true|false',
            'LITERAL_NUM': 'dd*',
            'LITERAL_TEXT': 'a(l|d|s|e)*a', #erro
            'OPERATOR':    '(+|\\-|\\*|/|>|<|=)', #erro
            'DELIMITER':   ';',
            'IDENTIFIER':  'l(l|d|e)*' # e = !@#$%&?/|_ 
        }#por enquanto identificador sem limite de caracteres!!!
        lista_afns_criados = []
        for nome, er in token_specs_simplificadas.items():
            try:
                er_posfixa = infixa_para_posfixa(er)
                lista_afns_criados = converter_er_para_afn(er_posfixa)
                print(f"Infixa: {er}\n Posfixa:{er_posfixa}")
                print(f"{nome}: AFN criado com sucesso!\n\n")
            except Exception as e:
                print(f"{nome}: ER inválida -> {e}")

if __name__ == "__main__":
    _main__()
