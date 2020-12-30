def is_aux_singular(knowledge, elements):
    """Determine if a given set of words is a Singular Auxiliary Verb"""

    if len(elements) == 1 and knowledge.is_a(elements, "AUX_S"):
        return True, ["AUX_S"]
    return False, []


def is_aux_plural(knowledge, elements):
    """Determine if a given set of words is a Plural Auxiliary Verb"""

    if len(elements) == 1 and knowledge.is_a(elements, "AUX_P"):
        return True, ["AUX_P"]
    return False, []
