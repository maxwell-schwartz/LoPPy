import loppy as lp
from pos.specifiers import (
    is_specifier_with_tr_verb_1,
    is_specifier_with_tr_verb_3,
    is_specifier_with_int_verb_1,
    is_specifier_with_int_verb_3,
)

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("SPEC", "that"))
knowledge.update_knowledge(lp.Fact("TR_VERB_1", "throw"))
knowledge.update_knowledge(lp.Fact("TR_VERB_3", "throws"))
knowledge.update_knowledge(lp.Fact("INT_VERB_1", "sleep"))
knowledge.update_knowledge(lp.Fact("INT_VERB_3", "sleeps"))
knowledge.update_knowledge(lp.Fact("ADV", "often"))


def test_is_specifier_with_tr_verb_1():
    elements = ["that", "often", "throw"]

    result = is_specifier_with_tr_verb_1(knowledge, elements)

    assert result == (True, ["SPEC", "ADV", "TR_VERB_1"])


def test_is_specifier_with_tr_verb_3():
    elements = ["that", "often", "throws"]

    result = is_specifier_with_tr_verb_3(knowledge, elements)

    assert result == (True, ["SPEC", "ADV", "TR_VERB_3"])


def test_is_specifier_with_int_verb_1():
    elements = ["that", "often", "sleep"]

    result = is_specifier_with_int_verb_1(knowledge, elements)

    assert result == (True, ["SPEC", "ADV", "INT_VERB_1"])


def test_is_specifier_with_int_verb_3():
    elements = ["that", "often", "sleeps"]

    result = is_specifier_with_int_verb_3(knowledge, elements)

    assert result == (True, ["SPEC", "ADV", "INT_VERB_3"])
