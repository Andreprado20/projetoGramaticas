


# def ler_gramatica_do_arquivo(nome_arquivo):
#     gramatica = {}
#     with open(nome_arquivo, 'r') as arquivo:
#         for linha in arquivo:
#             simbolo, producoes = linha.strip().split(' -> ')
#             gramatica[simbolo] = producoes.split('|')
#     return gramatica

# Primeiro passo: Vamos definir a função de leitura da gramática 
# passando um arquivo .txt como entrada

def leituraGramatica(nomeArquivo):
    # Após isso, vamos definir a gramatica através de 
    # um set 
    gramatica = {}

    # file = open(nomeArquivo)
    with open(nomeArquivo) as file: 
    #     return file.read()
        for line in file:
            # print(line)
            # print(type(line))
            simbolo, producoes = line.strip().split(' -> ')
            gramatica[simbolo] = producoes.split(' | ')

    # for key, value in gramatica.items():
    #     # print(dict.values(gramatica)) 
    #     print(key, "->", value)

    # gramatica.popitem()
    # for value in gramatica.items():
    #     print(value)
    # print("Gramática antes:", gramatica)

    # x = list(dict.values(gramatica))
    # # print(x)
    # # print(x[0])
    # # x[0].remove('ε')
    # print(x)
    # print(x[0])

    # for i in x:
    #     if 'ε' in i: 
    #         i.remove('ε')
    
    # print(x)
    # print(x[0])
        
    # print("Gramática depois:", gramatica)
    # print("Gramática: ", gramatica)
    return gramatica

def testsWithGrammar(gramatica):
    producoesVazias = set()

    for simbolo, producoes in gramatica.items():
        if 'ε' in producoes:
            producoesVazias.add(simbolo)

    for producao in producoesVazias:
        if 'AB' in gramatica[producao]:
            gramatica[producao].append('AB')
        print(producao, '->', gramatica[producao])

    

    print(producoesVazias)
    print(gramatica)



    return producoesVazias

# def escrever_gramatica_no_arquivo(gramatica, nome_arquivo):
#     with open(nome_arquivo, 'w') as arquivo:
#         for simbolo, producoes in gramatica.items():
#             arquivo.write(simbolo + ' -> ' + '|'.join(producoes) + '\n')


# def limpar_gramatica(nome_arquivo_entrada, nome_arquivo_saida):
#     gramatica = ler_gramatica_do_arquivo(nome_arquivo_entrada)
#     escrever_gramatica_no_arquivo(gramatica, nome_arquivo_saida)

grammar = leituraGramatica('gramatica.txt')

testsWithGrammar(grammar)

# print(leituraGramatica('gramatica.txt'))
