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

def is_wrapped(knowledge, elements, f1, f2, f3):
    '''
    Determine if a given set of words is a combo of three types,
    one embedded between two others.

    This is relevant for cases of auxiliary verbs agreeing with
    other verbs:
    e.g. "does the bird eat"
    '''

    head, *middle, end = elements
    head, end = [head], [end]
    head_truth, head_pos = f1(knowledge, head)
    middle_truth, middle_pos = f2(knowledge, middle)
    end_truth, end_pos = f3(knowledge, end)
    if head_truth and middle_truth and end_truth:
        return True, head_pos + middle_pos + end_pos
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

def is_wh_subject_word(knowledge, elements):
    '''
    Determine if given set of words is a WH-word that can serve as a subject
    Specifically: "who" and "what"
    '''

    if len(elements) == 1 and knowledge.is_a(elements, 'WH_S'):
        return True, ['WH_S']
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

def is_np_p(knowledge, elements):
    '''
    Determine if a given set of words is a Plural Noun Phrase
    e.g. "small blue dogs"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'NOUN_P'):
        return True, ['NOUN_P']
    head, *tail = elements
    if knowledge.is_a([head], 'ADJ'):
        truth, pos_list = is_np_p(knowledge, tail)
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

def is_dp_p(knowledge, elements):
    '''
    Determine if a given set of words in a Singular Determiner Phrase
    e.g. "the small blue dogs"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'DET'):
        truth, pos_list = is_np_p(knowledge, tail)
        return truth, ['DET'] + pos_list
    return False, []

def is_advp(knowledge, elements):
    '''
    Determine if given set of words is a series of Adverbs
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

def is_aux(knowledge, elements):
    '''Determine if a given set of words is an Auxiliary Verb'''

    if len(elements) == 1 and knowledge.is_a(elements, 'AUX'):
        return True, ['AUX']
    return False, []

def is_int_vp_1(knowledge, elements):
    '''
    Determine if a given set of words is a 1st Person (or 2nd or Plural-3rd)
    Intransitive Verb Phrase
    e.g. "often sleep"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'INT_VERB_1'):
        # A lone verb works
        return True, ['INT_VERB_1']
    head, *tail = elements
    if knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_int_vp_1(knowledge, tail)
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

