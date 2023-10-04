import pytest

import loppy as lp
from pos.determiner_phrases_with_specifier import (
    is_determiner_phrase_with_spec_and_tr_verb,
    is_determiner_phrase_with_spec_and_int_verb,
)

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("INT_VERB_1", "sleep"))
knowledge.update_knowledge(lp.Fact("INT_VERB_3", "sleeps"))
knowledge.update_knowledge(lp.Fact("TR_VERB_1", "throw"))
knowledge.update_knowledge(lp.Fact("TR_VERB_3", "throws"))
knowledge.update_knowledge(lp.Fact("DET", "the"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "cat"))
knowledge.update_knowledge(lp.Fact("NOUN_P", "cats"))
knowledge.update_knowledge(lp.Fact("ADV", "quickly"))
knowledge.update_knowledge(lp.Fact("SPEC", "that"))


@pytest.mark.parametrize(
    "elements,expected",
    [
        (
            ["the", "cat", "that", "quickly", "throws"],
            (True, ["DET", "NOUN_S", "SPEC", "ADV", "TR_VERB_3"]),
        ),
        (
            ["the", "cats", "that", "quickly", "throw"],
            (True, ["DET", "NOUN_P", "SPEC", "ADV", "TR_VERB_1"]),
        ),
    ],
)
def test_is_determiner_phrase_with_spec_and_tr_verb(elements, expected):
    result = is_determiner_phrase_with_spec_and_tr_verb(knowledge, elements)

    assert result == expected


@pytest.mark.parametrize(
    "elements,expected",
    [
        (
            ["the", "cat", "that", "quickly", "sleeps"],
            (True, ["DET", "NOUN_S", "SPEC", "ADV", "INT_VERB_3"]),
        ),
        (
            ["the", "cats", "that", "quickly", "sleep"],
            (True, ["DET", "NOUN_P", "SPEC", "ADV", "INT_VERB_1"]),
        ),
    ],
)
def test_is_determiner_phrase_with_spec_and_int_verb(elements, expected):
    result = is_determiner_phrase_with_spec_and_int_verb(knowledge, elements)

    assert result == expected
