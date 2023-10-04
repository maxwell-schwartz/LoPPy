import pytest

import loppy as lp
from pos.simple_verb_phrases import (
    is_simple_verb_phrase,
    is_simple_verb_phrase_1_with_adverbs,
    is_simple_verb_phrase_3_with_adverbs,
)

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("TR_VERB_1", "throw"))
knowledge.update_knowledge(lp.Fact("TR_VERB_3", "throws"))
knowledge.update_knowledge(lp.Fact("TR_VERB_1", "eat"))
knowledge.update_knowledge(lp.Fact("TR_VERB_3", "eats"))
knowledge.update_knowledge(lp.Fact("INT_VERB_1", "sleep"))
knowledge.update_knowledge(lp.Fact("INT_VERB_3", "sleeps"))
knowledge.update_knowledge(lp.Fact("DET", "the"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "food"))
knowledge.update_knowledge(lp.Fact("NOUN_P", "foods"))
knowledge.update_knowledge(lp.Fact("ADV", "often"))


@pytest.mark.parametrize(
    "elements,expected",
    [
        (
            ["often", "throw", "the", "food"],
            (True, ["ADV", "TR_VERB_1", "DET", "NOUN_S"]),
        ),
        (
            ["often", "throw", "the", "foods"],
            (True, ["ADV", "TR_VERB_1", "DET", "NOUN_P"]),
        ),
        (["often", "sleep"], (True, ["ADV", "INT_VERB_1"])),
        (["often", "sleeps"], (True, ["ADV", "INT_VERB_3"])),
    ],
)
def test_is_simple_verb_phrase(elements, expected):
    result = is_simple_verb_phrase(knowledge, elements)

    assert result == expected


def test_is_simple_verb_phrase_1_with_adverbs():
    elements = ["eat", "the", "food", "often"]

    result = is_simple_verb_phrase_1_with_adverbs(knowledge, elements)

    assert result == (True, ["TR_VERB_1", "DET", "NOUN_S", "ADV"])


def test_is_simple_verb_phrase_3_with_adverbs():
    elements = ["eats", "the", "food", "often"]

    result = is_simple_verb_phrase_3_with_adverbs(knowledge, elements)

    assert result == (True, ["TR_VERB_3", "DET", "NOUN_S", "ADV"])
