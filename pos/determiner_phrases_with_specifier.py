from pos.determiner_phrases import (
    is_determiner_phrase_singular,
    is_determiner_phrase_plural,
)
from pos.specifiers import (
    is_specifier_with_tr_verb_3,
    is_specifier_with_tr_verb_1,
    is_specifier_with_int_verb_3,
    is_specifier_with_int_verb_1,
)
from structure_helpers.structure_helpers import is_branches


def is_determiner_phrase_singular_with_spec_and_tr_verb(knowledge, elements):
    """
    Determine if given set of words is a Singular Determiner Phrase
    with a Specifier and 3rd Person Transitive Verb
    e.g. "the cat that quickly throws"
    """

    return is_branches(
        knowledge, elements, is_determiner_phrase_singular, is_specifier_with_tr_verb_3
    )


def is_determiner_phrase_plural_with_spec_and_tr_verb(knowledge, elements):
    """
    Determine if given set of words is a Plural Determiner Phrase
    with a Specifier and 1st Person Transitive Verb
    e.g. "the cats that quickly throw"
    """

    return is_branches(
        knowledge, elements, is_determiner_phrase_plural, is_specifier_with_tr_verb_1
    )


def is_determiner_phrase_with_spec_and_tr_verb(knowledge, elements):
    """
    Determine if given set of words is any type of Determiner Phrase
    with a Specifier and Transitive Verb
    Singular or Plural
    """

    s_truth, s_pos = is_determiner_phrase_singular_with_spec_and_tr_verb(
        knowledge, elements
    )
    p_truth, p_pos = is_determiner_phrase_plural_with_spec_and_tr_verb(
        knowledge, elements
    )
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []


def is_determiner_phrase_singular_with_spec_and_int_verb(knowledge, elements):
    """
    Determine if given set of words is a Singular Determiner Phrase
    with a Specifier and 3rd Person Intransitive Verb
    e.g. "the cat that quickly sleeps"
    """

    return is_branches(
        knowledge, elements, is_determiner_phrase_singular, is_specifier_with_int_verb_3
    )


def is_determiner_phrase_plural_with_spec_and_int_verb(knowledge, elements):
    """
    Determine if given set of words is a Plural Determiner Phrase
    with a Specifier and 1st Person Intransitive Verb
    e.g. "the cats that quickly sleep"
    """

    return is_branches(
        knowledge, elements, is_determiner_phrase_plural, is_specifier_with_int_verb_1
    )


def is_determiner_phrase_with_spec_and_int_verb(knowledge, elements):
    """
    Determine if given set of words is a Determiner Phrase
    with a Specifier
    Singular or Plural
    """

    s_truth, s_pos = is_determiner_phrase_singular_with_spec_and_int_verb(
        knowledge, elements
    )
    p_truth, p_pos = is_determiner_phrase_plural_with_spec_and_int_verb(
        knowledge, elements
    )
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []
