## Crie *Tokens* apropriados e para cada *Token* faça uma Expressão Regular para a Linguagem *LangB*. 

| **Token**   | **Descrição**                               | **Expressão Regular (ER)**    |
| ----------- | ------------------------------------------- | ----------------------------- |
| `NUM`       | Palavra-chave para tipo numérico            | `\bnum\b`                     |
| `TEXT`      | Palavra-chave para tipo textual             | `\btext\b`                    |
| `TRUE`      | Valor lógico verdadeiro                     | `\btrue\b`                    |
| `FALSE`     | Valor lógico falso                          | `\bfalse\b`                   |
| `SHOW`      | Comando de saída                            | `\bshow\b`                    |
| `ID`        | Identificador de variável                   | `[a-zA-Z_][a-zA-Z0-9_]{0,29}` |
| `NUM_INT`   | Número inteiro                              | `[0-9]+`                      |
| `STRING`    | Cadeia de caracteres entre aspas            | `"[^"\n]*"`                   |
| `ASSIGN`    | Operador de atribuição                      | `=`                           |
| `PLUS`      | Operador soma                               | `\+`                          |
| `MINUS`     | Operador subtração                          | `-`                           |
| `TIMES`     | Operador multiplicação                      | `\*`                          |
| `DIV`       | Operador divisão                            | `/`                           |
| `GREATER`   | Operador maior que                          | `>`                           |
| `LESS`      | Operador menor que                          | `<`                           |
| `SEMICOLON` | Final de instrução                          | `;`                           |
| `INVALID`   | Caracteres inválidos                        | `[!@#\$%&\?/\|]`              |
| `SKIP`      | Espaços e tabulações (ignorar)              | `[ \t]+`                      |
| `NEWLINE`   | Quebra de linha (controle interno do lexer) | `\n`                          |
