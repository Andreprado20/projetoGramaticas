import re
from collections import defaultdict

def read_grammar(input_file):
    grammar = defaultdict(list)
    with open(input_file, 'r') as file:
        variables = file.readline().strip().split()
        for line in file:
            line = line.strip()
            if not line or '->' not in line:
                continue
            lhs, rhs = line.split(' -> ')
            lhs = lhs.strip()
            rhs = rhs.strip().split(' | ')
            for production in rhs:
                production = production.strip().replace('ε', '')
                grammar[lhs].append(production)
    return grammar, variables

def write_grammar(output_file, grammar):
    with open(output_file, 'w') as file:
        for lhs, productions in grammar.items():
            file.write(f"{lhs} -> {' | '.join(productions)}\n")

def remove_empty_productions(grammar):
    nullable = set()
    for lhs, productions in grammar.items():
        for production in productions:
            if production == '':
                nullable.add(lhs)

    while True:
        new_nullable = set()
        for lhs, productions in grammar.items():
            for production in productions:
                if all(symbol in nullable for symbol in production):
                    new_nullable.add(lhs)
        if new_nullable <= nullable:
            break
        nullable |= new_nullable

    new_grammar = defaultdict(list)
    for lhs, productions in grammar.items():
        for production in productions:
            if production == '':
                continue
            new_grammar[lhs].append(production)
            for nullable_symbol in nullable:
                if nullable_symbol in production:
                    new_production = production.replace(nullable_symbol, '')
                    if new_production and new_production not in new_grammar[lhs]:
                        new_grammar[lhs].append(new_production)
    return new_grammar

def remove_unit_productions(grammar):
    changed = True
    while changed:
        changed = False
        for lhs in list(grammar.keys()):
            new_productions = []
            for rhs in grammar[lhs]:
                if re.fullmatch(r'[A-Za-z]', rhs) and rhs in grammar:
                    changed = True
                    new_productions.extend(grammar[rhs])
                else:
                    new_productions.append(rhs)
            if new_productions != grammar[lhs]:
                grammar[lhs] = new_productions
    return grammar

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
                rhs_tokens = re.findall(r'[a-z]|[A-Za-z]+', rhs)
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
                    for B in non_terminals:
                        if new_rhs.startswith(B):
                            new_rhs = new_rhs.replace(B, grammar[B][0], 1)
                            break
                gnf_grammar[A].append(new_rhs)

    return gnf_grammar

def convert_to_gnf(input_file, output_file):
    grammar, variables = read_grammar(input_file)
    print("Grammar read from file:", grammar)
    grammar = remove_empty_productions(grammar)
    print("After removing empty productions:", grammar)
    grammar = remove_unit_productions(grammar)
    print("After removing unit productions:", grammar)
    grammar = to_cnf(grammar)
    print("After converting to CNF:", grammar)
    grammar = to_gnf(grammar)
    print("After converting to GNF:", grammar)
    write_grammar(output_file, grammar)

# Exemplo de uso
input_file = 'gramatica2.txt'
output_file = 'output_gnf_grammar.txt'
convert_to_gnf(input_file, output_file)
