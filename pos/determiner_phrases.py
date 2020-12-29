from pos.noun_phrases import is_noun_phrase_singlular, is_noun_phrase_plural


def is_determiner_phrase_singular(knowledge, elements):
    """
    Determine if a given set of words in a Singular Determiner Phrase
    e.g. "the small blue dog"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'DET'):
        truth, pos_list = is_noun_phrase_singlular(knowledge, tail)
        if truth:
            return True, ['DET'] + pos_list
    return False, []


def is_determiner_phrase_plural(knowledge, elements):
    """
    Determine if a given set of words is a Plural Determiner Phrase
    e.g. "the small blue dogs"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'DET'):
        truth, pos_list = is_noun_phrase_plural(knowledge, tail)
        if truth:
            return True, ['DET'] + pos_list
    return False, []


def is_determiner_phrase(knowledge, elements):
    """
    Determine if given set of words is any type of Determiner Phrase
    Singular or Plural
    """

    s_truth, s_pos = is_determiner_phrase_singular(knowledge, elements)
    p_truth, p_pos = is_determiner_phrase_plural(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []
