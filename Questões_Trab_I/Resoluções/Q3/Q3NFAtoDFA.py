import pandas as pd

nfa = {}
n = int(input("Número de estados: "))
t = int(input("Número de símbolos de transição: "))

print("\n--- Definição do AFN ---")
for _ in range(n):
    estado = input("Nome do estado: ")
    nfa[estado] = {}
    for _ in range(t):
        simbolo = input(f" Símbolo de transição para {estado}: ")
        destinos = input(f" Estado(s) alcançado(s a partir de {estado} com '{simbolo}' (separados por espaço): ").split()
        nfa[estado][simbolo] = destinos

print("\n AFN (NFA):")
print(nfa)
print("\n Tabela do AFN:")
print(pd.DataFrame(nfa).transpose())

# Entrada dos estados finais
estados_finais_afn = input("\n Estado(s) final(is) do AFN (separados por espaço): ").split()

# Entrada do estado inicial (NOVO)
estado_inicial = input("Estado inicial do AFN: ")

# Conversão para AFD
afd = {}
fila = [frozenset([estado_inicial])]
simbolos = list(nfa[estado_inicial].keys())

while fila:
    atual = fila.pop(0)
    estado_nome = ",".join(sorted(atual))
    if estado_nome not in afd:
        afd[estado_nome] = {}
    for simbolo in simbolos:
        destinos = set()
        for estado in atual:
            destinos.update(nfa[estado].get(simbolo, []))
        destinos_fs = frozenset(destinos)
        destino_nome = ",".join(sorted(destinos_fs))
        afd[estado_nome][simbolo] = destino_nome
        if destinos_fs and destino_nome not in afd:
            fila.append(destinos_fs)

print("\n AFD (DFA):")
print(afd)
print("\n Tabela do AFD:")
print(pd.DataFrame(afd).transpose())

# Determinar estados finais do AFD
estados_finais_afd = []
for estado_composto in afd.keys():
    if any(e in estados_finais_afn for e in estado_composto.split(",")):
        estados_finais_afd.append(estado_composto)

print("\n Estados finais do AFD:", estados_finais_afd)
