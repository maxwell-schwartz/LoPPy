def is_adverbs(knowledge, elements):
    """
    Determine if given set of words is a series of Adverbs
    e.g. "often quickly"
    """

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, "ADV"):
        return True, ["ADV"]
    head, *tail = elements
    if knowledge.is_a([head], "ADV"):
        truth, pos_list = is_adverbs(knowledge, tail)
        return truth, ["ADV"] + pos_list
    return False, []
