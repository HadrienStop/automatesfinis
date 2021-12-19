#!/usr/bin/env python3
"""
Read a regular expression and returns:
 * YES if word is recognized
 * NO if word is rejected"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn, RegExpReader
import sys
import pdb  # for debugging


##################


def is_deterministic(a: Automaton) -> bool:
    is_more_than_one = True
    for (source, symb, dest) in a.transitions:
        if len(symb) != 1:
            is_more_than_one = False

    return is_more_than_one


##################

def recognizes(a: Automaton, word: str) -> bool:
    current_state = list(a.statesdict)[0]
    for index in range(len(word)):
        if word[index] in list(a.statesdict[current_state].transitions):
            current_state = str(list(a.statesdict[current_state].transitions[word[index]])[0])
        else:
            if word[index] != '%':
                return False
        return current_state in a.acceptstates


##################

def determinise(a: Automaton):
    # Copy-paste or import from previous TPs
    pass


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
    a1star.name = a1.name + "*"
    for state in a1star.acceptstates:
        a1star.add_transition(state, EPSILON, a1.initial.name)
    nom_nouvel_etat = nouvel_etat(a1star)
    a1star.add_transition(nom_nouvel_etat, EPSILON, a1.initial.name)
    a1star.initial = a1star.statesdict[nom_nouvel_etat]
    a1star.make_accept(nom_nouvel_etat)
    return a1star


##################
def get_new_names(a1, a2):
    new_names = {}
    new_name = nouvel_etat(a1)
    for state in a2.states:
        new_names[state] = state
        if (state in a1.states) or (state in list(new_names.values())):
            new_names[state] = new_name
            new_name = str(int(new_name) + 1)
    return new_names


def concat(a1: Automaton, a2: Automaton) -> Automaton:
    a1_a2 = a1.deepcopy()
    a1_a2.name = a1.name + "_" + a2.name
    nom_nouvel_etat = get_new_names(a1, a2)
    for (source, symbol, destination) in a2.transitions:
        a1_a2.add_transition(nom_nouvel_etat[source], symbol, nom_nouvel_etat[destination])
    for state in a2.acceptstates:
        a1_a2.make_accept(nom_nouvel_etat[state])
    for state in a1.acceptstates:
        a1_a2.add_transition(state, EPSILON, nom_nouvel_etat[a2.initial.name])
        a1_a2.make_accept(a1.acceptstates, accepts=False)
    return a1_a2


##################

def union(a1: Automaton, a2: Automaton) -> Automaton:
    a1_or_a2 = a1.deepcopy()
    a1_or_a2.name = a1.name + "+" + a2.name
    nom_nouvel_etat = get_new_names(a1_or_a2, a2)
    for (source, symbol, destination) in a2.transitions:
        a1_or_a2.add_transition(nom_nouvel_etat[source], symbol, nom_nouvel_etat[destination])
    for state in a2.acceptstates:
        a1_or_a2.make_accept(nom_nouvel_etat[state])
    nouvel_etat_initial = nouvel_etat(a1_or_a2)
    a1_or_a2.add_transition(nouvel_etat_initial, EPSILON, a1.initial.name)
    a1_or_a2.add_transition(nouvel_etat_initial, EPSILON, nom_nouvel_etat[a2.initial.name])
    a1_or_a2.initial = a1_or_a2.statesdict[nouvel_etat_initial]
    return a1_or_a2


##################

def regexp_to_automaton(re: str) -> Automaton:
    """
  Moore's algorithm: regular expression `re` -> non-deterministic automaton
  """
    postfix = RegExpReader(regexp).to_postfix()
    stack: List[Automaton] = []
    # TODO implement!
    return stack[0]


##################

if __name__ == "__main__":

    if len(sys.argv) != 3:
        usagestring = "Usage: {} <regular-expression> <word-to-recognize>"
        error(usagestring.format(sys.argv[0]))

    regexp = sys.argv[1]
    word = sys.argv[2]

    a = regexp_to_automaton(regexp)
    determinise(a)
    if recognizes(a, word):
        print("YES")
    else:
        print("NO")
