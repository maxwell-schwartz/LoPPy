from pos.complex_determiner_phrases import is_complex_determiner_phrase_singular, is_complex_determiner_phrase_plural, \
    is_complex_determiner_phrase
from pos.determiner_phrases import is_determiner_phrase_singular, is_determiner_phrase_plural, is_determiner_phrase


def is_subject_singular(knowledge, elements):
    """
    Determine if given set of words is a viable Singular Subject for a sentence
    DP | Specifier Phrase | Specifier Phrase + ADVP
    """

    dp_truth, dp_pos = is_determiner_phrase_singular(knowledge, elements)
    spec_truth, spec_pos = is_complex_determiner_phrase_singular(knowledge, elements)
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []


def is_subject_plural(knowledge, elements):
    """
    Determine if given set of words is a viable Plural Subject for a sentence
    DP | Specifier Phrase | Specifier Phrase + ADVP
    """

    dp_truth, dp_pos = is_determiner_phrase_plural(knowledge, elements)
    spec_truth, spec_pos = is_complex_determiner_phrase_plural(knowledge, elements)
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []


def is_subject(knowledge, elements):
    """
    Determine if given set of words is a viable Subject for a sentence
    DP | Specifier Phrase | Specifier Phrase + ADVP
    """

    dp_truth, dp_pos = is_determiner_phrase(knowledge, elements)
    spec_truth, spec_pos = is_complex_determiner_phrase(knowledge, elements)
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []