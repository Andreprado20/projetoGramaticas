class Grammar:
    def __init__(self):
        self.producoes = {}

    def adicionaProducao(self, esquerda, right):
        if esquerda in self.producoes:
            self.producoes[esquerda].add(right)
        else:
            self.producoes[esquerda] = {right}

    def read_grammar(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                esquerda, right = line.strip().split("->")
                esquerda = esquerda.strip()
                right_parts = right.strip().split('|')
                for part in right_parts:
                    self.adicionaProducao(esquerda, part.strip())

    def write_grammar(self, filename):
        with open(filename, 'w') as file:
            for esquerda, rights in self.producoes.items():
                rights_str = ' | '.join(rights)
                file.write(f"{esquerda} -> {rights_str}\n")

    def remove_empty_productions(self):
        nullable = set()
        for esquerda, rights in self.producoes.items():
            if 'ε' in rights:
                nullable.add(esquerda)

        while True:
            new_nullable = nullable.copy()
            for esquerda, rights in self.producoes.items():
                for right in rights:
                    if all(symbol in nullable for symbol in right):
                        new_nullable.add(esquerda)
            if new_nullable == nullable:
                break
            nullable = new_nullable

        new_productions = {}
        for esquerda, rights in self.producoes.items():
            new_rights = set()
            for right in rights:
                if right != 'ε':
                    new_rights.add(right)
                if any(symbol in nullable for symbol in right):
                    new_rights.update(
                        self.generate_nullable_combinations(right, nullable))
            new_productions[esquerda] = new_rights

        self.producoes = new_productions
        for i in self.producoes.values():
            if '' in i: 
                i.remove('')

    def generate_nullable_combinations(self, right, nullable):
        if not right:
            return {''}
        first, rest = right[0], right[1:]
        combinations = self.generate_nullable_combinations(rest, nullable)
        if first in nullable:
            return {first + comb for comb in combinations} | combinations
        else:
            return {first + comb for comb in combinations}

    def remove_unit_productions(self):
        unit_pairs = set()
        for esquerda, rights in self.producoes.items():
            for right in rights:
                if len(right) == 1 and right.isupper():
                    unit_pairs.add((esquerda, right))

        while True:
            new_unit_pairs = unit_pairs.copy()
            for (A, B) in unit_pairs:
                if B in self.producoes:
                    for right in self.producoes[B]:
                        if len(right) == 1 and right.isupper():
                            new_unit_pairs.add((A, right))
            if new_unit_pairs == unit_pairs:
                break
            unit_pairs = new_unit_pairs

        new_productions = {}
        for esquerda, rights in self.producoes.items():
            new_rights = rights.copy()
            for (A, B) in unit_pairs:
                if A == esquerda and B in self.producoes:
                    new_rights.update(self.producoes[B])
            new_productions[esquerda] = {right for right in new_rights if not (
                len(right) == 1 and right.isupper())}

        self.producoes = new_productions

    def remove_useless_productions(self):
        reachable = set('S')
        while True:
            new_reachable = reachable.copy()
            for esquerda in reachable:
                if esquerda in self.producoes:
                    for right in self.producoes[esquerda]:
                        new_reachable.update(
                            [symbol for symbol in right if symbol.isupper()])
            if new_reachable == reachable:
                break
            reachable = new_reachable

        useful = set()
        for esquerda in reversed(list(self.producoes.keys())):
            if esquerda in useful or any(symbol in useful or symbol.islower() for right in self.producoes[esquerda] for symbol in right):
                useful.add(esquerda)

        self.producoes = {esquerda: rights for esquerda, rights in self.producoes.items(
        ) if esquerda in reachable and esquerda in useful}
        for esquerda in list(self.producoes.keys()):
            self.producoes[esquerda] = {right for right in self.producoes[esquerda] if all(
                symbol in reachable and useful or symbol.islower() for symbol in right)}


def main():    
    gramatica = Grammar()
    gramatica.read_grammar('entrada.txt')
    # grammar.write_grammar('gramaticaOriginal.txt')
    # print(grammar.producoes)
    gramatica.remove_empty_productions()
    # print(grammar.producoes)
    # grammar.write_grammar('gramaticaSemVazios.txt')
    gramatica.remove_unit_productions()
    # print(grammar.producoes)
    # grammar.write_grammar('gramaticaSemUnitarios.txt')
    gramatica.remove_useless_productions()
    # print(grammar.producoes)
    # grammar.write_grammar('gramaticaSemUnitarios.txt')
    gramatica.write_grammar('gramatica_limpa.txt')


if __name__ == "__main__":
    main()
