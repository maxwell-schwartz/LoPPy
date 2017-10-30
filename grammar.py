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

def is_dp(knowledge, elements):
    '''Determine if a given set of words in a Determiner Phrase'''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'DET'):
        truth, pos_list = is_np(knowledge, tail)
        return truth, ['DET'] + pos_list
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

def is_dp_with_advp(knowledge, elements):
    '''
    Determine if given set of words is a Noun Phrase followed by a series of Adverbs
    This is a potential component of Transitive Verb Phrases
    '''
    if len(elements) < 2:
        return False, []
    head, *tail = elements
    head = [head]
    while tail:
        dp_truth, dp_pos = is_dp(knowledge, head)
        advp_truth, advp_pos = is_advp(knowledge, tail)
        if dp_truth and advp_truth:
            return True, dp_pos + advp_pos
        new_head, *tail = tail
        head += [new_head]
    return False, []

def is_int_vp(knowledge, elements):
    '''Determine if a given set of words is an Intransitive Verb Phrase'''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'INT_VERB'):
        # A lone verb works
        return True, ['INT_VERB']
    head, *tail = elements
    if knowledge.is_a([head], 'INT_VERB'):
        # A verb followed by any number of adverbs works
        truth, pos_list = is_advp(knowledge, tail)
        return truth, ['INT_VERB'] + pos_list
    elif knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_int_vp(knowledge, tail)
        return truth, ['ADV'] + pos_list
    return False, []

def is_tr_vp(knowledge, elements):
    '''Determine if given set of words is a Transitive Verb Phrase'''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'TR_VERB'):
        # Check if words following the transitive verb are an NP or an NP+ADVP
        dp_truth, dp_pos_list = is_dp(knowledge, tail)
        dp_advp_truth, dp_advp_pos_list = is_dp_with_advp(knowledge, tail)
        if dp_truth:
            return True, ['TR_VERB'] + dp_pos_list
        elif dp_advp_truth:
            return True, ['TR_VERB'] + dp_advp_pos_list
    elif knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_tr_vp(knowledge, tail)
        return truth, ['ADV'] + pos_list
    return False, []

def is_vp(knowledge, elements):
    '''Determine if given set of words is any type of Verb Phrase'''
    tr_truth, tr_pos = is_tr_vp(knowledge, elements)
    int_truth, int_pos = is_int_vp(knowledge, elements)
    if tr_truth:
        return tr_truth, tr_pos
    elif int_truth:
        return int_truth, int_pos
    return False, []

def is_sub_clause(knowledge, elements):
    '''Determine if given set of words is a Subclause'''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    head = [head]
    if knowledge.is_a(head, 'C-MARKER'):
        truth, pos_list = is_vp(knowledge, tail)
        if truth:
            return truth, ['C-MARKER'] + pos_list
        head, *tail = tail
        head = [head]
        while tail:
            vp_truth, vp_pos = is_vp(knowledge, head)
            sub_truth, sub_pos = is_sub_clause(knowledge, tail)
            if vp_truth and sub_truth:
                return True, ['C-MARKER'] + vp_pos + sub_pos
            new_head, *tail = tail
            head += [new_head]
    return False, []

def is_sentence(knowledge, elements):
    '''Determin if given set of words is a grammatical sentence'''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    head = [head]
    while tail:
        subj_truth, subj_pos = is_dp(knowledge, head)
        pred_truth, pred_pos = is_vp(knowledge, tail)
        if subj_truth and pred_truth:
            return True, subj_pos + pred_pos
        new_head, *tail = tail
        head += [new_head] 
    return False, []

def main():
    # Test
    knowledge = lp.FactTracker()
    with open('word_lists/nouns.txt', 'r') as infile:
        nouns = infile.readlines()
    with open('word_lists/transitive_verbs.txt', 'r') as infile:
        tr_verbs = infile.readlines()
    with open('word_lists/intransitive_verbs.txt', 'r') as infile:
        int_verbs = infile.readlines()
    with open('word_lists/adjectives.txt', 'r') as infile:
        adjectives = infile.readlines()
    with open('word_lists/adverbs.txt', 'r') as infile:
        adverbs = infile.readlines()
    with open('word_lists/determiners.txt', 'r') as infile:
        determiners = infile.readlines()
    with open('word_lists/clause_markers.txt', 'r') as infile:
        c_markers = infile.readlines()

    for n in nouns:
        knowledge.update_knowledge(lp.Fact('NOUN', n.strip()))
    for t in tr_verbs:
        knowledge.update_knowledge(lp.Fact('TR_VERB', t.strip()))
    for i in int_verbs:
        knowledge.update_knowledge(lp.Fact('INT_VERB', i.strip()))
    for a in adjectives:
        knowledge.update_knowledge(lp.Fact('ADJ', a.strip()))
    for ad in adverbs:
        knowledge.update_knowledge(lp.Fact('ADV', ad.strip()))
    for d in determiners:
        knowledge.update_knowledge(lp.Fact('DET', d.strip()))
    for c in c_markers:
        knowledge.update_knowledge(lp.Fact('C-MARKER', c.strip()))

    keep_going = 'y'
    while keep_going == 'y':
        user_sent = input('Enter sentence >> ').split()
        # print('NP > ', is_np(knowledge, user_sent))
        # print('INT_VP > ', is_int_vp(knowledge, user_sent))
        # print('TR_VP > ', is_tr_vp(knowledge, user_sent))
        # print('ADVP > ', is_advp(knowledge, user_sent))
        # print('DP + ADVP > ', is_dp_with_advp(knowledge, user_sent))
        # print('DP > ', is_dp(knowledge, user_sent))
        print('Subclause > ', is_sub_clause(knowledge, user_sent))
        # print('SENTENCE > ', is_sentence(knowledge, user_sent))
        keep_going = input('Continue? (y/n) ')

if __name__ == '__main__':
    main()