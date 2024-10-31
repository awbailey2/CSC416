import re

def parse_sentence(sentence):
    # Match the predicate and terms within parentheses
    match = re.match(r"(\w+)\((.+)\)", sentence)
    if match:
        predicate = match.group(1)
        terms = match.group(2).split(', ')
        return predicate, terms
    else:
        raise ValueError("Invalid sentence format")

def unify(sentence1, sentence2):
    predicate1, terms1 = parse_sentence(sentence1)
    predicate2, terms2 = parse_sentence(sentence2)
    
    
    if predicate1 != predicate2 or len(terms1) != len(terms2):
        return {}
    
    substitutions = {}
    for term1, term2 in zip(terms1, terms2):
        result = unify_terms(term1, term2, substitutions)
        if result is None:
            return {}
        substitutions.update(result)
        
    return substitutions

def unify_terms(term1, term2, subs):
    
    term1 = subs.get(term1, term1)
    term2 = subs.get(term2, term2)
    
    if term1 == term2:
        return subs
    
    # Check if term is a variable
    if is_variable(term1):
        subs[term1] = term2
        return subs
    elif is_variable(term2):
        subs[term2] = term1
        return subs
    
    # Handle compound terms
    if '(' in term1 and '(' in term2:
        return unify(term1, term2)
    
    return None  

def is_variable(term):
    return term.islower() and not '(' in term  


print(unify('Parent(x, y)', 'Parent(John, Mary)'))  # {'x': 'John', 'y': 'Mary'}
print(unify('Loves(father(x), x)', 'Loves(father(John), John)'))  # {'x': 'John'}
print(unify('Parent(x, x)', 'Parent(John, Mary)'))  # {}

def negate_clause(clause):
    return clause[1:] if clause.startswith('¬') else f"¬{clause}"

def resolve(clause1, clause2):
    set1 = set(clause1)
    set2 = set(clause2)

    resolvable_literal = None
    for literal in set1:
        if literal.startswith('¬'):
            complement = literal[1:]
        else:
            complement = '¬' + literal
        
        if complement in set2:
            resolvable_literal = literal
            break

    if not resolvable_literal:
        return set()

    resolved_clause = (set1 | set2) - {resolvable_literal, complement}
    return list(resolved_clause)






def inference_by_resolution(kb, query):
    kb = [set(clause) for clause in kb]  # Convert clauses to sets for easier manipulation
    negated_query = [negate_clause(query)]
    kb.append(set(negated_query))
    
    new_clauses = set()
    
    while True:
        pairs = [(kb[i], kb[j]) for i in range(len(kb)) for j in range(i + 1, len(kb))]
        
        for (clause1, clause2) in pairs:
            resolvent = resolve(clause1, clause2)
            if resolvent == set():
                return True 
            new_clauses.add(frozenset(resolvent))
        
        if new_clauses.issubset(kb):
            return False  
        kb.extend(new_clauses - set(kb))


kb = [
    ['¬King(x)', '¬Greedy(x)', 'Evil(x)'],
    ['King(John)'],
    ['Greedy(x)']
]
query = 'Evil(John)'
print(inference_by_resolution(kb, query))  # Expected output: True

# https://chatgpt.com/share/6723cbcd-57d8-8013-b178-ec02d893cd33