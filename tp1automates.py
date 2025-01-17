#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * ERROR if non deterministic
 * YES if word is recognized
 * NO if word is rejected
"""

from automaton import Automaton, EPSILON, error, warn
import sys
import pdb  # for debugging


##################

def is_deterministic(a: 'Automaton') -> bool:
    is_deterministic = True
    for (source, symb, dest) in a.transitions:
        if len(symb) != 1:
            is_deterministic = False
        if symb == EPSILON:
            is_deterministic = False
    return is_deterministic


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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
        error(usagestring.format(sys.argv[0]))

    automatonfile = sys.argv[1]
    word = sys.argv[2]

    a = Automaton("dummy")
    a.from_txtfile(automatonfile)

    if not is_deterministic(a):
        print("ERROR")
    elif recognizes(a, word):
        print("YES")
    else:
        print("NO")
