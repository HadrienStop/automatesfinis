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
    deterministic = True
    for (source, symb, dest) in a.transitions:
        if len(symb) != 1:
            deterministic = False
        if symb == EPSILON:
            deterministic = False
    return deterministic


##################

def recognizes(a: Automaton, word: str) -> bool:
    current_state = list(a.statesdict)[0]
    for i in range(len(word)):
        if word[i] in list(a.statesdict[current_state].transitions):
            current_state = str(list(a.statesdict[current_state].transitions[word[i]])[0])
        else:
            if word[i] != '%':
                return False
        return current_state in a.acceptstates


##################
def transitions_epsilon(a):
    list_epsilon_transition = []
    for (source, symb, dest) in a.transitions:
        if str(symb) == '%':
            transit_lign = source, symb, dest
            list_epsilon_transition.append(transit_lign)

    return list_epsilon_transition


def supprimer_epsilon(a):
    list = transitions_epsilon(a)
    for transition in a.transitions:
        for element in list:
            a.make_accept(element[0])
            if transition[0] == element[2]:
                a.add_transition(element[0], transition[1], element[2])
    for value in list:
        a.remove_transition(*value)


def determinise(a):
    supprimer_epsilon(a)

    for s in a.states:
        nouvel_etat = [{a.initial.name}]
        for t in a.transitions:
            if t[0] == str(s):
                print(s, t)
                a.add_transition(str(nouvel_etat[s]), t[1], str(nouvel_etat[t[2]]))
                a.remove_transition(s, t[1], t[2])


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
    for s in a1star.acceptstates:
        a1star.add_transition(s, EPSILON, a1.initial.name)
    nom_nouvel_etat = nouvel_etat(a1star)
    a1star.add_transition(nom_nouvel_etat, EPSILON, a1.initial.name)
    a1star.initial = a1star.statesdict[nom_nouvel_etat]
    a1star.make_accept(nom_nouvel_etat)
    return a1star


##################
def nouveaux_noms(a1, a2):
    nouveaux_noms = {}
    nouveau_nom = nouvel_etat(a1)
    for s in a2.states:
        nouveaux_noms[s] = s
        if (s in a1.states) or (s in list(nouveaux_noms.values())):
            nouveaux_noms[s] = nouveau_nom
            nouveau_nom = str(int(nouveau_nom) + 1)
    return nouveaux_noms


def concat(a1: Automaton, a2: Automaton) -> Automaton:
    a1_a2 = a1.deepcopy()
    a1_a2.name = "a1_a2"
    nom_nouvel_etat = nouveaux_noms(a1, a2)
    for (source, symbol, destination) in a2.transitions:
        a1_a2.add_transition(nom_nouvel_etat[source], symbol, nom_nouvel_etat[destination])
    for s in a2.acceptstates:
        a1_a2.make_accept(nom_nouvel_etat[s])
    for s in a1.acceptstates:
        a1_a2.add_transition(s, EPSILON, nom_nouvel_etat[a2.initial.name])
        a1_a2.make_accept(a1.acceptstates, accepts=False)
    return a1_a2


##################

def union(a1: Automaton, a2: Automaton) -> Automaton:
    a1_or_a2 = a1.deepcopy()
    a1_or_a2.name = "a1_or_a2"
    nom_nouvel_etat = nouveaux_noms(a1_or_a2, a2)
    for (source, symbol, destination) in a2.transitions:
        a1_or_a2.add_transition(nom_nouvel_etat[source], symbol, nom_nouvel_etat[destination])
    for s in a2.acceptstates:
        a1_or_a2.make_accept(nom_nouvel_etat[s])
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
