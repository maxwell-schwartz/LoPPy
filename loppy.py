class FactTracker(object):
    def __init__(self):
        # Initialize empty dict of name: elements
        self.known_facts = {}
        # Initialize empty dict of elements: name
        self.known_elements = {}

    def update_knowledge(self, fact):
        '''Add a fact to the known facts, and elements to known elements'''
        if fact.name in self.known_facts:
            self.known_facts[fact.name].add(fact.elements)
        else:
            self.known_facts[fact.name] = set([fact.elements])

        tup_elements = tuple(fact.elements)
        if tup_elements in self.known_elements:
            self.known_elements[tup_elements].append(fact.name)
        else:
            self.known_elements[tup_elements] = [fact.name]

    def is_fact(self, fact):
        '''Return a boolean indicating whether fact is true'''
        if fact.name not in self.known_facts:
            return False
        if fact.elements in self.known_facts[fact.name]:
            return True
        else:
            return False

    def get_types(self, elements):
        '''Return known fact-types of given list of elements'''
        tup_elements = tuple(elements)
        if tup_elements in self.known_elements:
            return self.known_elements[tup_elements]
        else:
            return []

    def is_a(self, elements, type_query):
        '''Return a boolean indicating if given elements match a given type'''
        known_types = self.get_types(elements)
        if type_query in known_types:
            return True
        else:
            return False

    def solve_one(self, fact):
        '''Provide all possible values for variables in a single fact'''
        # List indices of elements that are variables and those that aren't
        knowns = [i for i, e in enumerate(fact.elements) if e[0] != '?' 
                    and e != '_']
        unknowns = [i for i, e in enumerate(fact.elements) if e[0] == '?']

        # Loop through all facts of this name
        # If all known elements match, that fact is a viable option
        for choice in self.known_facts[fact.name]:
            # Default viability to True
            viable = True
            for k in knowns:
                if choice[k] != fact.elements[k]:
                    # If known index doesn't match the choice's index,
                    # this fact isn't one of our options
                    viable = False
            # If choice is viable at the end, provide all solutions to unknowns
            if viable:
                solution = [(fact.elements[u], choice[u]) for u in unknowns]
                yield '{} = {}'.format(solution[0][0], solution[0][1])

    def solve_full(self, *args):
        '''Yield only solutions that satisfy all searched facts'''
        solutions = []
        for a in args:
            one_solved = set([])
            for s in self.solve_one(a):
                one_solved.add(s)
            solutions.append(one_solved)

        solved = set.intersection(*solutions)
        for s in solved:
            yield s


class Fact(object):
    def __init__(self, name, *args):
        self.name = name
        self.elements = args

    def get_args(self):
        print(self.name)
        print(self.elements)
