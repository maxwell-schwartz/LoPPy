import loppy as lp

def is_np_s(knowledge, elements):
    '''
    Determine if a given set of words is a Singular Noun Phrase
    e.g. "small blue dog"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'NOUN_S'):
        return True, ['NOUN_S']
    head, *tail = elements
    if knowledge.is_a([head], 'ADJ'):
        truth, pos_list = is_np_s(knowledge, tail)
        return truth, ['ADJ'] + pos_list
    return False, []

def is_dp_s(knowledge, elements):
    '''
    Determine if a given set of words in a Singular Determiner Phrase
    e.g. "the small blue dog"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'DET'):
        truth, pos_list = is_np_s(knowledge, tail)
        return truth, ['DET'] + pos_list
    return False, []

def is_advp(knowledge, elements):
    '''
    Determing if given set of words is a series of Adverbs
    e.g. "often quickly"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'ADV'):
        return True, ['ADV']
    head, *tail = elements
    if knowledge.is_a([head], 'ADV'):
        truth, pos_list = is_advp(knowledge, tail)
        return truth, ['ADV'] + pos_list
    return False, []

def is_int_vp_3(knowledge, elements):
    '''
    Determine if a given set of words is a 3rd Person Intransitive Verb Phrase
    e.g. "often sleeps"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'INT_VERB'):
        # A lone verb works
        return True, ['INT_VERB']
    head, *tail = elements
    if knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_int_vp_3(knowledge, tail)
        return truth, ['ADV'] + pos_list
    return False, []

def is_tr_vp_3(knowledge, elements):
    '''
    Determine if given set of words is a 3rd Person Transitive Verb Phrase
    e.g. "throws the food"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'TR_VERB'):
        # Check if words following the transitive verb are a DP
        dp_truth, dp_pos_list = is_dp_s(knowledge, tail)
        if dp_truth:
            return True, ['TR_VERB'] + dp_pos_list
    elif knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_tr_vp_3(knowledge, tail)
        return truth, ['ADV'] + pos_list
    return False, []

def is_simple_vp_3(knowledge, elements):
    '''Determine if given set of words is any type of Verb Phrase'''

    tr_truth, tr_pos = is_tr_vp_3(knowledge, elements)
    int_truth, int_pos = is_int_vp_3(knowledge, elements)
    if tr_truth:
        return True, tr_pos
    elif int_truth:
        return True, int_pos
    return False, []

def is_simple_vp_3_with_advp(knowledge, elements):
    '''
    Determine if given set of words is a VP followed by any number of adverbs
    This includes 0 adverbs
    e.g. "eats the food often quickly"
    '''

    vp_truth, vp_pos = is_simple_vp_3(knowledge, elements)
    # If it is a standard VP, it is accepted
    if vp_truth:
        return True, vp_pos
    head, *tail = elements
    head = [head]
    # Check to see if it is a VP + ADVP
    while tail:
        vp_truth, vp_pos = is_simple_vp_3(knowledge, head)
        adv_truth, adv_pos = is_advp(knowledge, tail)
        if vp_truth and adv_truth:
            return True, vp_pos + adv_pos
        new_head, *tail = tail
        head += [new_head]
    return False, []

def is_specifier(knowledge, elements):
    '''
    Determine if given set of words is a Specifier
    e.g. "that eats the bird that eats the food"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    head = [head]
    if knowledge.is_a(head, 'SPEC'):
        truth, pos_list = is_simple_vp_3(knowledge, tail)
        if truth:
            return truth, ['SPEC'] + pos_list
        head, *tail = tail
        head = [head]
        while tail:
            vp_truth, vp_pos = is_simple_vp_3(knowledge, head)
            sub_truth, sub_pos = is_specifier(knowledge, tail)
            if vp_truth and sub_truth:
                return True, ['SPEC'] + vp_pos + sub_pos
            new_head, *tail = tail
            head += [new_head]
    return False, []

def is_specifier_with_advp(knowledge, elements):
    '''
    Determine if given set of words is a Specifier followed by any number of adverbs
    This includes 0 adverbs
    e.g. "that eats the bird that eats the food quickly"
    '''

    sc_truth, sc_pos = is_specifier(knowledge, elements)
    # If it is a standard Specifier, it is accepted
    if sc_truth:
        return True, sc_pos
    head, *tail = elements
    head = [head]
    # Check to see if it is a Specifier + ADVP
    while tail:
        sc_truth, sc_pos = is_specifier(knowledge, head)
        adv_truth, adv_pos = is_advp(knowledge, tail)
        if sc_truth and adv_truth:
            return True, sc_pos + adv_pos
        new_head, *tail = tail
        head += [new_head]
    return False, []

