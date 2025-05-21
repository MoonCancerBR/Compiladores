#from erPARAafn import gerar_afns_de_ers  # nome mais claro que 'do_nfa_to_dfa'
import pandas as pd
from collections import deque
from collections import defaultdict
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

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

class Estado:
    def __init__(self, nome=None, token=None): 
        self.nome = nome
        self.transicoes = defaultdict(set)
        self.epsilon = []  
        self.token = token
        
class AFN:
    def __init__(self, inicio, finais):
        self.inicio = inicio
        self.finais = finais

def converter_er_para_afn(posfixa, nome_token):
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
            fim = Estado(token=nome_token)
            inicio.transicoes[simbolo] = [fim]
            pilha.append(AFN(inicio, [fim]))

    if len(pilha) != 1:
        raise ValueError("Expressão malformada. Pilha final: ", pilha)
    # Marcar todos os finais com o token
    for estado in pilha[0].finais:
        estado.token = nome_token  

    return pilha[0]

def unir_afns(lista_afns):
    novo_inicio = Estado()
    novos_finais = []

    for afn in lista_afns:
        novo_inicio.epsilon.append(afn.inicio)
        novos_finais.extend(afn.finais)

    return AFN(novo_inicio, novos_finais)

def er_afn():
    token_specs_simplificadas = {
        'WHITESPACE':  ':*', #: ->  
        'NUM': 'num',
        'TEXT': 'text',
        'SHOW': 'show',
        'TRUE': 'true',
        'FALSE': 'false',
        'LITERAL_NUM': '~~*', #~: 0-9
        'LITERAL_TEXT': '^((l|d|s|o)*)^', # ^:" 
        'EQ': '=',
        'ADD': '+',
        'SUB': '-',
        'MUL': '´', #´: *
        'DIV': '/',
        'GT': '>',
        'LT': '<',
        'SEMICOLON': ';',
        'IDENTIFIER': 'l(l|d|e)*'
    }
    lista_afns_criados = []
    for nome, er in token_specs_simplificadas.items():
        try:
            er_posfixa = infixa_para_posfixa(er)
            afn_criado = converter_er_para_afn(er_posfixa, nome)
            lista_afns_criados.append(afn_criado)
        except Exception as e:
            print(f"{nome}: ER inválida -> {e}")
    afn_unificado = unir_afns(lista_afns_criados)
    return afn_unificado

#  _________________________________________________________________________

def epsilon_fechamento(estados):
    stack = list(estados)
    fechamento = set(estados)

    while stack:
        estado = stack.pop()
        for e in estado.epsilon:
            if e not in fechamento:
                fechamento.add(e)
                stack.append(e)

    return fechamento

def mover(estados, simbolo):
    resultado = set()
    for estado in estados:
        if simbolo in estado.transicoes:
            resultado.update(estado.transicoes[simbolo])
    return resultado

def converter_afn_para_afd(afn):
    estados_afn = set()
    alfabeto = set()
    token_afd = {}

    fila = deque([afn.inicio])
    visitados = set()

    while fila:
        atual = fila.popleft()
        if atual in visitados:
            continue
        visitados.add(atual)
        estados_afn.add(atual)
        for simbolo, destinos in atual.transicoes.items():
            alfabeto.add(simbolo)
            fila.extend(destinos)
        fila.extend(atual.epsilon)

    alfabeto = sorted(alfabeto)

    estado_inicial = frozenset(epsilon_fechamento([afn.inicio]))
    fila = deque([estado_inicial])
    afd = {}
    mapeamento_estados = {estado_inicial: "q0"}
    finais_afd = set()
    contador = 1

    while fila:
        atual = fila.popleft()
        nome_atual = mapeamento_estados[atual]
        afd[nome_atual] = {}

        for simbolo in alfabeto:
            move = mover(atual, simbolo)
            fecho = epsilon_fechamento(move)

            if not fecho:
                continue

            fecho_frozen = frozenset(fecho)
            if fecho_frozen not in mapeamento_estados:
                nome_estado = f"q{contador}"
                mapeamento_estados[fecho_frozen] = nome_estado
                fila.append(fecho_frozen)
                contador += 1
            else:
                nome_estado = mapeamento_estados[fecho_frozen]

            afd[nome_atual][simbolo] = nome_estado

    for conjunto, nome in mapeamento_estados.items():
        for estado in conjunto:
            if estado in afn.finais and estado.token:
                finais_afd.add(nome)
                if nome not in token_afd:
                    token_afd[nome] = estado.token  # ← salva o primeiro token associado
                break

    return afd, finais_afd, token_afd

# Executa a conversão
afn_unico = er_afn()
afd_resultado, finais_afd, token_afd = converter_afn_para_afd(afn_unico)

# Exibe o AFD com Pandas
print("\nAFD unificado:")
df = pd.DataFrame(afd_resultado).fillna("∅")
print(df.transpose())
print("\nEstados finais do AFD:", finais_afd)
for estado in finais_afd:
    print(f"{estado}: token → {token_afd.get(estado, '???')}")
