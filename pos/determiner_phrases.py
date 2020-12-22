from pos.noun_phrases import is_np_s, is_np_p


def is_dp_s(knowledge, elements):
    """
    Determine if a given set of words in a Singular Determiner Phrase
    e.g. "the small blue dog"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'DET'):
        truth, pos_list = is_np_s(knowledge, tail)
        if truth:
            return True, ['DET'] + pos_list
    return False, []


def is_dp_p(knowledge, elements):
    """
    Determine if a given set of words in a Singular Determiner Phrase
    e.g. "the small blue dogs"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'DET'):
        truth, pos_list = is_np_p(knowledge, tail)
        if truth:
            return True, ['DET'] + pos_list
    return False, []


def is_dp(knowledge, elements):
    """
    Determine if given set of words is any type of Determiner Phrase
    Singular or Plural
    """

    s_truth, s_pos = is_dp_s(knowledge, elements)
    p_truth, p_pos = is_dp_p(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []
