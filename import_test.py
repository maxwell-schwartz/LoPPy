# Testing the functionality

import loppy as lp

def main():
    # I may have written this while very tired...

    knowledge = lp.FactTracker()
    knowledge.update_knowledge(lp.Fact('is tired', 'Max'))
    knowledge.update_knowledge(lp.Fact('ready for bed', 'Max'))
    knowledge.update_knowledge(lp.Fact('ready for bed', 'Most People'))

    print(knowledge.get_types(['Max']))
    print(knowledge.is_a(['Most People'], 'ready for bed'))
    # print(knowledge.is_a('Most Poeple', 'is tired'))

    # tired_and_ready = knowledge.solve_full(lp.Fact('is tired', '?who'), 
    #                     lp.Fact('ready for bed', '?who'))
    # for t in tired_and_ready:
    #     print('{} = tired and ready for bed.'.format(t[0][1]))

    # ready = knowledge.solve_one(lp.Fact('ready for bed', '?X'))
    # for r in ready:
    #     print('{} = ready for bed.'.format(r[0][1]))


main()