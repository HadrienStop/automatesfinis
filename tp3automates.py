#!/usr/bin/env python3
"""
Applies Kleene's star, concatenation and union of automata.
"""

from automaton import Automaton, EPSILON, State, error, warn
import sys
import pdb  # for debugging


##################
def nouvel_etat(a1: Automaton) -> str:
    maxstate = -1
    for a in a1.states:
        try:
            maxstate = max(int(a), maxstate)
        except ValueError:
            pass
    return str(maxstate + 1)


def kleene(a1: Automaton) -> Automaton:
    a1star = a1.deepcopy()
    a1star.name = "a1star"
    for index in a1star.acceptstates:
        a1star.add_transition(a1star.acceptstates[index], EPSILON, a1star.initial.name)
    nom_nouvel_etat = nouvel_etat(a1star)
    a1star.add_transition(nom_nouvel_etat, EPSILON, a1.initial.name)
    a1star.initial = a1star.statesdict[nom_nouvel_etat]
    a1star.make_accept(nom_nouvel_etat)
    return a1star


##################

def concat(a1: Automaton, a2: Automaton) -> Automaton:
    a1_a2 = a1star.deepcopy()
    a1_a2.name = "a1_a2"
    nom_nouvel_etat = nouvel_etat(a1_a2)
    for s in a2.states:
        if s in a1_a2.states:
            a2.rename_state(s, nom_nouvel_etat)
            nom_nouvel_etat = str(int(nom_nouvel_etat) + 1)
    for (s, a, d) in a2.transitions:
        a1_a2.add_transition(s, a, d)
    a1_a2.make_accept(a2.acceptstates)
    for ac in a1star.acceptstates:
        a1_a2.add_transition(ac, EPSILON, a2.initial.name)
    a1_a2.make_accept(a1star.acceptstates, accepts=False)

    return a1_a2


##################

def union(a1: Automaton, a2: Automaton) -> Automaton:
    a1_or_a2 = a1.deepcopy()
    a1_or_a2.name = "a1_or_a2"
    nom_nouvel_etat = nouvel_etat(a1_or_a2)
    for s in a2.states:
        if s in a1_or_a2.states:
            a2.rename_state(s, nom_nouvel_etat)
    nom_nouvel_etat = str(int(nom_nouvel_etat) + 1)
    for (s, a, d) in a2.transitions:
        a1_or_a2.add_transition(s, a, d)
    a1_or_a2.make_accept(a2.acceptstates)
    a1_or_a2.add_transition(nom_nouvel_etat, EPSILON, a1.initial.name)
    a1_or_a2.add_transition(nom_nouvel_etat, EPSILON, a2.initial.name)
    a1_or_a2.initial = a1_or_a2.statesdict[nom_nouvel_etat]
    return a1_or_a2


##################

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usagestring = "Usage: {} <automaton-file1.af> <automaton-file2.af>"
        error(usagestring.format(sys.argv[0]))

    # First automaton, argv[1]
    a1 = Automaton("dummy")
    a1.from_txtfile(sys.argv[1])
    a1.to_graphviz(a1.name + ".gv")
    print(a1)

    # Second automaton, argv[2]
    a2 = Automaton("dummy")
    a2.from_txtfile(sys.argv[2])
    a2.to_graphviz(a2.name + ".gv")
    print(a2)

    a1star = kleene(a1)
    print()
    print(a1star)
    a1star.to_graphviz("a1star.gv")

    a1a2 = concat(a1, a2)
    print()
    print(a1a2)
    a1a2.to_graphviz("a1a2.gv")

    a1ora2 = union(a1, a2)
    print()
    print(a1ora2)
    a1ora2.to_graphviz("a1ora2.gv")
