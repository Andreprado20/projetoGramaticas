def remove_producoes_vazias(gramatica):
    producoes_vazias = set()
    
    # Encontra os símbolos que derivam em vazio
    for simbolo, producoes in gramatica.items():
        if '' in producoes:
            producoes_vazias.add(simbolo)
    
    # Remove produções vazias
    for simbolo in producoes_vazias:
        gramatica[simbolo].remove('')
    
    # Verifica todas as produções e atualiza-as removendo símbolos que derivam em vazio
    for simbolo, producoes in gramatica.items():
        for producao in producoes:
            for vazio in producoes_vazias:
                if vazio in producao:
                    gramatica[simbolo].append(producao.replace(vazio, ''))
    
    return gramatica

def remove_producoes_unitarias(gramatica):
    producoes_unitarias = []
    
    # Encontra as produções unitárias
    for simbolo, producoes in gramatica.items():
        for producao in producoes:
            if len(producao) == 1 and producao.isupper():
                producoes_unitarias.append((simbolo, producao))
    
    # Remove produções unitárias
    for origem, destino in producoes_unitarias:
        gramatica[origem].remove(destino)
        gramatica[origem].extend(gramatica[destino])
    
    # Remove duplicatas nas produções
    for simbolo, producoes in gramatica.items():
        gramatica[simbolo] = list(set(producoes))
    
    return gramatica

def ler_gramatica_do_arquivo(nome_arquivo):
    gramatica = {}
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            simbolo, producoes = linha.strip().split(' -> ')
            gramatica[simbolo] = producoes.split(' | ')
    return gramatica

def escrever_gramatica_no_arquivo(gramatica, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for simbolo, producoes in gramatica.items():
            arquivo.write(simbolo + ' -> ' + ' | '.join(producoes) + '\n')

def limpar_gramatica(nome_arquivo_entrada, nome_arquivo_saida):
    gramatica = ler_gramatica_do_arquivo(nome_arquivo_entrada)
    gramatica = remove_producoes_vazias(gramatica)
    gramatica = remove_producoes_unitarias(gramatica)
    escrever_gramatica_no_arquivo(gramatica, nome_arquivo_saida)

# Teste
limpar_gramatica('gramatica.txt', 'gramatica_limpa.txt')
