from pos.complex_determiner_phrases import is_complex_determiner_phrase


def is_tr_verb_phrase_3_with_specifier(knowledge, elements):
    """
    Determine if given set of words is a transitive VP with an optional Specifier
    e.g. "eats the bird that eats the food"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], "TR_VERB_3"):
        truth, pos_list = is_complex_determiner_phrase(knowledge, tail)
        if truth:
            return True, ["TR_VERB_3"] + pos_list
    return False, []
