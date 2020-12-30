from pos.int_verb_phrases import is_int_verb_phrase_1, is_int_verb_phrase_3
from pos.tr_verb_phrases import is_adverbs_with_tr_verb_1, is_adverbs_with_tr_verb_3


def is_specifier_with_tr_verb_1(knowledge, elements):
    """
    Determine if given set of words is a specifier followed by a
    First Person Transitive Verb
    e.g. "that quickly throw"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are a transitive verb phrase
        tr_truth, tr_pos_list = is_adverbs_with_tr_verb_1(knowledge, tail)
        if tr_truth:
            return True, ['SPEC'] + tr_pos_list
    return False, []


def is_specifier_with_tr_verb_3(knowledge, elements):
    """
    Determine if given set of words is a specifier followed by a
    3rd Person Transitive Verb
    e.g. "that quickly throws"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are an transitive verb phrase
        tr_truth, tr_pos_list = is_adverbs_with_tr_verb_3(knowledge, tail)
        if tr_truth:
            return True, ['SPEC'] + tr_pos_list
    return False, []


def is_specifier_with_int_verb_1(knowledge, elements):
    """
    Determine if given set of words is a Specifier followed by an
    Intransitive 1st Person Verb Phrase
    e.g. "that sleep"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are a transitive verb phrase
        int_truth, int_pos_list = is_int_verb_phrase_1(knowledge, tail)
        if int_truth:
            return True, ['SPEC'] + int_pos_list
    return False, []


def is_specifier_with_int_verb_3(knowledge, elements):
    """
    Determine if given set of words is a Specifier followed by an
    Intransitive 3rd Person Verb Phrase
    e.g. "that sleeps"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], 'SPEC'):
        # Check if words following specifier are a transitive verb phrase
        int_truth, int_pos_list = is_int_verb_phrase_3(knowledge, tail)
        if int_truth:
            return True, ['SPEC'] + int_pos_list
    return False, []