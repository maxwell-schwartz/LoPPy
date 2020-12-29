import pytest

import loppy as lp
from pos.tr_verb_phrases import (
    is_adverbs_with_tr_verb_1,
    is_adverbs_with_tr_verb_3,
    is_tr_verb_phrase_1,
    is_tr_verb_phrase_3,
)

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("TR_VERB_1", "throw"))
knowledge.update_knowledge(lp.Fact("TR_VERB_3", "throws"))
knowledge.update_knowledge(lp.Fact("DET", "the"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "food"))
knowledge.update_knowledge(lp.Fact("NOUN_P", "foods"))
knowledge.update_knowledge(lp.Fact("ADV", "often"))


def test_is_adverbs_with_tr_verb_1():
    elements = ["often", "throw"]

    result = is_adverbs_with_tr_verb_1(knowledge, elements)

    assert result == (True, ["ADV", "TR_VERB_1"])


def test_is_adverbs_with_tr_verb_3():
    elements = ["often", "throws"]

    result = is_adverbs_with_tr_verb_3(knowledge, elements)

    assert result == (True, ["ADV", "TR_VERB_3"])


@pytest.mark.parametrize("elements,expected", [
    (["often", "throw", "the", "food"], (True, ["ADV", "TR_VERB_1", "DET", "NOUN_S"])),
    (["often", "throw", "the", "foods"], (True, ["ADV", "TR_VERB_1", "DET", "NOUN_P"])),
])
def test_is_tr_verb_phrase_1(elements, expected):
    result = is_tr_verb_phrase_1(knowledge, elements)

    assert result == expected


@pytest.mark.parametrize("elements,expected", [
    (["often", "throws", "the", "food"], (True, ["ADV", "TR_VERB_3", "DET", "NOUN_S"])),
    (["often", "throws", "the", "foods"], (True, ["ADV", "TR_VERB_3", "DET", "NOUN_P"])),
])
def test_is_tr_verb_phrase_3(elements, expected):
    result = is_tr_verb_phrase_3(knowledge, elements)

    assert result == expected
