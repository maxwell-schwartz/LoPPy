import pytest

import loppy as lp
from pos.complex_determiner_phrases import (
    is_complex_determiner_phrase_singular,
    is_complex_determiner_phrase_plural,
    is_complex_determiner_phrase,
)

knowledge = lp.FactTracker()
knowledge.update_knowledge(lp.Fact("TR_VERB_1", "eat"))
knowledge.update_knowledge(lp.Fact("TR_VERB_3", "eats"))
knowledge.update_knowledge(lp.Fact("DET", "the"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "cat"))
knowledge.update_knowledge(lp.Fact("NOUN_P", "cats"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "bird"))
knowledge.update_knowledge(lp.Fact("NOUN_S", "food"))
knowledge.update_knowledge(lp.Fact("ADV", "quickly"))
knowledge.update_knowledge(lp.Fact("SPEC", "that"))


def test_is_complex_determiner_phrase_singular():
    elements = [
        "the",
        "cat",
        "that",
        "eats",
        "the",
        "bird",
        "that",
        "eats",
        "the",
        "food",
        "quickly",
    ]

    result = is_complex_determiner_phrase_singular(knowledge, elements)

    assert result == (
        True,
        [
            "DET",
            "NOUN_S",
            "SPEC",
            "TR_VERB_3",
            "DET",
            "NOUN_S",
            "SPEC",
            "TR_VERB_3",
            "DET",
            "NOUN_S",
            "ADV",
        ],
    )


def test_is_complex_determiner_phrase_plural():
    elements = [
        "the",
        "cats",
        "that",
        "eat",
        "the",
        "bird",
        "that",
        "eats",
        "the",
        "food",
        "quickly",
    ]

    result = is_complex_determiner_phrase_plural(knowledge, elements)

    assert result == (
        True,
        [
            "DET",
            "NOUN_P",
            "SPEC",
            "TR_VERB_1",
            "DET",
            "NOUN_S",
            "SPEC",
            "TR_VERB_3",
            "DET",
            "NOUN_S",
            "ADV",
        ],
    )


@pytest.mark.parametrize(
    "elements,expected",
    [
        (
            [
                "the",
                "cat",
                "that",
                "eats",
                "the",
                "bird",
                "that",
                "eats",
                "the",
                "food",
                "quickly",
            ],
            (
                True,
                [
                    "DET",
                    "NOUN_S",
                    "SPEC",
                    "TR_VERB_3",
                    "DET",
                    "NOUN_S",
                    "SPEC",
                    "TR_VERB_3",
                    "DET",
                    "NOUN_S",
                    "ADV",
                ],
            ),
        ),
        (
            [
                "the",
                "cats",
                "that",
                "eat",
                "the",
                "bird",
                "that",
                "eats",
                "the",
                "food",
                "quickly",
            ],
            (
                True,
                [
                    "DET",
                    "NOUN_P",
                    "SPEC",
                    "TR_VERB_1",
                    "DET",
                    "NOUN_S",
                    "SPEC",
                    "TR_VERB_3",
                    "DET",
                    "NOUN_S",
                    "ADV",
                ],
            ),
        ),
    ],
)
def test_is_complex_determiner_phrase(elements, expected):
    result = is_complex_determiner_phrase(knowledge, elements)

    assert result == expected
