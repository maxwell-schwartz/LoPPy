from pos.adverbs import is_adverbs
from pos.int_verb_phrases import is_int_verb_phrase_1, is_int_verb_phrase_3
from pos.tr_verb_phrases import is_tr_verb_phrase_1, is_tr_verb_phrase_3
from structure_helpers.structure_helpers import is_branches


def is_simple_verb_phrase_1(knowledge, elements):
    """Determine if given set of words is any type of 1st-Person Verb Phrase"""

    tr_truth, tr_pos = is_tr_verb_phrase_1(knowledge, elements)
    int_truth, int_pos = is_int_verb_phrase_1(knowledge, elements)
    if tr_truth:
        return True, tr_pos
    elif int_truth:
        return True, int_pos
    return False, []


def is_simple_verb_phrase_3(knowledge, elements):
    """Determine if given set of words is any type of 3rd-Person Verb Phrase"""

    tr_truth, tr_pos = is_tr_verb_phrase_3(knowledge, elements)
    int_truth, int_pos = is_int_verb_phrase_3(knowledge, elements)
    if tr_truth:
        return True, tr_pos
    elif int_truth:
        return True, int_pos
    return False, []


def is_simple_verb_phrase(knowledge, elements):
    """Determine if given set of words is any type of Verb Phrase"""

    first_truth, first_pos = is_simple_verb_phrase_1(knowledge, elements)
    third_truth, third_pos = is_simple_verb_phrase_3(knowledge, elements)
    if first_truth:
        return True, first_pos
    elif third_truth:
        return True, third_pos
    return False, []


def is_simple_verb_phrase_1_with_adverbs(knowledge, elements):
    """
    Determine if given set of words is a VP followed by any number of adverbs
    This includes 0 adverbs
    e.g. "eat the food often quickly"
    """

    vp_truth, vp_pos = is_simple_verb_phrase_1(knowledge, elements)
    # If it is a standard VP, it is accepted
    if vp_truth:
        return True, vp_pos
    # Check to see if it is a VP + ADVP
    return is_branches(knowledge, elements, is_simple_verb_phrase_1, is_adverbs)


def is_simple_verb_phrase_3_with_adverbs(knowledge, elements):
    """
    Determine if given set of words is a VP followed by any number of adverbs
    This includes 0 adverbs
    e.g. "eats the food often quickly"
    """

    vp_truth, vp_pos = is_simple_verb_phrase_3(knowledge, elements)
    # If it is a standard VP, it is accepted
    if vp_truth:
        return True, vp_pos
    # Check to see if it is a VP + ADVP
    return is_branches(knowledge, elements, is_simple_verb_phrase_3, is_adverbs)
