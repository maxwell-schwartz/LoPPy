def is_np_s(knowledge, elements):
    """
    Determine if a given set of words is a Singular Noun Phrase
    e.g. "small blue dog"
    """

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
    """
    Determine if a given set of words is a Plural Noun Phrase
    e.g. "small blue dogs"
    """

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'NOUN_P'):
        return True, ['NOUN_P']
    head, *tail = elements
    if knowledge.is_a([head], 'ADJ'):
        truth, pos_list = is_np_p(knowledge, tail)
        return truth, ['ADJ'] + pos_list
    return False, []
