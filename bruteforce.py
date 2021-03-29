#!/usr/bin/env python3
import enchant

test = False

dico_factor = 2
usual_remplacements = {
    '@': 'a',
    '3': 'e',
    '7': 't',
    '5': 's',
    '1': 'l',
    '4': 'a',
    '0': 'o'
}

def simplify(string):
    for i in usual_remplacements:
        string = string.replace(i, usual_remplacements[i])
    return string

def verify_if_dico(inp):
    d = enchant.Dict("fr_FR")
    for i in inp:
        if d.check(simplify(i)):
            inp[i] = inp[i] * dico_factor
    return inp

def generate_possible_passwords(inp, length, index = 0, string ="", prob = 1000):
    if length <= index:
        return {string: prob}

    d = {}
    for i in inp[index]:
        d = dict(d, **generate_possible_passwords(inp, length, index + 1, string + i, prob * inp[index][i]))

    return d



def list_possible_passwords(inp):
    possible = generate_possible_passwords(inp, len(inp))
    ponderated = verify_if_dico(possible)

    return ponderated



test = True
example_input = [
        {'p': 0.5, 'd': 0.25, 'g': 0.12},
        {'@': 0.5, 'k': 0.25, 'n': 0.12},
        {'t': 0.5, 'x': 0.25, '0': 0.12},
        {'@': 0.5, 'q': 0.25, 'z': 0.12},
        {'7': 0.5, 'l': 0.25, 'p': 0.12},
        {'3': 0.5, 'o': 0.25, 'j': 0.12},
]

if test:
    print(list_possible_passwords(example_input))
