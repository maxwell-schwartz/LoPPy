import pytest

import loppy as lp
from pos.determiner_phrases import is_determiner_phrase_singular, is_determiner_phrase_plural

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
def test_is_determiner_phrase_singular(elements, expected):
    result = is_determiner_phrase_singular(knowledge, elements)

    assert result == expected


@pytest.mark.parametrize("elements,expected", [
    (["the", "dogs"], (True, ["DET", "NOUN_P"])),
    (["the", "small", "dogs"], (True, ["DET", "ADJ", "NOUN_P"])),
    (["the", "small", "blue", "dogs"], (True, ["DET", "ADJ", "ADJ", "NOUN_P"])),
])
def test_is_determiner_phrase_plural(elements, expected):
    result = is_determiner_phrase_plural(knowledge, elements)

    assert result == expected
