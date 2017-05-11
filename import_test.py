# Testing the functionality

import loppy

def main():

    knowledge = loppy.FactTracker()
    knowledge.update_knowledge(loppy.Fact('is tired', 'Max'))
    knowledge.update_knowledge(loppy.Fact('ready for bed', 'Max'))
    knowledge.update_knowledge(loppy.Fact('ready for bed', 'Most People'))

    tired_and_ready = knowledge.solve_full(loppy.Fact('is tired', '?who'), 
                        loppy.Fact('ready for bed', '?who'))
    for t in tired_and_ready:
        print(t)

    ready = knowledge.solve_one(loppy.Fact('ready for bed', '?X'))
    for r in ready:
        print(r)


main()