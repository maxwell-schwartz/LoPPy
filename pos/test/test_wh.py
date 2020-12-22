import loppy as lp
from pos.wh import is_wh_word, is_wh_subject_word

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("WH", "why"))
knowledge.update_knowledge(lp.Fact("WH_S", "who"))


def test_is_wh_word():
    elements = ["why"]

    result = is_wh_word(knowledge, elements)

    assert result == (True, ["WH"])


def test_is_wh_subject_word():
    elements = ["who"]

    result = is_wh_subject_word(knowledge, elements)

    assert result == (True, ["WH_S"])
