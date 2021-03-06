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

    head, *tail = elements
    head = [head]
    head_truth, head_pos = f1(knowledge, head)
    tail_truth, tail_pos = is_branches(knowledge, tail, f2, f3)
    if head_truth and tail_truth:
        return True, head_pos + tail_pos
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
        if truth:
            return True, ['DET'] + pos_list
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
        if truth:
            return True, ['DET'] + pos_list
    return False, []

def is_dp(knowledge, elements):
    '''
    Determine if given set of words is any type of Determiner Phrase
    Singular or Plural
    '''

    s_truth, s_pos = is_dp_s(knowledge, elements)
    p_truth, p_pos = is_dp_p(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
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

def is_aux_s(knowledge, elements):
    '''Determine if a given set of words is an Singular Auxiliary Verb'''

    if len(elements) == 1 and knowledge.is_a(elements, 'AUX_S'):
        return True, ['AUX_S']
    return False, []

def is_aux_p(knowledge, elements):
    '''Determine if a given set of words is an Plural Auxiliary Verb'''

    if len(elements) == 1 and knowledge.is_a(elements, 'AUX_P'):
        return True, ['AUX_P']
    return False, []

def is_int_vp_1(knowledge, elements):
    '''
    Determine if a given set of words is a 1st Person (or 2nd or Plural-3rd)
    Intransitive Verb Phrase
    e.g. "often sleep"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1:
        # A lone verb works
        if knowledge.is_a(elements, 'INT_VERB_1'):
            return True, ['INT_VERB_1']
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_int_vp_1(knowledge, tail)
        if truth:
            return True, ['ADV'] + pos_list
    return False, []

def is_int_vp_3(knowledge, elements):
    '''
    Determine if a given set of words is a 3rd Person Intransitive Verb Phrase
    e.g. "often sleeps"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1:
        # A lone verb works
        if knowledge.is_a(elements, 'INT_VERB_3'):
            return True, ['INT_VERB_3']
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'ADV'):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_int_vp_3(knowledge, tail)
        if truth:
            return True, ['ADV'] + pos_list
    return False, []

def is_advp_with_tr_v_1(knowledge, elements):
    '''
    Determine if given set of words is an adverb phrase followed by a 1st
    Person Transitive Verb
    e.g. "often throw"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1:
        # A lone transitive verb work
        if knowledge.is_a(elements, 'TR_VERB_1'):
            return True, ['TR_VERB_1']
        return False, []
    *head, tail = elements
    adv_truth, adv_pos = is_advp(knowledge, head)
    if adv_truth and knowledge.is_a([tail], 'TR_VERB_1'):
        return True, adv_pos + ['TR_VERB_1']
    return False, []

def is_advp_with_tr_v_3(knowledge, elements):
    '''
    Determine if given set of words is an adverb phrase followed by a 3rd
    Person Transitive Verb
    e.g. "often throws"
    '''

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1:
        # A lone transitive verb work
        if knowledge.is_a(elements, 'TR_VERB_3'):
            return True, ['TR_VERB_3']
        return False, []
    *head, tail = elements
    adv_truth, adv_pos = is_advp(knowledge, head)
    if adv_truth and knowledge.is_a([tail], 'TR_VERB_3'):
        return True, adv_pos + ['TR_VERB_3']
    return False, []

def is_tr_vp_1(knowledge, elements):
    '''
    Determine if given set of words is a 1st Person Transitive Verb Phrase
    Can have any number of preceding adverbs
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
    Can have any number of preceding adverbs
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

def is_specifier_with_tr_verb_1(knowledge, elements):
    '''
    Determine if given set of words is a specifier followed by a
    First Person Transitive Verb
    e.g. "that quickly throw"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are a transitive verb phrase
        tr_truth, tr_pos_list = is_advp_with_tr_v_1(knowledge, tail)
        if tr_truth:
            return True, ['SPEC'] + tr_pos_list
    return False, []

def is_specifier_with_tr_verb_3(knowledge, elements):
    '''
    Determine if given set of words is a specifier followed by a
    3rd Person Transitive Verb
    e.g. "that quickly throws"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are an transitive verb phrase
        tr_truth, tr_pos_list = is_advp_with_tr_v_3(knowledge, tail)
        if tr_truth:
            return True, ['SPEC'] + tr_pos_list
    return False, []

