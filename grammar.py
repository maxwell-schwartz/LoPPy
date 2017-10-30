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

def is_advp(knowledge, elements):
    '''Determing if given set of words is a series of Adverbs'''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'ADV'):
        return True, ['ADV']
    head, *tail = elements
    if knowledge.is_a([head], 'ADV'):
        truth, pos_list = is_advp(knowledge, tail)
        return truth, ['ADV'] + pos_list
    return False, []

def is_int_vp(knowledge, elements):
    '''Determine if a given set of words is a Verb Phrase'''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'INT_VERB'):
        return True, ['INT_VERB']
    head, *tail = elements
    if knowledge.is_a([head], 'INT_VERB'):
        truth, pos_list = is_advp(knowledge, tail)
        return truth, ['INT_VERB'] + pos_list
    elif knowledge.is_a([head], 'ADV'):
        truth, pos_list = is_int_vp(knowledge, tail)
        return truth, ['ADV'] + pos_list
    return False, []

def is_sentence(knowledge, elements):
    '''Determin if given set of words is a grammatical sentence'''

    if len(elements) < 2:
        return False, []
    else:
        head, *tail = elements
        head = [head]
        while tail:
            subj_truth, subj_pos = is_np(knowledge, head)
            pred_truth, pred_pos = is_int_vp(knowledge, tail)
            if subj_truth and pred_truth:
                return True, subj_pos + pred_pos
            new_head, *tail = tail
            head += [new_head] 
    return False, []

def main():
    # Test
    knowledge = lp.FactTracker()
    knowledge.update_knowledge(lp.Fact('NOUN', 'dog'))
    knowledge.update_knowledge(lp.Fact('NOUN', 'cat'))
    knowledge.update_knowledge(lp.Fact('ADJ', 'small'))
    knowledge.update_knowledge(lp.Fact('ADJ', 'blue'))
    knowledge.update_knowledge(lp.Fact('INT_VERB', 'dances'))
    knowledge.update_knowledge(lp.Fact('ADV', 'quickly'))
    knowledge.update_knowledge(lp.Fact('ADV', 'often'))

    keep_going = 'y'
    while keep_going == 'y':
        user_sent = input('Enter sentence >> ').split()
        # print('NP > ', is_np(knowledge, user_sent))
        # print('INT_VP > ', is_int_vp(knowledge, user_sent))
        # print('ADVP > ', is_advp(knowledge, user_sent))
        print('SENTENCE > ', is_sentence(knowledge, user_sent))
        keep_going = input('Continue? (y/n) ')

    # print(is_np(knowledge, 'small dog'.split()))
    # print(is_np(knowledge, 'small blue small dog'.split()))
    # print(is_np(knowledge, 'cat'.split()))
    # print(is_np(knowledge, 'small blue'.split()))

if __name__ == '__main__':
    main()