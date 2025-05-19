## Tokens da Linguagem LangB
| **Token**        | **Descrição**                                           | **Regex**                                                     |
|------------------|---------------------------------------------------------|---------------------------------------------------------------|
| `KEYWORD`        | Palavras-chave (`num`, `text`, `show`, `true`, `false`) | `\b(num \| text \| show \| true \| false)\b`                  |
| `IDENTIFIER`     | Nome de variável (até 30 caracteres)                    | `[a-zA-Z_][a-zA-Z0-9!@#$%&?/\|_]{0,29}`                       |
| `NUMBER`         | Inteiros (ex: `42`)                                     | `\d+`                                                         |
| `STRING`         | Texto entre aspas (ex: `"Olá!"`)                        | `"([^"\\] \| \\.)*"`                                          |
| `OPERATOR`       | Operadores (`+`, `-`, `*`, `/`, `>`, `<`, `=`)          | `( \+ \| \- \| \* \| / \| > \| < \| = )`                      |
| `SEMICOLON`      | Delimitador `;`                                         | `;`                                                           |
| `WHITESPACE`     | Espaços, tabs, novas linhas                             | `\s+`                                                         |
