import re

# Dicionário de padrões de tokens para as regexs
tokens_specs = [
    ('NUM',       r'\bnum\b'),           
    ('TEXT',      r'\btext\b'),          
    ('VAR',       r'\b[a-zA-Z_]\w*\b'),  
    ('NUMBER',    r'\b\d+\b'),           
    ('EQ',        r'='),
    ('ADD',       r'\+'),
    ('CONST',     r'"[^"]*"'),           
    ('SEMICOLON', r';'),
    ('SKIP',      r'[ \t]+'),             
    ('NEWLINE',   r'\n'),                 
    ('MISMATCH',  r'.'),                 
]

tokens_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens_specs)

def lexer(langb_programa):
    tokens = []
    for mo in re.finditer(tokens_regex, langb_programa):
        tipo = mo.lastgroup
        if tipo in ('SKIP', 'NEWLINE'):
            continue
        elif tipo == 'MISMATCH':
            return ['ERRO']
        if tipo == 'NUMBER':
            tipo = 'NUM'
        tokens.append(tipo)
    return tokens

# Entrada de dados
print("Digite seu código em LangB. Ao finalizar, pressione Enter duas vezes:")
linhas = []
while True:
    linha = input()
    if linha.strip() == '':
        break
    linhas.append(linha)

for linha in linhas:
    resultado = lexer(linha)
    print(' '.join(resultado))