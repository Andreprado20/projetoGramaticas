import re
from collections import defaultdict

class Grammar:
    def __init__(self):
        self.productions = defaultdict(list)
        self.non_terminals = set()
        self.start_symbol = None
    
    def add_production(self, lhs, rhs):
        self.productions[lhs].append(rhs)
        self.non_terminals.add(lhs)
    
    def read_grammar(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                lhs, rhs = line.strip().split(" -> ")
                rhs = rhs.split(" | ")
                for production in rhs:
                    self.add_production(lhs, production)
        self.start_symbol = next(iter(self.non_terminals))
    
    def write_grammar(self, file_path):
        with open(file_path, 'w') as file:
            for lhs in self.productions:
                rhs = " | ".join(self.productions[lhs])
                file.write(f"{lhs} -> {rhs}\n")

def left_recursion_elimination(grammar):
    new_productions = defaultdict(list)
    non_terminals = sorted(grammar.non_terminals)
    
    for i in range(len(non_terminals)):
        Ai = non_terminals[i]
        for j in range(i):
            Aj = non_terminals[j]
            new_rhs = []
            for production in grammar.productions[Ai]:
                if production.startswith(Aj):
                    gamma = production[len(Aj):]
                    for Aj_prod in new_productions[Aj]:
                        new_rhs.append(Aj_prod + gamma)
                else:
                    new_rhs.append(production)
            grammar.productions[Ai] = new_rhs
        
        alpha = []
        beta = []
        for production in grammar.productions[Ai]:
            if production.startswith(Ai):
                alpha.append(production[len(Ai):])
            else:
                beta.append(production)
        
        if alpha:
            Ai_prime = Ai + "'"
            grammar.non_terminals.add(Ai_prime)
            new_productions[Ai] = [b + Ai_prime for b in beta]
            new_productions[Ai_prime] = [a + Ai_prime for a in alpha] + ['']
        else:
            new_productions[Ai] = grammar.productions[Ai]
    
    grammar.productions = new_productions

def greibach_normal_form(grammar):
    non_terminals = sorted(grammar.non_terminals)
    
    for i in range(len(non_terminals)):
        Ai = non_terminals[i]
        new_productions = []
        for production in grammar.productions[Ai]:
            if production[0] in non_terminals and non_terminals.index(production[0]) < i:
                Aj = production[0]
                rest = production[1:]
                for Aj_prod in grammar.productions[Aj]:
                    new_productions.append(Aj_prod + rest)
            else:
                new_productions.append(production)
        grammar.productions[Ai] = new_productions

    for lhs in list(grammar.productions):
        new_productions = []
        for production in grammar.productions[lhs]:
            if not production[0].islower():
                raise ValueError("Transformation to GNF failed, production does not start with a terminal")
            new_productions.append(production)
        grammar.productions[lhs] = new_productions

def transform_to_greibach(file_input, file_output):
    grammar = Grammar()
    grammar.read_grammar(file_input)
    left_recursion_elimination(grammar)
    greibach_normal_form(grammar)
    grammar.write_grammar(file_output)

if __name__ == "__main__":
    input_file = 'gramatica.txt'
    output_file = 'gramaticaGreibach.txt'
    transform_to_greibach(input_file, output_file)
