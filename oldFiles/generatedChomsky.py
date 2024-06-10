import re
from collections import defaultdict

# Função para ler a gramática de um arquivo de texto
def ler_gramatica(filename):
    with open(filename, 'r') as file:
        producoes = defaultdict(list)
        for linha in file:
            linha = linha.strip()
            if not linha:
                continue
            lhs, rhs = linha.split('->')
            lhs = lhs.strip()
            rhs = [r.strip() for r in rhs.split('|')]
            for prod in rhs:
                producoes[lhs].append(prod.split())
    return producoes

# Função para transformar a gramática para a Forma Normal de Chomsky
def transformar_para_cnf(producoes):
    novas_producoes = defaultdict(list)
    terminais = {}
    novo_estado = 0

    # Substituir produções terminais com variáveis
    for lhs, regras in producoes.items():
        for regra in regras:
            if len(regra) == 1 and regra[0].islower():
                novas_producoes[lhs].append(regra)
            else:
                nova_regra = []
                for simbolo in regra:
                    if simbolo.islower():
                        if simbolo not in terminais:
                            novo_terminal = f"X{novo_estado}"
                            novo_estado += 1
                            terminais[simbolo] = novo_terminal
                            novas_producoes[novo_terminal].append([simbolo])
                        nova_regra.append(terminais[simbolo])
                    else:
                        nova_regra.append(simbolo)
                novas_producoes[lhs].append(nova_regra)

    # Transformar produções para forma binária
    while True:
        modificada = False
        for lhs, regras in list(novas_producoes.items()):
            for regra in regras:
                if len(regra) > 2:
                    modificada = True
                    novo_simbolo = f"X{novo_estado}"
                    novo_estado += 1
                    novas_producoes[lhs].remove(regra)
                    novas_producoes[lhs].append([regra[0], novo_simbolo])
                    novas_producoes[novo_simbolo].append(regra[1:])
                    break
            if modificada:
                break
        if not modificada:
            break

    return novas_producoes

# Função para escrever a gramática resultante em um arquivo
def escrever_gramatica(filename, producoes):
    with open(filename, 'w') as file:
        for lhs, regras in producoes.items():
            regras_str = [" ".join(regra) for regra in regras]
            file.write(f"{lhs} -> {' | '.join(regras_str)}\n")

# Função principal
def main(entrada, saida):
    producoes = ler_gramatica(entrada)
    cnf_producoes = transformar_para_cnf(producoes)
    escrever_gramatica(saida, cnf_producoes)

# Criar o arquivo de entrada
def criar_arquivo_entrada():
    conteudo = """
S -> A B | B C
A -> a A | a
B -> b B | b
C -> c C | c
"""
    with open('gramatica.txt', 'w') as file:
        file.write(conteudo.strip())

# Criar o arquivo de entrada
criar_arquivo_entrada()

# Chamando a função principal com os arquivos de entrada e saída
main('gramatica.txt', 'gramaticaChomsky.txt')