def is_specifier_with_int_verb_1(knowledge, elements):
    '''
    Determine if given set of words is a Specifier followed by an
    Intransitive 1st Person Verb Phrase
    e.g. "that sleep"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are a transitive verb phrase
        int_truth, int_pos_list = is_int_vp_1(knowledge, tail)
        if int_truth:
            return True, ['SPEC'] + int_pos_list
    return False, []

def is_specifier_with_int_verb_3(knowledge, elements):
    '''
    Determine if given set of words is a Specifier followed by an
    Intransitive 3rd Person Verb Phrase
    e.g. "that sleeps"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are a transitive verb phrase
        int_truth, int_pos_list = is_int_vp_3(knowledge, tail)
        if int_truth:
            return True, ['SPEC'] + int_pos_list
    return False, []

def is_dp_s_with_spec_and_tr_verb(knowledge, elements):
    '''
    Determine if given set of words is a Singular Determiner Phrase
    with a Specifier and 3rd Person Transitive Verb
    e.g. "the cat that quickly throws"
    '''

    return is_branches(knowledge, elements, is_dp_s, is_specifier_with_tr_verb_3)

def is_dp_p_with_spec_and_tr_verb(knowledge, elements):
    '''
    Determine if given set of words is a Plural Determiner Phrase
    with a Specifier and 1st Person Transitive Verb
    e.g. "the cats that quickly throw"
    '''

    return is_branches(knowledge, elements, is_dp_p, is_specifier_with_tr_verb_1)

