from juntando2e3 import  afd_resultado, finais_afd, token_afd, token_specs_simplificadas 

def simbolo_ficticio(c):
    if c.isdigit():
        return 'd'
    elif c in ' \t\n\r':
        return 's'
    elif c.isalpha():
        return 'l'
    elif c == '*':
        return 'x'
    elif c == '_':
        return 'e'
    elif c in '!@#$%&?/|' :
        return 'o'
    else: #precisa disso pra que?
        return c
    
def analisar_entrada(entrada, afd_resultado, estado_inicial, finais_afd, token_afd):
    tokens = []
    pos = 0
    while pos < len(entrada):
        estado = estado_inicial
        lexema = ''
        ultimo_token = None
        ultima_pos = pos
        i = pos

        while i < len(entrada):
            simb = simbolo_ficticio(entrada[i])
            transicoes = afd_resultado.get(estado, {})
            if simb in transicoes:
                estado = transicoes[simb]
                lexema += entrada[i]

                if estado in finais_afd:
                    ultimo_token = token_afd.get(estado)
                    ultima_pos = i + 1  # salvar a posição do último token válido
                i += 1
            else:
                break

        if ultimo_token:
            tokens.append((ultimo_token, lexema))
            pos = ultima_pos
        else:
            tokens.append(('ERRO', entrada[pos]))
            pos += 1
    return tokens

entrada = """show 2>2
num a = 5;
text mensagem = "Oi!";
show mensagem;
show a;
""" #LEMBRANDO: !@#$%&?/| só aceito quando em literalText
tokens = analisar_entrada(entrada, afd_resultado, 'q0', finais_afd, token_afd)
for token, lexema in tokens:
    print(f'{token}: "{lexema}"')
