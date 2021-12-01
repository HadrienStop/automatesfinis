#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * YES if word is recognized
 * NO if word is rejected
Determinises the automaton if it's non deterministic
"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn
import sys
import pdb  # for debugging


##################

def is_deterministic(a: 'Automaton') -> bool:
    is_more_than_one = True
    for (source, symb, dest) in a.transitions:
        if len(symb) != 1:
            is_more_than_one = False

    return is_more_than_one


##################

def recognizes(a: 'Automaton', word: str) -> bool:
    current_state = list(a.statesdict)[0]
    for index in range(len(word)):
        if word[index] in list(a.statesdict[current_state].transitions):
            current_state = str(list(a.statesdict[current_state].transitions[word[index]])[0])
        else:
            if word[index] != '%':
                return False
        return current_state in a.acceptstates


##################

def remove_epsilon(a: Automaton):
    for (source, symb, dest) in a.transitions:
        if symb == '%':
            for trans in list(a.statesdict[dest].transitions):
                a.add_transition(source, trans, dest)
            for trans_epsilon in list(a.statesdict[source].transitions):
                a.remove_transition(source, "%", dest)
        if dest in a.acceptstates:
            a.make_accept(source)
    a.remove_unreachable()


def reduce_transitions(a: Automaton):
    new_states = [set([a.initial.name])]


def determinise(a: Automaton):
    remove_epsilon(a)


##################

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
        error(usagestring.format(sys.argv[0]))

    automatonfile = sys.argv[1]
    word = sys.argv[2]

    a = Automaton("dummy")
    a.from_txtfile(automatonfile)
    if not is_deterministic(a):
        determinise(a)
    if recognizes(a, word):
        print("YES")
    else:
        print("NO")
