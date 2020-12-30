import pytest

import loppy as lp
from pos.adverbs import is_adverbs

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("ADV", "quickly"))
knowledge.update_knowledge(lp.Fact("ADV", "often"))


@pytest.mark.parametrize(
    "elements,expected",
    [
        (["quickly"], (True, ["ADV"])),
        (["often", "quickly", "quickly"], (True, ["ADV", "ADV", "ADV"])),
    ],
)
def test_is_adverbs(elements, expected):
    result = is_adverbs(knowledge, elements)

    assert result == expected
