import re

# Token specifications (order is important!)
token_specs = [
    ('WHITESPACE',  r'\s+'),          # Spaces, tabs, newlines (ignored)
    ('KEYWORD',     r'\b(num|text|show|true|false)\b'),
    ('LITERAL_NUM', r'\d+'),          # Inteiros # Integers
    ('LITERAL_TEXT', r'"([^"\\]|\\.)*"'),  # Strings com escape de " # Strings escaped with "
    ('OPERATOR',    r'(\+|\-|\*|/|>|<|=)'),
    ('DELIMITER',   r';'),            # Delimitador de fim de instrução
    ('IDENTIFIER',  r'[a-zA-Z_][a-zA-Z0-9!@#$%&?/|_]{0,29}'),  # Variable names
]

def lex_langb(code):
    tokens = []
    pos = 0
    while pos < len(code):
        # Try to find a pattern from the current position
        for token_type, regex in token_specs:
            pattern = re.compile(regex)
            match = pattern.match(code, pos)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':  # Ignore spaces
                    tokens.append((token_type, value))
                pos = match.end()  # Advance the position
                break
        else:
            # If no pattern was found, there is a lexical error.
            raise SyntaxError(f"Caractere inválido na posição {pos}: '{code[pos]}'")
    return tokens

# Example
code = """
show 2>2;
num a = 5;
text mensagem = "Oi!";
show mensagem;
show a;
"""

tokens = lex_langb(code)
for token in tokens:
    print(token)