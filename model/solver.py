"""
solver
Author: Neil Balaskandarajah
Created on: 11/05/2023
Functions related to solving the game
"""

def is_stack_solved_or_empty(stack, max_stack_size):
    """Return if the stack is solved, empty or neither

    @param stack: The stack to check
    @param max_stack_size: The maximum size of a stack
    @return: True if it is solved (all of same color and of max length) or empty (no hoops)
    """
    stack_is_empty = len(stack) == 0
    stack_is_solved = is_stack_homog(stack) and len(stack) == max_stack_size
    return stack_is_empty or stack_is_solved

def is_stack_homog(stack):
    """Return if a stack is all the same color or not (False if empty)

    @param stack: The stack to check
    @return: Whether there is only one unique color present in the stack
    """
    uniques = []
    num_unique = 0

    for item in stack:
        if item not in uniques:
            uniques.append(item)
            num_unique += 1
        if num_unique > 1:
            return False
    return True