def is_tr_vp_3_with_specifier(knowledge, elements):
    '''
    Determine if given set of words is a transitive VP with an optional Specifier
    e.g. "eats the bird that eats the food"
    '''

    head, *tail = elements
    head = [head]
    # Check to see if it is a Transitive VP + Specifier with optional ADVP
    while tail:
        tr_truth, tr_pos = is_tr_vp_3(knowledge, head)
        sp_truth, sp_pos = is_specifier_with_advp(knowledge, tail)
        if tr_truth and sp_truth:
            return True, tr_pos + sp_pos
        new_head, *tail = tail
        head += [new_head]
    return False, []

def is_subject(knowledge, elements):
    '''
    Determine if given set of words is a viable Subject for a sentence
    DP | DP + Specifier | DP + Specifier + ADVP
    '''

    dp_truth, dp_pos = is_dp_s(knowledge, elements)
    # If it is a standard DP, it is accepted
    if dp_truth:
        return True, dp_pos
    head, *tail = elements
    head = [head]
    # Check to see if it is a DP + Specifier with ADVP
    while tail:
        dp_truth, dp_pos = is_dp_s(knowledge, head)
        sc_truth, sc_pos = is_specifier_with_advp(knowledge, tail)
        if dp_truth and sc_truth:
            return True, dp_pos + sc_pos
        new_head, *tail = tail
        head += [new_head]
    return False, []

def is_predicate(knowledge, elements):
    '''
    Determine if given set of words is a viable Predicate for a sentence
    VP | VP + ADVP | Int_VP + Specifier | Int_VP + Specifier + ADVP
    '''
    vp_truth, vp_pos = is_simple_vp_3_with_advp(knowledge, elements)
    tr_sp_truth, tr_sp_pos = is_tr_vp_3_with_specifier(knowledge, elements)
    if vp_truth:
        return True, vp_pos
    elif tr_sp_truth:
        return True, tr_sp_pos
    return False, []

def is_sentence(knowledge, elements):
    '''Determine if given set of words is a grammatical sentence'''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    head = [head]
    while tail:
        subj_truth, subj_pos = is_subject(knowledge, head)
        pred_truth, pred_pos = is_predicate(knowledge, tail)
        if subj_truth and pred_truth:
            return True, subj_pos + pred_pos
        new_head, *tail = tail
        head += [new_head] 
    return False, []

def main():
    # Test
    knowledge = lp.FactTracker()
    with open('word_lists/nouns_singular.txt', 'r') as infile:
        nouns_s = infile.readlines()
    with open('word_lists/transitive_verbs_3rd.txt', 'r') as infile:
        tr_verbs_3 = infile.readlines()
    with open('word_lists/intransitive_verbs_3rd.txt', 'r') as infile:
        int_verbs_3 = infile.readlines()
    with open('word_lists/adjectives.txt', 'r') as infile:
        adjectives = infile.readlines()
    with open('word_lists/adverbs.txt', 'r') as infile:
        adverbs = infile.readlines()
    with open('word_lists/determiners.txt', 'r') as infile:
        determiners = infile.readlines()
    with open('word_lists/specifiers.txt', 'r') as infile:
        specifiers = infile.readlines()

    for n in nouns_s:
        knowledge.update_knowledge(lp.Fact('NOUN_S', n.strip()))
    for t in tr_verbs_3:
        knowledge.update_knowledge(lp.Fact('TR_VERB_3', t.strip()))
    for i in int_verbs_3:
        knowledge.update_knowledge(lp.Fact('INT_VERB_3', i.strip()))
    for a in adjectives:
        knowledge.update_knowledge(lp.Fact('ADJ', a.strip()))
    for ad in adverbs:
        knowledge.update_knowledge(lp.Fact('ADV', ad.strip()))
    for d in determiners:
        knowledge.update_knowledge(lp.Fact('DET', d.strip()))
    for c in specifiers:
        knowledge.update_knowledge(lp.Fact('SPEC', c.strip()))

    keep_going = 'y'
    while keep_going == 'y':
        user_sent = input('Enter sentence >> ').split()
        # print('NP > ', is_np_s(knowledge, user_sent))
        # print('INT_VP_3 > ', is_int_vp_3(knowledge, user_sent))
        # print('TR_VP_3 > ', is_tr_vp_3(knowledge, user_sent))
        # print('ADVP > ', is_advp(knowledge, user_sent))
        # print('VP_3 + ADVP > ', is_simple_vp_3_with_advp(knowledge, user_sent))
        # print('DP > ', is_dp_s(knowledge, user_sent))
        # print('Specifier > ', is_specifier(knowledge, user_sent))
        # print('Specifier + ADVP > ', is_specifier_with_advp(knowledge, user_sent))
        # print('TR_VP_3 + Specifier > ', is_tr_vp_3_with_specifier(knowledge, user_sent))
        # print('Subject > ', is_subject(knowledge, user_sent))
        # print('Predicate > ', is_predicate(knowledge, user_sent))
        print('SENTENCE > ', is_sentence(knowledge, user_sent))
        keep_going = input('Continue? (y/n) ')

if __name__ == '__main__':
    main()