import pytest

import loppy as lp
from pos.noun_phrases import is_np_s, is_np_p

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("NOUN_S", "dog"))
knowledge.update_knowledge(lp.Fact("NOUN_P", "dogs"))
knowledge.update_knowledge(lp.Fact("ADJ", "small"))
knowledge.update_knowledge(lp.Fact("ADJ", "blue"))


@pytest.mark.parametrize("elements,expected", [
    (["dog"], (True, ["NOUN_S"])),
    (["small", "dog"], (True, ["ADJ", "NOUN_S"])),
    (["small", "blue", "dog"], (True, ["ADJ", "ADJ", "NOUN_S"])),
])
def test_is_np_s(elements, expected):
    result = is_np_s(knowledge, elements)

    assert result == expected


@pytest.mark.parametrize("elements,expected", [
    (["dogs"], (True, ["NOUN_P"])),
    (["small", "dogs"], (True, ["ADJ", "NOUN_P"])),
    (["small", "blue", "dogs"], (True, ["ADJ", "ADJ", "NOUN_P"])),
])
def test_is_np_p(elements, expected):
    result = is_np_p(knowledge, elements)

    assert result == expected
