import pytest

import loppy as lp
from pos.int_verb_phrases import is_int_verb_phrase_1, is_int_verb_phrase_3

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("INT_VERB_1", "dance"))
knowledge.update_knowledge(lp.Fact("INT_VERB_3", "dances"))
knowledge.update_knowledge(lp.Fact("ADV", "often"))
knowledge.update_knowledge(lp.Fact("ADV", "quickly"))


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["dance"], (True, ["INT_VERB_1"])),
        (["often", "quickly", "dance"], (True, ["ADV", "ADV", "INT_VERB_1"])),
    ],
)
def test_is_int_verb_phrase_1(elements, expected):
    result = is_int_verb_phrase_1(knowledge, elements)

    assert result == expected


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["dances"], (True, ["INT_VERB_3"])),
        (["often", "quickly", "dances"], (True, ["ADV", "ADV", "INT_VERB_3"])),
    ],
)
def test_is_int_verb_phrase_3(elements, expected):
    result = is_int_verb_phrase_3(knowledge, elements)

    assert result == expected
