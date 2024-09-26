"""
We want to write a program that consists of
1. The Wumpus World
2. A Player / Agent that has limited visibility of the world but can collect percepts
and perform logic inference.

"""
class Player:
    def __init__(self, kb):
        self.kb = kb

    def inference_by_resolution(self, query):
        """
        Perform inference by resolution on the knowledge base with respect to a query.
        """
        # Convert the KB and negated query to CNF
        clauses = self.convert_kb_to_cnf()
        negated_query = self.convert_to_cnf(('NOT', query))
        clauses.extend(negated_query)

        # Keep track of the clauses we've processed
        new_resolvents = set()
        while True:
            n = len(clauses)
            pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
            for (ci, cj) in pairs:
                resolvents = self.resolve(ci, cj)
                if [] in resolvents:
                    return True  # Empty clause found, query is true
                new_resolvents.update(frozenset(r) for r in resolvents)

            if new_resolvents.issubset(set(map(frozenset, clauses))):
                return False  # No new clauses, query is false
            clauses.extend(list(new_resolvents))

    def resolve(self, ci, cj):
        """
        Resolve two clauses and return the resulting clauses after resolution.
        """
        resolvents = []
        for di in ci:
            for dj in cj:
                if di == ('NOT', dj) or ('NOT', di) == dj:
                    resolvent = [x for x in ci if x != di] + [x for x in cj if x != dj]
                    resolvents.append(resolvent)
        return resolvents

    def convert_kb_to_cnf(self):
        """
        Convert the knowledge base to CNF.
        """
        clauses = []
        for sentence in self.kb:
            cnf_clauses = self.convert_to_cnf(sentence)
            clauses.extend(cnf_clauses)
        return clauses

    def convert_to_cnf(self, sentence):
        """
        Convert a logical sentence into Conjunctive Normal Form (CNF).
        """
        if isinstance(sentence, str):
            return [[sentence]]
        operator, *operands = sentence
        if operator == 'NOT':
            a = operands[0]
            if isinstance(a, tuple) and a[0] == 'NOT':
                return self.convert_to_cnf(a[1])  # Double negation
            return [[sentence]]  # Negated atom
        elif operator == 'AND':
            return sum([self.convert_to_cnf(op) for op in operands], [])
        elif operator == 'OR':
            clause = []
            for op in operands:
                clause.extend(self.convert_to_cnf(op)[0])
            return [clause]
        elif operator == 'IMPLIES':
            a, b = operands
            return self.convert_to_cnf(('OR', ('NOT', a), b))
        elif operator == 'IFF':
            a, b = operands
            return self.convert_to_cnf(('AND', ('IMPLIES', a, b), ('IMPLIES', b, a)))

if __name__ == '__main__':
    # Initial knowledge base
    initial_kb = [
        'P',
        ('IMPLIES', 'P', 'Q'),
        ('NOT', 'B11'),
        ('IFF', 'B11', ('OR', 'P12', 'P21'))
    ]
    player = Player(kb=initial_kb)

    
    query = 'Q'
    print("Q:", player.inference_by_resolution(query))

    
    query_not_q = ('NOT', 'Q')
    print("NOT Q:", player.inference_by_resolution(query_not_q))

    query_p21 = 'P21'
    player2 = Player(kb=initial_kb)
    print("P21:", player2.inference_by_resolution(query_p21))

    # https://chatgpt.com/share/66f598df-1e00-8013-a3e0-302e228df267
