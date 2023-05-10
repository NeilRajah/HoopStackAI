"""
util
Author: Neil Balaskandarajah
Created on: 30/04/2023
Utility functions
"""

def subtract_lists(a, b):
    """Subtract b from a (a - b)

    :param a: First list
    :parma b: Second list
    :return: List a without everything in b
    """
    for x in b:
        if x in a:
            a.remove(x)

def print_tup(group, msg):
    """All elements of a tuple in a String

    @param group: Group of elements
    @param msg: Message to print before listing off elements
    """
    elements = ''
    for i, tup in enumerate(group):
        elements = elements + ''.join(tup) + ' '
        # if i % 5 == 0: elements = elements + '\n'
    print("{}: {}".format(msg, elements))

# Num uniques