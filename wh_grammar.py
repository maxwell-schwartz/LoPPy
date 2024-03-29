import loppy as lp
from pos.auxiliary import is_aux_singular, is_aux_plural
from pos.int_verb_phrases import is_int_verb_phrase_1
from pos.simple_verb_phrases import is_simple_verb_phrase_3_with_adverbs
from pos.tr_verb_phrases import is_adverbs_with_tr_verb_1
from pos.tr_verb_phrases_with_specifier import is_tr_verb_phrase_3_with_specifier
from sentence_pieces.subjects import is_subject_singular, is_subject_plural, is_subject
from structure_helpers.structure_helpers import is_branches, is_wrapped
from pos.wh import is_wh_word, is_wh_subject_word


def is_predicate(knowledge, elements):
    """
    Determine if given set of words is a viable Predicate for a sentence
    VP | VP + ADVP | Tr_VP + Specifier | Tr_VP + Specifier + ADVP
    """
    vp_truth, vp_pos = is_simple_verb_phrase_3_with_adverbs(knowledge, elements)
    tr_sp_truth, tr_sp_pos = is_tr_verb_phrase_3_with_specifier(knowledge, elements)
    if vp_truth:
        return True, vp_pos
    elif tr_sp_truth:
        return True, tr_sp_pos
    return False, []


def is_int_aux_phrase_s(knowledge, elements):
    """
    Determine if a given set of words is a Singular Intransitive Auxiliary Verb Phrase
    e.g. "does the bird sleep"
    """

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(
        knowledge, elements, is_aux_singular, is_subject_singular, is_int_verb_phrase_1
    )
    if aux_truth:
        return True, aux_pos
    return False, []


def is_int_aux_phrase_p(knowledge, elements):
    """
    Determine if a given set of words is a Plural Intransitive Auxiliary Verb Phrase
    e.g. "do the birds sleep"
    """

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(
        knowledge, elements, is_aux_plural, is_subject_plural, is_int_verb_phrase_1
    )
    if aux_truth:
        return True, aux_pos
    return False, []


