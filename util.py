"""
util
Author: Neil Balaskandarajah
Created on: 30/04/2023
Utility functions
"""

def subtract_lists(a, b):
    """Subtract b from a (a - b)

    :param a: First list
    :param b: Second list
    :return: List a without everything in b
    """
    for x in b:
        if x in a:
            a.remove(x)
    return a

def print_tup(group, msg, elems_per_row=3):
    """All elements of a tuple in a String

    @param group: Group of elements
    @param msg: Message to print before listing off elements
    @param elems_per_row: Number of elements per row
    """
    elements = ''
    for i, tup in enumerate(group):
        end = '\n' if (i+1) % elems_per_row == 0 else ' '
        elements = elements + ''.join(tup) + end
        # if i % 5 == 0: elements = elements + '\n'
    print("{}{}".format(msg, elements))

def print_n_at_a_time(lis, n, msg=''):
    """Print out a list with each line containing n elements

    :param lis: List of elements to print
    :param n: Number of elements to print
    :param msg: Message to print before printing the list
    """
    if len(lis) == 0:
        print('empty list')
    if msg != '':
        print(msg)
    for i, elem in enumerate(lis):
        print(elem, end=' ')
        if (i + 1) % n == 0:
            print()
    print()