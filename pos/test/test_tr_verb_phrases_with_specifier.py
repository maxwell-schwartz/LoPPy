import loppy as lp
from pos.tr_verb_phrases_with_specifier import is_tr_verb_phrase_3_with_specifier

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("TR_VERB_3", "eats"))
knowledge.update_knowledge(lp.Fact("DET", "the"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "bird"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "food"))
knowledge.update_knowledge(lp.Fact("SPEC", "that"))


def test_is_tr_verb_phrase_3_with_specifier():
    elements = ["eats", "the", "bird", "that", "eats", "the", "food"]

    result = is_tr_verb_phrase_3_with_specifier(knowledge, elements)

    assert result == (
        True,
        ["TR_VERB_3", "DET", "NOUN_S", "SPEC", "TR_VERB_3", "DET", "NOUN_S"],
    )