def is_int_aux_phrase(knowledge, elements):
    """
    Determine if a given set of words is any Intransitive Auxiliary Verb Phrase
    Singular or Plural
    """

    s_truth, s_pos = is_int_aux_phrase_s(knowledge, elements)
    p_truth, p_pos = is_int_aux_phrase_p(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []


def is_tr_aux_phrase_s(knowledge, elements):
    """
    Determine if a given set of words is a Singular Transitive Auxiliary Verb Phrase
    e.g. "does the bird throw"
    """

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(
        knowledge, elements, is_aux_singular, is_subject_singular, is_adverbs_with_tr_verb_1
    )
    if aux_truth:
        return True, aux_pos
    return False, []


def is_tr_aux_phrase_p(knowledge, elements):
    """
    Determine if a given set of words is a Plural Transitive Auxiliary Verb Phrase
    e.g. "do the birds throw"
    """

    if len(elements) < 3:
        return False, []

    aux_truth, aux_pos = is_wrapped(
        knowledge, elements, is_aux_plural, is_subject_plural, is_adverbs_with_tr_verb_1
    )
    if aux_truth:
        return True, aux_pos
    return False, []


def is_tr_aux_phrase(knowledge, elements):
    """
    Determine if a given set of words is any Transitive Auxiliary Verb Phrase
    Singular or Plural
    """

    s_truth, s_pos = is_tr_aux_phrase_s(knowledge, elements)
    p_truth, p_pos = is_tr_aux_phrase_p(knowledge, elements)
    if s_truth:
        return True, s_pos
    elif p_truth:
        return True, p_pos
    return False, []


def is_aux_phrase(knowledge, elements):
    """
    Determine if given set of words is any complete Auxiliary Verb Phrase
    Transitive or Intransitive
    """

    int_truth, int_pos = is_int_aux_phrase(knowledge, elements)
    if int_truth:
        return True, int_pos
    return is_branches(knowledge, elements, is_tr_aux_phrase, is_subject)


def is_wh_question(knowledge, elements):
    """
    Determine if given set of words is a grammatical wh-question
    """

    if len(elements) < 2:
        return False, []

    subj_truth, subj_pos = is_branches(
        knowledge, elements, is_wh_subject_word, is_predicate
    )
    int_aux_truth, int_aux_pos = is_branches(
        knowledge, elements, is_wh_subject_word, is_int_aux_phrase
    )
    aux_truth, aux_pos = is_branches(knowledge, elements, is_wh_word, is_aux_phrase)
    if subj_truth:
        return True, subj_pos
    elif int_aux_truth:
        return True, int_aux_pos
    elif aux_truth:
        return True, aux_pos
    return False, []


def is_wh_question_with_adv(knowledge, elements):
    """
    Determine if given set of words is a wh-question plus 0 or 1 adverbs
    e.g. "what does the bird eat quickly"
    """

    *head, tail = elements
    wh_question_truth, wh_question_pos = is_wh_question(knowledge, head)
    if wh_question_truth and knowledge.is_a([tail], "ADV"):
        return wh_question_pos + ["ADV"]

    return is_wh_question(knowledge, elements)


def main():
    # Test
    knowledge = lp.FactTracker()
    with open("word_lists/nouns_singular.txt", "r") as infile:
        nouns_s = infile.readlines()
    with open("word_lists/nouns_plural.txt", "r") as infile:
        nouns_p = infile.readlines()
    with open("word_lists/transitive_verbs_1st.txt", "r") as infile:
        tr_verbs_1 = infile.readlines()
    with open("word_lists/transitive_verbs_3rd.txt", "r") as infile:
        tr_verbs_3 = infile.readlines()
    with open("word_lists/intransitive_verbs_1st.txt", "r") as infile:
        int_verbs_1 = infile.readlines()
    with open("word_lists/intransitive_verbs_3rd.txt", "r") as infile:
        int_verbs_3 = infile.readlines()
    with open("word_lists/auxiliary_verbs_singular.txt", "r") as infile:
        aux_verbs_s = infile.readlines()
    with open("word_lists/auxiliary_verbs_plural.txt", "r") as infile:
        aux_verbs_p = infile.readlines()
    with open("word_lists/adjectives.txt", "r") as infile:
        adjectives = infile.readlines()
    with open("word_lists/adverbs.txt", "r") as infile:
        adverbs = infile.readlines()
    with open("word_lists/determiners.txt", "r") as infile:
        determiners = infile.readlines()
    with open("word_lists/specifiers.txt", "r") as infile:
        specifiers = infile.readlines()
    with open("word_lists/wh_words.txt", "r") as infile:
        wh_words = infile.readlines()
    with open("word_lists/wh_subject_words.txt", "r") as infile:
        wh_subject_words = infile.readlines()

    for ns in nouns_s:
        knowledge.update_knowledge(lp.Fact("NOUN_S", ns.strip()))
    for np in nouns_p:
        knowledge.update_knowledge(lp.Fact("NOUN_P", np.strip()))
    for t1 in tr_verbs_1:
        knowledge.update_knowledge(lp.Fact("TR_VERB_1", t1.strip()))
    for t3 in tr_verbs_3:
        knowledge.update_knowledge(lp.Fact("TR_VERB_3", t3.strip()))
    for i1 in int_verbs_1:
        knowledge.update_knowledge(lp.Fact("INT_VERB_1", i1.strip()))
    for i3 in int_verbs_3:
        knowledge.update_knowledge(lp.Fact("INT_VERB_3", i3.strip()))
    for aux_s in aux_verbs_s:
        knowledge.update_knowledge(lp.Fact("AUX_S", aux_s.strip()))
    for aux_p in aux_verbs_p:
        knowledge.update_knowledge(lp.Fact("AUX_P", aux_p.strip()))
    for adj in adjectives:
        knowledge.update_knowledge(lp.Fact("ADJ", adj.strip()))
    for adv in adverbs:
        knowledge.update_knowledge(lp.Fact("ADV", adv.strip()))
    for d in determiners:
        knowledge.update_knowledge(lp.Fact("DET", d.strip()))
    for s in specifiers:
        knowledge.update_knowledge(lp.Fact("SPEC", s.strip()))
    for w in wh_words:
        knowledge.update_knowledge(lp.Fact("WH", w.strip()))
    for ws in wh_subject_words:
        knowledge.update_knowledge(lp.Fact("WH_S", ws.strip()))

    keep_going = "y"
    while keep_going == "y":
        user_sent = input("Enter wh-question >> ").split()
        print("Wh question >", is_wh_question_with_adv(knowledge, user_sent))
        keep_going = input("Continue? (y/n) ")


if __name__ == "__main__":
    main()
