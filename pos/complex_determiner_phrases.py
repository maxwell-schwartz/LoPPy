from pos.adverbs import is_adverbs
from pos.determiner_phrases import is_determiner_phrase
from pos.determiner_phrases_with_specifier import (
    is_determiner_phrase_plural_with_spec_and_tr_verb,
    is_determiner_phrase_plural_with_spec_and_int_verb,
    is_determiner_phrase_singular_with_spec_and_tr_verb,
    is_determiner_phrase_singular_with_spec_and_int_verb,
    is_determiner_phrase_with_spec_and_tr_verb,
    is_determiner_phrase_with_spec_and_int_verb,
)
from structure_helpers.structure_helpers import is_branches


def _is_spec_ender(knowledge, elements):
    """
    Determine if a given set of words can serve to end a Specifier Phrase
    This can be any Determiner Phrase or DP with a Spec and Intransitive Verb
    """

    dp_truth, dp_pos = is_determiner_phrase(knowledge, elements)
    spec_truth, spec_pos = is_determiner_phrase_with_spec_and_int_verb(
        knowledge, elements
    )
    if dp_truth:
        return True, dp_pos
    elif spec_truth:
        return True, spec_pos
    return False, []


def _is_complete_determiner_phrase_with_specifier(knowledge, elements):
    """
    Determine if given set of words is a Complete Determiner Phrase with a Specifier
    e.g. "the cat that eats the bird that eats the food"
    """

    if len(elements) < 3:
        return False, []
    # Any single Intransitive Phrase will work
    int_truth, int_pos = is_determiner_phrase_with_spec_and_int_verb(
        knowledge, elements
    )
    if int_truth:
        return True, int_pos
    tr_truth, tr_pos = is_branches(
        knowledge, elements, is_determiner_phrase_with_spec_and_tr_verb, _is_spec_ender
    )
    if tr_truth:
        return True, tr_pos
    nested_truth, nested_pos = is_branches(
        knowledge,
        elements,
        is_determiner_phrase_with_spec_and_tr_verb,
        _is_complete_determiner_phrase_with_specifier,
    )
    if nested_truth:
        return True, nested_pos
    return False, []


def _is_complete_determiner_phrase_with_specifier_singular(knowledge, elements):
    """
    Determine if given set of words is a Complete Determiner Phrase with a Specifier (Singular)
    e.g. "the cat that eats the bird"
    """

    if len(elements) < 3:
        return False, []
    # Any single Intransitive Phrase will work
    int_truth, int_pos = is_determiner_phrase_singular_with_spec_and_int_verb(
        knowledge, elements
    )
    if int_truth:
        return True, int_pos
    tr_truth, tr_pos = is_branches(
        knowledge,
        elements,
        is_determiner_phrase_singular_with_spec_and_tr_verb,
        _is_spec_ender,
    )
    if tr_truth:
        return True, tr_pos
    nested_truth, nested_pos = is_branches(
        knowledge,
        elements,
        is_determiner_phrase_singular_with_spec_and_tr_verb,
        _is_complete_determiner_phrase_with_specifier,
    )
    if nested_truth:
        return True, nested_pos
    return False, []


def _is_complete_determiner_phrase_with_specifier_plural(knowledge, elements):
    """
    Determine if given set of words is a Complete Determiner Phrase with a Specifier (Plural)
    e.g. "the cats that eat the bird"
    """

    if len(elements) < 3:
        return False, []
    # Any single Intransitive Phrase will work
    int_truth, int_pos = is_determiner_phrase_plural_with_spec_and_int_verb(
        knowledge, elements
    )
    if int_truth:
        return True, int_pos
    tr_truth, tr_pos = is_branches(
        knowledge,
        elements,
        is_determiner_phrase_plural_with_spec_and_tr_verb,
        _is_spec_ender,
    )
    if tr_truth:
        return True, tr_pos
    nested_truth, nested_pos = is_branches(
        knowledge,
        elements,
        is_determiner_phrase_plural_with_spec_and_tr_verb,
        _is_complete_determiner_phrase_with_specifier,
    )
    if nested_truth:
        return True, nested_pos
    return False, []


def is_complex_determiner_phrase_singular(knowledge, elements):
    """
    Determine if given set of words is a Complex Determiner Phrase (Singular)
    followed by any number of adverbs
    This includes 0 adverbs
    e.g. "the cat that eats the bird that eats the food quickly"
    """

    sp_truth, sp_pos = _is_complete_determiner_phrase_with_specifier_singular(
        knowledge, elements
    )
    # If it is a standard Specifier Phrase, it is accepted
    if sp_truth:
        return True, sp_pos
    # Check to see if it is a Specifier + ADVP
    return is_branches(
        knowledge,
        elements,
        _is_complete_determiner_phrase_with_specifier_singular,
        is_adverbs,
    )


def is_complex_determiner_phrase_plural(knowledge, elements):
    """
    Determine if given set of words is a Complex Determiner Phrase (Plural)
    followed by any number of adverbs
    This includes 0 adverbs
    e.g. "the cats that eat the bird that eats the food quickly"
    """

    sp_truth, sp_pos = _is_complete_determiner_phrase_with_specifier_plural(
        knowledge, elements
    )
    # If it is a standard Specifier Phrase, it is accepted
    if sp_truth:
        return True, sp_pos
    # Check to see if it is a Specifier + ADVP
    return is_branches(
        knowledge,
        elements,
        _is_complete_determiner_phrase_with_specifier_plural,
        is_adverbs,
    )


def is_complex_determiner_phrase(knowledge, elements):
    """
    Determine if given set of words is a Complex Determiner Phrase (Singular or Plural)
    followed by any number of adverbs
    This includes 0 adverbs
    e.g. "the cat that eats the bird that eats the food quickly"
    """

    sp_truth, sp_pos = _is_complete_determiner_phrase_with_specifier(
        knowledge, elements
    )
    # If it is a standard Specifier Phrase, it is accepted
    if sp_truth:
        return True, sp_pos
    # Check to see if it is a Specifier + ADVP
    return is_branches(
        knowledge, elements, _is_complete_determiner_phrase_with_specifier, is_adverbs
    )
