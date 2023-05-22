"""
game
Author: Neil Balaskandarajah
Created on: 18/06/2020
Game class with all interactions
"""
import time
import itertools
import util
import random
import model.solver as solver
import matplotlib.pyplot as plt

def are_stacks_compatible(stack1, stack2, max_stack_size):
    """Return if a move can be done between the two stacks

    :param stack1: First stack
    :param stack2: Second stack
    :param max_stack_size: Maximum number of hoops in a stack
    :return: True if both stacks have top hoops of same color and are not full
    """
    # Cannot move from empty stack or to a full stack
    if len(stack1) == 0 or len(stack2) == max_stack_size:
        return False

    # Can move to an empty stack or if the stacks have the same top piece
    if len(stack2) == 0 or stack1[-1] == stack2[-1]:
        return True
    return False

def get_max_stack_size(stacks):
    item = None
    max_stack_size = 0
    for stack in stacks:
        for hoop in stack:
            if item is None:
                item = hoop
            if hoop == item:
                max_stack_size += 1
    return max_stack_size

class Game:
    def __init__(self, max_stack_size, name='Game'):
        """Create a Game object

        :param max_stack_size: The max size of a stack
        :param name: Name of the game
        """
        self.name = name
        self.max_stack_size = max_stack_size        # Max number of pieces in a stack

        # Attributes for solving
        self.stacks = []                # Stacks containing pieces

    #---Creation---#

    def add_stack(self, stack):
        """Add a stack to the game

        :param stack: Stack of hoops ordered top to bottom (ie. index 0 is top, -1 is bottom)
        """
        if not isinstance(stack, list):
            raise Exception('Stack must be a Python list!')

        # Reverse stack so stack.pop() removes the top piece
        # Add a bottom-up check
        stack.reverse()
        self.stacks.append(stack)

    def add_stacks(self, stacks):
        """Add multiple stacks to the game

        :param stacks: List of stacks to add
        """
        for stack in stacks:
            self.add_stack(stack)

    def add_piece(self, stack_idx, piece):
        """Add a piece to a stack when creating the game

        :param stack_idx: Index of the stack to add the piece to
        :param piece: Piece to add to stack
        """
        self.stacks[stack_idx].append(piece)

    #---Actions---#

    def move_pieces(self, pair_tup, bypassing=False):
        """Move a piece from the top of one stack to the other

        :param pair_tup: The pair of stacks in (from, to) format (ie. move_pieces (x,y) moves from stack x to stack y)
        :param bypassing: Whether the rules should be considered or not (Rules not considered if true)
        """
        if not self.is_pair_compatible(pair_tup) and not bypassing:
            msg = "Stacks {} and {} are not compatible!".format(pair_tup[0], pair_tup[1])
            msg += "\n[{}, {}]".format(self.stacks[pair_tup[0]], self.stacks[pair_tup[1]])
            raise Exception(msg)

        # Move from top of the first stack to the second
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]
        b.append(a.pop())

    def is_pair_compatible(self, pair_tup):
        """Check if a pair of stacks are compatible

        :param pair_tup: The pair of stacks identified by their stack label
        :return: Whether the top hoop of the first stack can be placed on the second stack
        """
        stack1 = self.stacks[pair_tup[0]]
        stack2 = self.stacks[pair_tup[1]]

        return are_stacks_compatible(stack1, stack2, self.max_stack_size)

    def display(self):
        """Print the game out to the console"""
        # print(self.stacks)
        s = ''
        for stack in self.stacks:
            if len(stack) > 0:
                s = stack[0]
                break
        blank = '_' * len(s) + ' '
        spacer = '-' * (7 * len(self.stacks))
        for i in reversed(range(self.max_stack_size)):
            row = ""
            for stack in self.stacks:
                if i > len(stack)-1:
                    row = row + blank
                else:
                    row = row + "{} ".format(stack[i])
            print(row)
        print(spacer)

    def get_num_stacks(self):
        """Get the number of stacks in the game

        :return: Total number of stacks
        """
        return len(self.stacks)

    def is_solved(self):
        """Return if the game is solved or not

        :return: True if all of the stacks are solved or empty, else false
        """
        return all([solver.is_stack_solved_or_empty(stack, self.max_stack_size) for stack in self.stacks])
        # for stack in self.stacks:
        #     if not solver.is_stack_solved_or_empty(stack, self.max_stack_size):
        #         return False
        # return True

