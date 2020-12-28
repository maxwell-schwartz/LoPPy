def is_int_verb_phrase_1(knowledge, elements):
    """
    Determine if a given set of words is a 1st Person (or 2nd or Plural-3rd)
    Intransitive Verb Phrase
    e.g. "often sleep"
    """

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
        truth, pos_list = is_int_verb_phrase_1(knowledge, tail)
        if truth:
            return True, ['ADV'] + pos_list
    return False, []


def is_int_verb_phrase_3(knowledge, elements):
    """
    Determine if a given set of words is a 3rd Person Intransitive Verb Phrase
    e.g. "often sleeps"
    """

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
        truth, pos_list = is_int_verb_phrase_3(knowledge, tail)
        if truth:
            return True, ['ADV'] + pos_list
    return False, []