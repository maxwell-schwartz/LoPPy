def is_wh_word(knowledge, elements):
    """
    Determine if given set of words is a WH-word

    To Do: deal with preposition cases, e.g. To what...
    """

    if len(elements) == 0:
        return False, []
    elif len(elements) == 1 and knowledge.is_a(elements, 'WH'):
        return True, ['WH']
    return False, []


def is_wh_subject_word(knowledge, elements):
    """
    Determine if given set of words is a WH-word that can serve as a subject
    Specifically: "who" and "what"
    """

    if len(elements) == 1 and knowledge.is_a(elements, 'WH_S'):
        return True, ['WH_S']
    return False, []
