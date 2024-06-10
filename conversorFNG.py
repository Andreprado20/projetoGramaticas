import re
from collections import defaultdict, deque

def read_grammar(input_file):
    grammar = defaultdict(list)
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or '->' not in line:
                continue
            lhs, rhs = line.split('->')
            lhs = lhs.strip()
            rhs = rhs.strip().split('|')
            for production in rhs:
                grammar[lhs].append(production.strip())
    return grammar

def write_grammar(output_file, grammar):
    with open(output_file, 'w') as file:
        for lhs, productions in grammar.items():
            direita = ' | '.join(productions)
            file.write(f"{lhs} -> {direita}\n")

# def remove_unit_productions(grammar):
#     unit_productions = defaultdict(set)
#     for lhs, rhs_list in grammar.items():
#         for rhs in rhs_list:
#             if re.fullmatch(r'[A-Z]', rhs):
#                 unit_productions[lhs].add(rhs)
    
#     while unit_productions:
#         lhs, rhs_set = unit_productions.popitem()
#         for rhs in rhs_set:
#             if rhs in grammar:
#                 for production in grammar[rhs]:
#                     if production not in unit_productions[lhs] and production != lhs:
#                         grammar[lhs].append(production)
#                         if re.fullmatch(r'[A-Z]', production):
#                             unit_productions[lhs].add(production)
#         grammar[lhs] = [prod for prod in grammar[lhs] if not re.fullmatch(r'[A-Z]', prod)]
#     return grammar

def to_cnf(grammar):
    new_grammar = defaultdict(list)
    new_variables = {}
    counter = 1

    def get_new_variable():
        nonlocal counter
        new_var = f'X{counter}'
        counter += 1
        return new_var

    def get_variable_for_terminal(terminal):
        if terminal not in new_variables:
            new_var = get_new_variable()
            new_variables[terminal] = new_var
            new_grammar[new_var] = [terminal]
        return new_variables[terminal]

    for lhs, productions in grammar.items():
        for rhs in productions:
            if re.fullmatch(r'[a-z]', rhs):
                new_grammar[lhs].append(rhs)
            else:
                rhs_tokens = re.findall(r'[a-z]|[A-Z]+', rhs)
                new_rhs = []

                for token in rhs_tokens:
                    if re.fullmatch(r'[a-z]', token):
                        new_rhs.append(get_variable_for_terminal(token))
                    else:
                        new_rhs.append(token)

                while len(new_rhs) > 2:
                    new_var = get_new_variable()
                    new_grammar[new_var] = [new_rhs.pop(0) + new_rhs.pop(0)]
                    new_rhs.insert(0, new_var)

                new_grammar[lhs].append(''.join(new_rhs))

    return new_grammar

def eliminate_left_recursion(grammar):
    non_terminals = sorted(grammar.keys())

    for i, Ai in enumerate(non_terminals):
        for j in range(i):
            Aj = non_terminals[j]
            new_productions = []

            for rhs in grammar[Ai]:
                if rhs.startswith(Aj):
                    for Aj_rhs in grammar[Aj]:
                        new_productions.append(Aj_rhs + rhs[len(Aj):])
                else:
                    new_productions.append(rhs)

            grammar[Ai] = new_productions

        new_productions = []
        direct_recursions = []
        
        for rhs in grammar[Ai]:
            if rhs.startswith(Ai):
                direct_recursions.append(rhs[len(Ai):])
            else:
                new_productions.append(rhs)

        if direct_recursions:
            Ai_prime = f"{Ai}'"
            while Ai_prime in grammar:
                Ai_prime += "'"

            grammar[Ai] = [rhs + Ai_prime for rhs in new_productions]
            grammar[Ai_prime] = [rhs + Ai_prime for rhs in direct_recursions] + ['']

    return grammar

def to_gnf(grammar):
    grammar = eliminate_left_recursion(grammar)
    non_terminals = sorted(grammar.keys())

    for i, A in enumerate(non_terminals):
        for j in range(i):
            B = non_terminals[j]
            new_productions = []
            for rhs in grammar[A]:
                if rhs.startswith(B):
                    for B_rhs in grammar[B]:
                        new_productions.append(B_rhs + rhs[len(B):])
                else:
                    new_productions.append(rhs)
            grammar[A] = new_productions

    gnf_grammar = defaultdict(list)
    for A in non_terminals:
        for rhs in grammar[A]:
            if re.match(r'^[a-z]', rhs):
                gnf_grammar[A].append(rhs)
            else:
                new_rhs = rhs
                while not re.match(r'^[a-z]', new_rhs):
                    # Guardar o estado original do new_rhs para verificar o progresso
                    original_new_rhs = new_rhs
                    for B in non_terminals:
                        if new_rhs.startswith(B):
                            new_rhs = new_rhs.replace(B, grammar[B][0], 1)
                            break
                    # Se new_rhs não mudou, então não foi possível fazer uma substituição válida
                    if new_rhs == original_new_rhs:
                        break
                gnf_grammar[A].append(new_rhs)

    return gnf_grammar


def convert_to_gnf(input_file, output_file):
    grammar = read_grammar(input_file)
    print(grammar)
    # grammar = remove_unit_productions(grammar)
    print(grammar)
    grammar = to_cnf(grammar)
    print(grammar)
    grammar = to_gnf(grammar)
    print(grammar)
    write_grammar(output_file, grammar)

# Example usage
entrada = 'gramatica_limpa.txt'
saida = 'gramaticaLimpaNaFNG.txt'
convert_to_gnf(entrada, saida)
