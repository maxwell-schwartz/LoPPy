import loppy as lp

def is_branches(knowledge, elements, f1, f2):
    '''Determine if given set of words is combo of two types'''

    head, *tail = elements
    head = [head]
    # Divide elements
    # If both functions return True, return True and POS list
    while tail:
        left_truth, left_pos = f1(knowledge, head)
        right_truth, right_pos = f2(knowledge, tail)
        if left_truth and right_truth:
            return True, left_pos + right_pos
        new_head, *tail = tail
        head += [new_head]
    return False, []

def is_wh_word(knowledge, elements):
    '''
    Determine if given set of words is a WH-word

    To Do: deal with preposition cases, e.g. To what...
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'WH'):
        return True, ['WH']
    return False, []

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
    Determin if given set of words is a series of Adverbs
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
    elif len(elements) == 1 and knowledge.is_a(elements, 'INT_VERB_3'):
        # A lone verb works
        return True, ['INT_VERB_3']
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
    if knowledge.is_a([head], 'TR_VERB_3'):
        # Check if words following the transitive verb are a DP
        dp_truth, dp_pos_list = is_dp_s(knowledge, tail)
        if dp_truth:
            return True, ['TR_VERB_3'] + dp_pos_list
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
    # Check to see if it is a VP + ADVP
    return is_branches(knowledge, elements, is_simple_vp_3, is_advp)

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
    # Check to see if it is a Specifier + ADVP
    return is_branches(knowledge, elements, is_specifier, is_advp)

def is_tr_vp_3_with_specifier(knowledge, elements):
    '''
    Determine if given set of words is a transitive VP with an optional Specifier
    e.g. "eats the bird that eats the food"
    '''

    return is_branches(knowledge, elements, is_tr_vp_3, is_specifier_with_advp)

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

def is_wh_question(knowledge, elements):
    '''Determine if given set of words is a grammatical wh-question'''

    if len(elements) < 2:
        return False, []

    return is_branches(knowledge, elements, is_wh_word, is_predicate)

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
    with open('word_lists/wh_words.txt', 'r') as infile:
        wh_words = infile.readlines()

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
    for s in specifiers:
        knowledge.update_knowledge(lp.Fact('SPEC', s.strip()))
    for w in wh_words:
        knowledge.update_knowledge(lp.Fact('WH', w.strip()))

    keep_going = 'y'
    while keep_going == 'y':
        user_sent = input('Enter wh-question >> ').split()
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
        print('Wh question > ', is_wh_question(knowledge, user_sent))
        keep_going = input('Continue? (y/n) ')

if __name__ == '__main__':
    main()