def is_tr_vp_1(knowledge, elements):
    '''
    Determine if given set of words is a 1st Person Transitive Verb Phrase
    e.g. "throw the food"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'TR_VERB_1'):
        # Check if words following the transitive verb are a DP
        dp_truth, dp_pos_list = is_dp_p(knowledge, tail)
        if dp_truth:
            return True, ['TR_VERB_1'] + dp_pos_list
    elif knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_tr_vp_1(knowledge, tail)
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

def is_simple_vp_1(knowledge, elements):
    '''Determine if given set of words is any type of 1st-Person Verb Phrase'''

    tr_truth, tr_pos = is_tr_vp_1(knowledge, elements)
    int_truth, int_pos = is_int_vp_1(knowledge, elements)
    if tr_truth:
        return True, tr_pos
    elif int_truth:
        return True, int_pos
    return False, []

def is_simple_vp_3(knowledge, elements):
    '''Determine if given set of words is any type of 3rd-Person Verb Phrase'''

    tr_truth, tr_pos = is_tr_vp_3(knowledge, elements)
    int_truth, int_pos = is_int_vp_3(knowledge, elements)
    if tr_truth:
        return True, tr_pos
    elif int_truth:
        return True, int_pos
    return False, []

def is_simple_vp(knowledge, elements):
    '''Determine if given set of words is any type of Verb Phrase'''

    first_truth, first_pos = is_simple_vp_1(knowledge, elements)
    third_truth, third_pos = is_simple_vp_3(knowledge, elements)
    if first_truth:
        return True, first_pos
    elif third_truth:
        return True, third_pos
    return False, []

def is_simple_vp_1_with_advp(knowledge, elements):
    '''
    Determine if given set of words is a VP followed by any number of adverbs
    This includes 0 adverbs
    e.g. "eat the food often quickly"
    '''

    vp_truth, vp_pos = is_simple_vp_1(knowledge, elements)
    # If it is a standard VP, it is accepted
    if vp_truth:
        return True, vp_pos
    # Check to see if it is a VP + ADVP
    return is_branches(knowledge, elements, is_simple_vp_1, is_advp)

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

def is_subject(knowledge, elements):
    '''
    Determine if given set of words is a viable Subject for a sentence
    DP | DP + Specifier | DP + Specifier + ADVP
    '''

    dp_truth, dp_pos = is_dp_s(knowledge, elements)
    # If it is a standard DP, it is accepted
    if dp_truth:
        return True, dp_pos
    # Check to see if it is a DP + Specifier with ADVP
    return is_branches(knowledge, elements, is_dp_s, is_specifier_with_advp)

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

def is_aux_phrase(knowledge, elements):
    '''
    Determine if a given set of words is an auxiliary verb phrase
    e.g. "does the bird eat"
    '''

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(knowledge, elements, is_aux, is_subject, is_int_vp_1)
    if aux_truth:
        return True, aux_pos
    return False, []

def is_wh_question(knowledge, elements):
    '''
    Determine if given set of words is a grammatical wh-question
    '''

    if len(elements) < 2:
        return False, []

    subj_truth, subj_pos = is_branches(knowledge, elements, is_wh_subject_word, is_predicate)
    aux_truth, aux_pos = is_branches(knowledge, elements, is_wh_word, is_aux_phrase)
    if subj_truth:
        return True, subj_pos
    elif aux_truth:
        return True, aux_pos
    return False, []

def main():
    # Test
    knowledge = lp.FactTracker()
    with open('word_lists/nouns_singular.txt', 'r') as infile:
        nouns_s = infile.readlines()
    with open('word_lists/nouns_plural.txt', 'r') as infile:
        nouns_p = infile.readlines()
    with open('word_lists/transitive_verbs_1st.txt', 'r') as infile:
        tr_verbs_1 = infile.readlines()
    with open('word_lists/transitive_verbs_3rd.txt', 'r') as infile:
        tr_verbs_3 = infile.readlines()
    with open('word_lists/intransitive_verbs_1st.txt', 'r') as infile:
        int_verbs_1 = infile.readlines()
    with open('word_lists/intransitive_verbs_3rd.txt', 'r') as infile:
        int_verbs_3 = infile.readlines()
    with open('word_lists/auxiliary_verbs.txt', 'r') as infile:
        aux_verbs = infile.readlines()
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
    with open('word_lists/wh_subject_words.txt', 'r') as infile:
        wh_subject_words = infile.readlines()

    for ns in nouns_s:
        knowledge.update_knowledge(lp.Fact('NOUN_S', ns.strip()))
    for np in nouns_p:
        knowledge.update_knowledge(lp.Fact('NOUN_P', np.strip()))
    for t1 in tr_verbs_1:
        knowledge.update_knowledge(lp.Fact('TR_VERB_1', t1.strip()))
    for t3 in tr_verbs_3:
        knowledge.update_knowledge(lp.Fact('TR_VERB_3', t3.strip()))
    for i1 in int_verbs_1:
        knowledge.update_knowledge(lp.Fact('INT_VERB_1', i1.strip()))
    for i3 in int_verbs_3:
        knowledge.update_knowledge(lp.Fact('INT_VERB_3', i3.strip()))
    for aux in aux_verbs:
        knowledge.update_knowledge(lp.Fact('AUX', aux.strip()))
    for adj in adjectives:
        knowledge.update_knowledge(lp.Fact('ADJ', adj.strip()))
    for adv in adverbs:
        knowledge.update_knowledge(lp.Fact('ADV', adv.strip()))
    for d in determiners:
        knowledge.update_knowledge(lp.Fact('DET', d.strip()))
    for s in specifiers:
        knowledge.update_knowledge(lp.Fact('SPEC', s.strip()))
    for w in wh_words:
        knowledge.update_knowledge(lp.Fact('WH', w.strip()))
    for ws in wh_subject_words:
        knowledge.update_knowledge(lp.Fact('WH_S', ws.strip()))

    keep_going = 'y'
    while keep_going == 'y':
        user_sent = input('Enter wh-question >> ').split()
        # print('NP > ', is_np_s(knowledge, user_sent))
        # print('INT_VP_1 > ', is_int_vp_1(knowledge, user_sent))
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