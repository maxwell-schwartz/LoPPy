# Some examples of the functionality

from loppy import *

def main():
    # My actual family members

    tracker = FactTracker()
    tracker.update_knowledge(Fact('child', 'Max', 'Jan', 'Ellen'))
    tracker.update_knowledge(Fact('child', 'Dash', 'Jan', 'Ellen'))
    tracker.update_knowledge(Fact('child', 'Rocky', 'Jan', 'Ellen'))
    tracker.update_knowledge(Fact('spouse', 'Jan', 'Ellen'))
    tracker.update_knowledge(Fact('brother', 'Max', 'Dash'))
    tracker.update_knowledge(Fact('brother', 'Max', 'Rocky'))
    tracker.update_knowledge(Fact('brother', 'Dash', 'Rocky'))
    
    for i in (tracker.solve_full(Fact('child', '?X', 'Jan', 'Ellen'), 
                Fact('brother', '?X', 'Rocky'))):
        print(i)

if __name__ == '__main__':
    main()