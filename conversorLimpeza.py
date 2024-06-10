class Grammar:
    def __init__(self):
        self.producoes = {}

    def adicionaProducao(self, left, right):
        if left in self.producoes:
            self.producoes[left].add(right)
        else:
            self.producoes[left] = {right}

    def read_grammar(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                left, right = line.strip().split("->")
                left = left.strip()
                right_parts = right.strip().split('|')
                for part in right_parts:
                    self.adicionaProducao(left, part.strip())

    def write_grammar(self, filename):
        with open(filename, 'w') as file:
            file.write("Saída:\n")
            for left, rights in self.producoes.items():
                rights_str = ' | '.join(rights)
                file.write(f"{left} -> {rights_str}\n")

    def remove_empty_productions(self):
        nullable = set()
        for left, rights in self.producoes.items():
            if 'ε' in rights:
                nullable.add(left)

        while True:
            new_nullable = nullable.copy()
            for left, rights in self.producoes.items():
                for right in rights:
                    if all(symbol in nullable for symbol in right):
                        new_nullable.add(left)
            if new_nullable == nullable:
                break
            nullable = new_nullable

        new_productions = {}
        for left, rights in self.producoes.items():
            new_rights = set()
            for right in rights:
                if right != 'ε':
                    new_rights.add(right)
                if any(symbol in nullable for symbol in right):
                    new_rights.update(
                        self.generate_nullable_combinations(right, nullable))
            new_productions[left] = new_rights

        self.producoes = new_productions

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
        for left, rights in self.producoes.items():
            for right in rights:
                if len(right) == 1 and right.isupper():
                    unit_pairs.add((left, right))

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
        for left, rights in self.producoes.items():
            new_rights = rights.copy()
            for (A, B) in unit_pairs:
                if A == left and B in self.producoes:
                    new_rights.update(self.producoes[B])
            new_productions[left] = {right for right in new_rights if not (
                len(right) == 1 and right.isupper())}

        self.producoes = new_productions

    def remove_useless_productions(self):
        reachable = set('S')
        while True:
            new_reachable = reachable.copy()
            for left in reachable:
                if left in self.producoes:
                    for right in self.producoes[left]:
                        new_reachable.update(
                            [symbol for symbol in right if symbol.isupper()])
            if new_reachable == reachable:
                break
            reachable = new_reachable

        useful = set()
        for left in reversed(list(self.producoes.keys())):
            if left in useful or any(symbol in useful or symbol.islower() for right in self.producoes[left] for symbol in right):
                useful.add(left)

        self.producoes = {left: rights for left, rights in self.producoes.items(
        ) if left in reachable and left in useful}
        for left in list(self.producoes.keys()):
            self.producoes[left] = {right for right in self.producoes[left] if all(
                symbol in reachable and useful or symbol.islower() for symbol in right)}


def main():
    grammar = Grammar()
    grammar.read_grammar('entrada.txt')
    # grammar.write_grammar('gramaticaOriginal.txt')
    grammar.remove_empty_productions()
    # grammar.write_grammar('gramaticaSemVazios.txt')
    grammar.remove_unit_productions()
    # grammar.write_grammar('gramaticaSemUnitarios.txt')
    grammar.remove_useless_productions()
    # grammar.write_grammar('gramaticaSemUnitarios.txt')
    grammar.write_grammar('gramatica_limpa.txt')


if __name__ == "__main__":
    main()
