import pytest

import loppy as lp
from pos.determiner_phrases import is_dp_s, is_dp_p

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("DET", "the"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "dog"))
knowledge.update_knowledge(lp.Fact("NOUN_P", "dogs"))
knowledge.update_knowledge(lp.Fact("ADJ", "small"))
knowledge.update_knowledge(lp.Fact("ADJ", "blue"))


@pytest.mark.parametrize("elements,expected", [
    (["the", "dog"], (True, ["DET", "NOUN_S"])),
    (["the", "small", "dog"], (True, ["DET", "ADJ", "NOUN_S"])),
    (["the", "small", "blue", "dog"], (True, ["DET", "ADJ", "ADJ", "NOUN_S"])),
])
def test_is_dp_s(elements, expected):
    result = is_dp_s(knowledge, elements)

    assert result == expected


@pytest.mark.parametrize("elements,expected", [
    (["the", "dogs"], (True, ["DET", "NOUN_P"])),
    (["the", "small", "dogs"], (True, ["DET", "ADJ", "NOUN_P"])),
    (["the", "small", "blue", "dogs"], (True, ["DET", "ADJ", "ADJ", "NOUN_P"])),
])
def test_is_dp_p(elements, expected):
    result = is_dp_p(knowledge, elements)

    assert result == expected
