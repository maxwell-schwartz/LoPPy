import loppy as lp
from pos.auxiliary import is_aux_singular, is_aux_plural

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("AUX_S", "does"))
knowledge.update_knowledge(lp.Fact("AUX_P", "do"))


def test_is_aux_singular():
    elements = ["does"]

    result = is_aux_singular(knowledge, elements)

    assert result == (True, ["AUX_S"])


def test_is_aux_plural():
    elements = ["do"]

    result = is_aux_plural(knowledge, elements)

    assert result == (True, ["AUX_P"])
