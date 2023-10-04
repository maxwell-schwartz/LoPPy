# Some examples of the functionality

import loppy as lp


def main():
    # I may have written this while very tired...

    knowledge = lp.FactTracker()
    knowledge.update_knowledge(lp.Fact("is tired", "Max"))
    knowledge.update_knowledge(lp.Fact("ready for bed", "Max"))
    knowledge.update_knowledge(lp.Fact("ready for bed", "Most People"))

    # Get all the "types" or rules the given element list satisfies
    print('Types of "Max" > ', knowledge.get_types(["Max"]))
    # Find out whether or not a given element list satisfies a rule
    print(
        'Is it true that "Most People" satisfies the rule "ready for bed"? ',
        knowledge.is_a(["Most People"], "ready for bed"),
    )
    # Get all elements that are true for a given set of rules
    tired_and_ready = knowledge.solve_full(
        lp.Fact("is tired", "?who"), lp.Fact("ready for bed", "?who")
    )
    for t in tired_and_ready:
        print(t)
    # Get all elements that are true for a given rule
    ready = knowledge.solve_one(lp.Fact("ready for bed", "?X"))
    for r in ready:
        print(r)


if __name__ == "__main__":
    main()
