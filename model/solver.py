"""
solver
Author: Neil Balaskandarajah
Created on: 11/05/2023
Functions related to solving the game
"""
import model.game as game
import util

STACK_LABELS = 'ABCDEFGH'

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

    :param stack: The stack to check
    :return: Whether there is only one unique color present in the stack
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

def fill_efficiently(stacks, move):
    """Fill stacks efficiently by moving from small homogenous stacks to large ones instead of vice versa

    :param stacks: Dictionary of stacks in the game
    :param move: Move of (from, to) stack labels
    :return: Return the move that moves the hoop from the smaller stack to the larger one
    """
    stack1 = stacks[move[0]]
    stack2 = stacks[move[1]]

    if is_stack_homog(stack1) and is_stack_homog(stack2):
        if len(stack1) > len(stack2):
            return move[::-1]  #Flip the move if going from large homog to small homog
    return move

def clean_up_moves(history):
    """Streamline the solution by removing redundant moves (ie. AB, BC -> AC)

    :param history: All moves which have been performed
    :return: The entire set of movements without redundant moves
    """
    idx = 0
    while idx < len(history)-1:
        start = history[idx]
        end = history[idx+1]

        # turn AB BC to AC
        if start[1] == end[0]:
            history.pop(idx)
            history.pop(idx)
            history.insert(idx, (start[0], end[1]))
        idx += 1
    return history

def remove_empty_solved(stacks, pairs, max_stack_size):
    """Remove the empty and solved stacks from the current set of moves

    :param stacks: List of stacks
    :param pairs: Pairs of moves in (from, to) stack label format
    :param max_stack_size: Greatest number of hoops in a stack
    """
    # Check for empty or solved stacks
    solved_or_empty = []
    for stack in stacks:
        if is_stack_solved_or_empty(stack, max_stack_size):
            solved_or_empty.append(stack)

    # Eliminate all moves with pieces going from empty or solved pairs
    remove = []
    for pair in pairs:
        for stack in solved_or_empty:
            if pair[0] == stack:
                remove.append(pair)
    if len(remove) > 0:
        util.subtract_lists(pairs, remove)

    return pairs

def remove_opposite(pairs, prev_moves):
    """Remove the opposite of the last move to avoid getting stuck in a two-move loop

    :param pairs: Pairs of moves in (from, to) stack label format
    :param prev_moves: List of previous moves
    """
    if len(prev_moves) > 0:
        opp = prev_moves[-1][::-1]
        if opp in pairs:
            pairs.remove(opp)

    return pairs

def remove_incompatibles(stacks, pairs, max_stack_size):
    """Remove moves between incompatible stacks

    :param stacks: Dictionary of stacks
    :param pairs: Pairs of moves in (from, to) stack label format
    :param max_stack_size: The maximum number of hoops in a stack
    :return: The new set of moves without moves to/from incompatible stacks
    """
    remove = []
    for pair in pairs:
        stack1 = stacks[pair[0]]
        stack2 = stacks[pair[1]]
        if not game.are_stacks_compatible(stack1, stack2, max_stack_size):
            remove.append(pair)
    if len(remove) > 0:
        util.subtract_lists(pairs, remove)

    return pairs

def remove_homog_to_homog(stacks, pairs):
    """Remove moves coming from a stack with all of the same colors to a stack that's not the same color

    :param stacks: Dictionary of stacks
    :param pairs: Pairs of moves in (from, to) stack label format
    """
    remove = []
    for pair in pairs:
        stack1 = stacks[pair[0]]
        stack2 = stacks[pair[1]]
        if is_stack_homog(stack1) and not is_stack_homog(stack2):
            remove.append(pair)
    if len(remove) > 0:
        util.subtract_lists(pairs, remove)

    return pairs
