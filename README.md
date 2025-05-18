# Compiladores
Trabalho colaborativo pra conclusão da disciplina de Compiladores 2025.1 - UFC/Qx

A *LangB* é uma linguagem minimalista e estruturada inspirada na *Linguagem C*, com regras claras e sintaxe simplificada para facilitar o aprendizado e a implementação de compiladores. 
O alfabeto da linguagem é formado por números, letras do alfabeto português (sem acentuação), os caracteres reservados da linguagem além dos símbolos: `! @ # $ % & ? / _ |`

## Características da *LangB*:

### 1. Tipos de Dados

Apenas dois tipos são suportados:
 * num (equivalente a int para números inteiros).
 * text (equivalente a string para cadeias de caracteres).
 * true.
 * false.

### 2. Operadores Suportados

* Operações matemáticas básicas: `+`, `-`, `*`, `/`
* Operadores de comparação: `>`, `<`
* Operador de atribuição: `=`
* **Não** Não há operadores bit a bit.

### 3. Estrutura do Código

* Cada instrução deve terminar com `;`
* Declaração de variáveis segue o formato:

  ```langb
  num x = 10;
  text y = "hello";
  ```
* Nome de variáveis devem ter tamanho de no máximo 30 caracteres e **não podem** iniciar com seguintes caracteres:  `! @ # $ % & ? / |`

* **Não há funções, blocos de código ou estruturas de controle** como loops e condicionais.

### 4. Entrada e Saída

* A única forma de saída é a instrução `show`, que exibe o valor de uma variável:

  ```langb
  show x;
  show y;
  ```
* **Não há entrada de dados ou interação com o usuário.**

### 5. Ausências na Linguagem

* Não há estruturas de repetição (`for`, `while`)
* Não há condicionais (`if`, `else`)
* Não há funções ou modularização.
* Não há suporte para bibliotecas externas ou importação de código.
* Não há ponteiros ou gerenciamento avançado de memória.

---

## Exemplo de Código em *LangB*

```langb
show 2 > 2
num a = 5;
text mensagem = "Oi!";
show mensagem;
show a;
```

### Saída Esperada

```
false
Oi
5
```
---
Essa linguagem mantém a estrutura do C, mas com palavras-chave simplificadas para tornar sua compreensão mais acessível.

##  Opção 1 – Análise Léxica

### Etapas do Projeto

1. (2,0 pontos) Crie Tokens apropriados e para cada Token faça uma Expressão Regular 
para a Linguagem *LangB*.

2. (2,0 pontos) Implemente um algoritmo que recebe como entrada todas as Expressões 
Regulares da Questão anterior e retorna um único Autômato Finito Não-Determinístico 
(NFA).

3. (3,0 pontos) Implemente um algoritmo que recebe como entrada um Autômato Finito 
Não-Determinístico (NFA) e retorna um Autômato Finito Determinístico (DFA). A 
forma de representação dos Autômatos é livre, ou seja, você pode representá-los como 
matriz, lista, dicionário etc.

4. (3,0 pontos) Utilizando o DFA da Questão 3, implemente um analisador léxico  para a 
Linguagem *LangB*. Além do código, é preciso entregar um arquivo .txt contendo a lista 
de tokens utilizados e o que eles representam. O arquivo tem o seguinte formato: cada 
linha contém duas informações separadas por espaço, sendo a primeira posição o token 
e a segunda o que ele representa. Se o token representa mais de uma entidade, separe-os 
por vírgula.

### Entrada

* A entrada é composta por um código fonte de um programa qualquer escrito em LangB.

### Saída

* Para cada entrada, seu programa deve produzir uma sequência de Tokens ou a palavra 
`ERRO`, caso a entrada tenha erro léxico

### Exemplo

#### Entrada

```langb
int a = 0 ;
int b = 5 + a ;
text c = “teSte” ;
```

#### Saída

```
INT VAR EQ NUM SEMICOLON
INT VAR EQ NUM ADD VAR SEMICOLON
TEXT VAR EQ CONST SEMICOLON
```

---

