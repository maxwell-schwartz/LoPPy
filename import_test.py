# Testing the functionality

import loppy

def main():
    # I may have written this while very tired...

    knowledge = loppy.FactTracker()
    knowledge.update_knowledge(loppy.Fact('is tired', 'Max'))
    knowledge.update_knowledge(loppy.Fact('ready for bed', 'Max'))
    knowledge.update_knowledge(loppy.Fact('ready for bed', 'Most People'))

    print(knowledge.get_types('Max'))

    # tired_and_ready = knowledge.solve_full(loppy.Fact('is tired', '?who'), 
    #                     loppy.Fact('ready for bed', '?who'))
    # for t in tired_and_ready:
    #     print('{} = tired and ready for bed.'.format(t[0][1]))

    # ready = knowledge.solve_one(loppy.Fact('ready for bed', '?X'))
    # for r in ready:
    #     print('{} = ready for bed.'.format(r[0][1]))


main()