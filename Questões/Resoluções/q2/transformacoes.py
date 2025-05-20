import string
from automata.fa.nfa import NFA

epsilon = ''

# Gerador de nomes únicos para estados
class EstadoFactory:
    def __init__(self):
        self.count = 0

    def novo(self):
        nome = f"q{self.count}"
        self.count += 1
        return nome

estado_factory = EstadoFactory()

# AFN básico
def construir_afn_basico(simbolo):
    inicio = estado_factory.novo()
    fim = estado_factory.novo()
    transitions = {
        inicio: {simbolo: {fim}}
    }
    return NFA(
        states={inicio, fim},
        input_symbols={simbolo} if simbolo != epsilon else set(),
        transitions=transitions,
        initial_state=inicio,
        final_states={fim}
    )

# Concatenação
def concatenar_afns(afn1, afn2):
    transitions = {**afn1.transitions}
    for f in afn1.final_states:
        transitions.setdefault(f, {}).setdefault(epsilon, set()).add(afn2.initial_state)
    for estado, trans in afn2.transitions.items():
        transitions[estado] = transitions.get(estado, {})
        for simbolo, destinos in trans.items():
            transitions[estado].setdefault(simbolo, set()).update(destinos)
    return NFA(
        states=afn1.states | afn2.states,
        input_symbols=afn1.input_symbols | afn2.input_symbols,
        transitions=transitions,
        initial_state=afn1.initial_state,
        final_states=afn2.final_states
    )

# União
def unir_afns(afn1, afn2):
    novo_inicio = estado_factory.novo()
    novo_fim = estado_factory.novo()
    transitions = {
        novo_inicio: {
            epsilon: {afn1.initial_state, afn2.initial_state}
        }
    }
    for f in afn1.final_states:
        transitions.setdefault(f, {}).setdefault(epsilon, set()).add(novo_fim)
    for f in afn2.final_states:
        transitions.setdefault(f, {}).setdefault(epsilon, set()).add(novo_fim)
    for afn in [afn1, afn2]:
        for estado, trans in afn.transitions.items():
            transitions[estado] = transitions.get(estado, {})
            for simbolo, destinos in trans.items():
                transitions[estado].setdefault(simbolo, set()).update(destinos)
    return NFA(
        states=afn1.states | afn2.states | {novo_inicio, novo_fim},
        input_symbols=afn1.input_symbols | afn2.input_symbols,
        transitions=transitions,
        initial_state=novo_inicio,
        final_states={novo_fim}
    )

# Estrela de Kleene
def aplicar_estrela(afn):
    novo_inicio = estado_factory.novo()
    novo_fim = estado_factory.novo()
    transitions = {
        novo_inicio: {
            epsilon: {afn.initial_state, novo_fim}
        }
    }
    for f in afn.final_states:
        transitions.setdefault(f, {}).setdefault(epsilon, set()).update({afn.initial_state, novo_fim})
    for estado, trans in afn.transitions.items():
        transitions[estado] = transitions.get(estado, {})
        for simbolo, destinos in trans.items():
            transitions[estado].setdefault(simbolo, set()).update(destinos)
    return NFA(
        states=afn.states | {novo_inicio, novo_fim},
        input_symbols=afn.input_symbols,
        transitions=transitions,
        initial_state=novo_inicio,
        final_states={novo_fim}
    )
