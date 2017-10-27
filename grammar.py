import loppy as lp

def is_np(knowledge, elements):
    '''Determine if a given set of words is a Noun Phrase'''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'NOUN'):
        return True, ['NOUN']
    head, *tail = elements
    if knowledge.is_a([head], 'ADJ'):
        truth, pos_list = is_np(knowledge, tail)
        return truth, ['ADJ'] + pos_list
    return False, []

def main():
    # Test
    knowledge = lp.FactTracker()
    knowledge.update_knowledge(lp.Fact('NOUN', 'dog'))
    knowledge.update_knowledge(lp.Fact('NOUN', 'cat'))
    knowledge.update_knowledge(lp.Fact('ADJ', 'small'))
    knowledge.update_knowledge(lp.Fact('ADJ', 'blue'))

    print(is_np(knowledge, 'small dog'.split()))
    print(is_np(knowledge, 'small blue small dog'.split()))
    print(is_np(knowledge, 'cat'.split()))
    print(is_np(knowledge, 'small blue'.split()))

if __name__ == '__main__':
    main()