def is_dp_with_spec_and_tr_verb(knowledge, elements):
    '''
    Determine if given set of words is any type of Determiner Phrase
    with a Specifier and Transitive Verb
    Singular or Plural
    '''

    s_truth, s_pos = is_dp_s_with_spec_and_tr_verb(knowledge, elements)
    p_truth, p_pos = is_dp_p_with_spec_and_tr_verb(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []

def is_dp_s_with_spec_and_int_verb(knowledge, elements):
    '''
    Determine if given set of words is a Singular Determiner Phrase
    with a Specifier and 3rd Person Intransitive Verb
    e.g. "the cat that quickly sleeps"
    '''

    return is_branches(knowledge, elements, is_dp_s, is_specifier_with_int_verb_3)

def is_dp_p_with_spec_and_int_verb(knowledge, elements):
    '''
    Determine if given set of words is a Plural Determiner Phrase
    with a Specifier and 1st Person Intransitive Verb
    e.g. "the cats that quickly sleep"
    '''

    return is_branches(knowledge, elements, is_dp_p, is_specifier_with_int_verb_1)

def is_dp_with_spec_and_int_verb(knowledge, elements):
    '''
    Determine if given set of words is a Determiner Phrase
    with a Specifier
    Singular or Plural
    '''

    s_truth, s_pos = is_dp_s_with_spec_and_int_verb(knowledge, elements)
    p_truth, p_pos = is_dp_p_with_spec_and_int_verb(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []

def is_spec_ender(knowledge, elements):
    '''
    Determine if a given set of words can serve to end a Specifier Phrase
    This can be any Determiner Phrase or DP with a Spec and Intransitive Verb 
    '''

    dp_truth, dp_pos = is_dp(knowledge, elements)
    spec_truth, spec_pos = is_dp_with_spec_and_int_verb(knowledge, elements)
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []

def is_specifier_phrase(knowledge, elements):
    '''
    Determine if given set of words is a Specifier Phrase
    e.g. "the cat that eats the bird that eats the food"
    '''

    if len(elements) < 3:
        return False, []
    # Any single Intransitive Phrase will work
    int_truth, int_pos = is_dp_with_spec_and_int_verb(knowledge, elements)
    if int_truth:
        return True, int_pos
    tr_truth, tr_pos = is_branches(knowledge, elements, is_dp_with_spec_and_tr_verb, is_spec_ender)
    if tr_truth:
        return True, tr_pos
    nested_truth, nested_pos = is_branches(knowledge, elements, is_dp_with_spec_and_tr_verb, is_specifier_phrase)
    if nested_truth:
        return True, nested_pos
    return False, []

def is_specifier_phrase_s(knowledge, elements):
    '''
    Determine if given set of words is a Singular Specifier Phrase
    e.g. "the cat that eats the bird"
    '''

    if len(elements) < 3:
        return False, []
    # Any single Intransitive Phrase will work
    int_truth, int_pos = is_dp_s_with_spec_and_int_verb(knowledge, elements)
    if int_truth:
        return True, int_pos
    tr_truth, tr_pos = is_branches(knowledge, elements, 
                                   is_dp_s_with_spec_and_tr_verb, is_spec_ender)
    if tr_truth:
        return True, tr_pos
    nested_truth, nested_pos = is_branches(knowledge, elements, 
                                           is_dp_s_with_spec_and_tr_verb, is_specifier_phrase)
    if nested_truth:
        return True, nested_pos
    return False, []

def is_specifier_phrase_p(knowledge, elements):
    '''
    Determine if given set of words is a Plural Specifier Phrase
    e.g. "the cats that eat the bird"
    '''

    if len(elements) < 3:
        return False, []
    # Any single Intransitive Phrase will work
    int_truth, int_pos = is_dp_p_with_spec_and_int_verb(knowledge, elements)
    if int_truth:
        return True, int_pos
    tr_truth, tr_pos = is_branches(knowledge, elements, 
                                   is_dp_p_with_spec_and_tr_verb, is_spec_ender)
    if tr_truth:
        return True, tr_pos
    nested_truth, nested_pos = is_branches(knowledge, elements, 
                                           is_dp_p_with_spec_and_tr_verb, is_specifier_phrase)
    if nested_truth:
        return True, nested_pos
    return False, []

def is_specifier_s_with_advp(knowledge, elements):
    '''
    Determine if given set of words is a Singular Specifier followed by any number of adverbs
    This includes 0 adverbs
    e.g. "the cat that eats the bird that eats the food quickly"
    '''

    sp_truth, sp_pos = is_specifier_phrase_s(knowledge, elements)
    # If it is a standard Specifier Phrase, it is accepted
    if sp_truth:
        return True, sp_pos
    # Check to see if it is a Specifier + ADVP
    return is_branches(knowledge, elements, is_specifier_phrase_s, is_advp)

def is_specifier_p_with_advp(knowledge, elements):
    '''
    Determine if given set of words is a Plural Specifier followed by any number of adverbs
    This includes 0 adverbs
    e.g. "the cats that eat the bird that eats the food quickly"
    '''

    sp_truth, sp_pos = is_specifier_phrase_p(knowledge, elements)
    # If it is a standard Specifier Phrase, it is accepted
    if sp_truth:
        return True, sp_pos
    # Check to see if it is a Specifier + ADVP
    return is_branches(knowledge, elements, is_specifier_phrase_p, is_advp)

def is_specifier_with_advp(knowledge, elements):
    '''
    Determine if given set of words is a Specifier followed by any number of adverbs
    This includes 0 adverbs
    e.g. "the cat that eats the bird that eats the food quickly"
    '''

    sp_truth, sp_pos = is_specifier_phrase(knowledge, elements)
    # If it is a standard Specifier Phrase, it is accepted
    if sp_truth:
        return True, sp_pos
    # Check to see if it is a Specifier + ADVP
    return is_branches(knowledge, elements, is_specifier_phrase, is_advp)

def is_tr_vp_3_with_specifier(knowledge, elements):
    '''
    Determine if given set of words is a transitive VP with an optional Specifier
    e.g. "eats the bird that eats the food"
    '''

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'TR_VERB_3'):
        truth, pos_list = is_specifier_with_advp(knowledge, tail)
        if truth:
            return True, ['TR_VERB_3'] + pos_list
    return False, []

def is_subject_s(knowledge, elements):
    '''
    Determine if given set of words is a viable Singular Subject for a sentence
    DP | Specifier Phrase | Specifier Phrase + ADVP
    '''

    dp_truth, dp_pos = is_dp_s(knowledge, elements)
    spec_truth, spec_pos = is_specifier_s_with_advp(knowledge, elements)
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []

def is_subject_p(knowledge, elements):
    '''
    Determine if given set of words is a viable Plural Subject for a sentence
    DP | Specifier Phrase | Specifier Phrase + ADVP
    '''

    dp_truth, dp_pos = is_dp_p(knowledge, elements)
    spec_truth, spec_pos = is_specifier_p_with_advp(knowledge, elements)
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []

def is_subject(knowledge, elements):
    '''
    Determine if given set of words is a viable Subject for a sentence
    DP | Specifier Phrase | Specifier Phrase + ADVP
    '''

    dp_truth, dp_pos = is_dp(knowledge, elements)
    spec_truth, spec_pos = is_specifier_with_advp(knowledge, elements)
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []

def is_predicate(knowledge, elements):
    '''
    Determine if given set of words is a viable Predicate for a sentence
    VP | VP + ADVP | Tr_VP + Specifier | Tr_VP + Specifier + ADVP
    '''
    vp_truth, vp_pos = is_simple_vp_3_with_advp(knowledge, elements)
    tr_sp_truth, tr_sp_pos = is_tr_vp_3_with_specifier(knowledge, elements)
    if vp_truth:
        return True, vp_pos
    elif tr_sp_truth:
        return True, tr_sp_pos
    return False, []

def is_int_aux_phrase_s(knowledge, elements):
    '''
    Determine if a given set of words is a Singular Intransitive Auxiliary Verb Phrase
    e.g. "does the bird sleep"
    '''

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(knowledge, elements, is_aux_s, is_subject_s, is_int_vp_1)
    if aux_truth:
        return True, aux_pos
    return False, []

def is_int_aux_phrase_p(knowledge, elements):
    '''
    Determine if a given set of words is a Plural Intransitive Auxiliary Verb Phrase
    e.g. "do the birds sleep"
    '''

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(knowledge, elements, is_aux_p, is_subject_p, is_int_vp_1)
    if aux_truth:
        return True, aux_pos
    return False, []

def is_int_aux_phrase(knowledge, elements):
    '''
    Determine if a given set of words is any Intransitive Auxiliary Verb Phrase
    Singular or Plural
    '''

    s_truth, s_pos = is_int_aux_phrase_s(knowledge, elements)
    p_truth, p_pos = is_int_aux_phrase_p(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []

def is_tr_aux_phrase_s(knowledge, elements):
    '''
    Determine if a given set of words is a Singular Transitive Auxiliary Verb Phrase
    e.g. "does the bird throw"
    '''

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(knowledge, elements, is_aux_s, is_subject_s, is_advp_with_tr_v_1)
    if aux_truth:
        return True, aux_pos
    return False, []

def is_tr_aux_phrase_p(knowledge, elements):
    '''
    Determine if a given set of words is a Plural Transitive Auxiliary Verb Phrase
    e.g. "do the birds throw"
    '''

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(knowledge, elements, is_aux_p, is_subject_p, is_advp_with_tr_v_1)
    if aux_truth:
        return True, aux_pos
    return False, []

def is_tr_aux_phrase(knowledge, elements):
    '''
    Determine if a given set of words is any Transitive Auxiliary Verb Phrase
    Singular or Plural
    '''

    s_truth, s_pos = is_tr_aux_phrase_s(knowledge, elements)
    p_truth, p_pos = is_tr_aux_phrase_p(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []

def is_aux_phrase(knowledge, elements):
    '''
    Determine if given set of words is any complete Auxiliary Verb Phrase
    Transitive or Intransitive
    '''

    int_truth, int_pos = is_int_aux_phrase(knowledge, elements)
    if int_truth:
        return True, int_pos
    return is_branches(knowledge, elements, is_tr_aux_phrase, is_subject)

def is_wh_question(knowledge, elements):
    '''
    Determine if given set of words is a grammatical wh-question
    '''

    if len(elements) < 2:
        return False, []

    subj_truth, subj_pos = is_branches(knowledge, elements, is_wh_subject_word, is_predicate)
    int_aux_truth, int_aux_pos = is_branches(knowledge, elements, is_wh_subject_word, is_int_aux_phrase)
    aux_truth, aux_pos = is_branches(knowledge, elements, is_wh_word, is_aux_phrase)
    if subj_truth:
        return True, subj_pos
    elif int_aux_truth:
        return True, int_aux_pos
    elif aux_truth:
        return True, aux_pos
    return False, []

def is_wh_question_with_adv(knowledge, elements):
    '''
    Determine if given set of words is a wh-question plus 0 or 1 adverbs
    e.g. "what does the bird eat quickly"
    '''

    *head, tail = elements
    wh_question_truth, wh_question_pos = is_wh_question(knowledge, head)
    if wh_question_truth and knowledge.is_a([tail], 'ADV'):
        return wh_question_pos + ['ADV']

    return is_wh_question(knowledge, elements)

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
    with open('word_lists/auxiliary_verbs_singular.txt', 'r') as infile:
        aux_verbs_s = infile.readlines()
    with open('word_lists/auxiliary_verbs_plural.txt', 'r') as infile:
        aux_verbs_p = infile.readlines()
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
    for aux_s in aux_verbs_s:
        knowledge.update_knowledge(lp.Fact('AUX_S', aux_s.strip()))
    for aux_p in aux_verbs_p:
        knowledge.update_knowledge(lp.Fact('AUX_P', aux_p.strip()))
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
        # print('ADVP_with_TR_V_1', is_advp_with_tr_v_1(knowledge, user_sent))
        # print('ADVP_with_TR_V_3', is_advp_with_tr_v_3(knowledge, user_sent))
        # print('ADVP > ', is_advp(knowledge, user_sent))
        # print('VP_3 + ADVP > ', is_simple_vp_3_with_advp(knowledge, user_sent))
        # print('DP > ', is_dp_s(knowledge, user_sent))
        # print('SPEC_with_TR_V_1 > ', is_specifier_with_tr_verb_1(knowledge, user_sent))
        # print('SPEC_with_TR_V_3 > ', is_specifier_with_tr_verb_3(knowledge, user_sent))
        # print('SPEC_with_INT_V_1 > ', is_specifier_with_int_verb_1(knowledge, user_sent))
        # print('SPEC_with_INT_V_3 > ', is_specifier_with_int_verb_3(knowledge, user_sent))
        # print('SPEC Singuler > ', is_specifier_phrase_s(knowledge, user_sent))
        # print('Specifier Phrase > ', is_specifier_phrase(knowledge, user_sent))
        # print('Specifier + ADVP > ', is_specifier_with_advp(knowledge, user_sent))
        # print('DP_S_with_SPEC', is_dp_s_with_spec_and_tr_verb(knowledge, user_sent))
        # print('DP_P_with_SPEC', is_dp_p_with_spec_and_tr_verb(knowledge, user_sent))
        # print('DP_with_SPEC_and_TR_VERB', is_dp_with_spec_and_tr_verb(knowledge, user_sent))
        # print('TR_VP_3 + Specifier > ', is_tr_vp_3_with_specifier(knowledge, user_sent))
        # print('Subject > ', is_subject(knowledge, user_sent))
        # print('Subject Singular > ', is_subject_s(knowledge, user_sent))
        # print('Predicate > ', is_predicate(knowledge, user_sent))
        # print('Int Aux Phrase S > ', is_int_aux_phrase_s(knowledge, user_sent))
        # print('Trans Aux Phrase S > ', is_tr_aux_phrase_s(knowledge, user_sent))
        # print('AUX > ', is_aux_phrase(knowledge, user_sent))
        # print('Wh question > ', is_wh_question(knowledge, user_sent))
        print('Wh question >', is_wh_question_with_adv(knowledge, user_sent))
        keep_going = input('Continue? (y/n) ')

if __name__ == '__main__':
    main()