from pos.adverbs import is_adverbs
from pos.determiner_phrases import is_determiner_phrase


def is_adverbs_with_tr_verb_1(knowledge, elements):
    """
    Determine if given set of words is an adverb phrase followed by a 1st
    Person Transitive Verb
    e.g. "often throw"
    """

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1:
        # A lone transitive verb works
        if knowledge.is_a(elements, "TR_VERB_1"):
            return True, ["TR_VERB_1"]
        return False, []
    *head, tail = elements
    adv_truth, adv_pos = is_adverbs(knowledge, head)
    if adv_truth and knowledge.is_a([tail], "TR_VERB_1"):
        return True, adv_pos + ["TR_VERB_1"]
    return False, []


def is_adverbs_with_tr_verb_3(knowledge, elements):
    """
    Determine if given set of words is an adverb phrase followed by a 3rd
    Person Transitive Verb
    e.g. "often throws"
    """

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1:
        # A lone transitive verb works
        if knowledge.is_a(elements, "TR_VERB_3"):
            return True, ["TR_VERB_3"]
        return False, []
    *head, tail = elements
    adv_truth, adv_pos = is_adverbs(knowledge, head)
    if adv_truth and knowledge.is_a([tail], "TR_VERB_3"):
        return True, adv_pos + ["TR_VERB_3"]
    return False, []


def is_tr_verb_phrase_1(knowledge, elements):
    """
    Determine if given set of words is a 1st Person Transitive Verb Phrase
    Can have any number of preceding adverbs
    e.g. "throw the food"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], "TR_VERB_1"):
        # Check if words following the transitive verb are a DP
        dp_truth, dp_pos_list = is_determiner_phrase(knowledge, tail)
        if dp_truth:
            return True, ["TR_VERB_1"] + dp_pos_list
    elif knowledge.is_a([head], "ADV"):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_tr_verb_phrase_1(knowledge, tail)
        return truth, ["ADV"] + pos_list
    return False, []


def is_tr_verb_phrase_3(knowledge, elements):
    """
    Determine if given set of words is a 3rd Person Transitive Verb Phrase
    Can have any number of preceding adverbs
    e.g. "throws the food"
    """

    if len(elements) < 2:
        return False, []
    head, *tail = elements
    if knowledge.is_a([head], "TR_VERB_3"):
        # Check if words following the transitive verb are a DP
        dp_truth, dp_pos_list = is_determiner_phrase(knowledge, tail)
        if dp_truth:
            return True, ["TR_VERB_3"] + dp_pos_list
    elif knowledge.is_a([head], "ADV"):
        # Any number of adverbs can precede the verb
        truth, pos_list = is_tr_verb_phrase_3(knowledge, tail)
        return truth, ["ADV"] + pos_list
    return False, []
