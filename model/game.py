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

class Game:
    def __init__(self, max_stack_size, name='Game'):
        """Create a Game object

        @param max_stack_size: The max size of a stack
        @param name: Name of the game
        """
        self.name = name
        self.max_stack_size = max_stack_size        # Max number of pieces in a stack

        # Attributes for solving
        self.stacks = []                # Stacks containing pieces

    #---Creation---#

    def add_stack(self, stack):
        """Add a stack to the game

        @param stack: Stack of hoops ordered top to bottom (ie. index 0 is top, -1 is bottom)
        """
        if not isinstance(stack, list):
            raise Exception('Stack must be a Python list!')

        # Reverse stack so stack.pop() removes the top piece
        stack.reverse()
        self.stacks.append(stack)

    def add_stacks(self, stacks):
        """Add multiple stacks to the game

        @param stacks: List of stacks to add
        """
        for stack in stacks:
            self.add_stack(stack)

    def add_piece(self, stack_idx, piece):
        """Add a piece to a stack when creating the game

        @param stack_idx: Index of the stack to add the piece to
        @param piece: Piece to add to stack
        """
        self.stacks.append(piece)

    #---Actions---#

    def move_pieces(self, pair_tup):
        """Move a piece from the top of one stack to the other

        @param pair_tup: The pair of stacks in (from, to) format (ie. move_pieces (x,y) moves from stack x to stack y)
        """
        if not self.is_pair_compatible(pair_tup):
            msg = "Stacks {} and {} are not compatible!".format(pair_tup[0], pair_tup[1])
            msg = msg + "\n{} | {}".format(self.stacks[pair_tup[0]], self.stacks[pair_tup[1]])
            raise Exception(msg)

        # Move from top of the first stack to the second
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]
        b.append(a.pop())

        # Save to history
        # self.history.append(pair_tup)
        # self.prev_moves.append(pair_tup)

    def is_pair_compatible(self, pair_tup):
        """Check if a pair of stacks are compatible

        @param pair_tup: The pair of stacks identified by their stack label
        @return:
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

    def display_history(self):
        """Print the move history to the console"""
        util.print_tup(self.history, '{}:\n'.format(len(self.history)))

    def move_and_display(self, pair_tup):
        """Move a piece and print game information to the console

        @param pair_tup: The pair of stacks identified by their stack label
        """
        self.move_pieces(pair_tup)
        self.display()
        self.display_history()

    def get_num_stacks(self):
        """Get the number of stacks in the game

        @return: Total number of stacks
        """
        return len(self.stacks)

    def is_solved(self):
        """Return if the game is solved or not

        @return: True if all of the stacks are solved or empty, else false
        """
        # return any([solver.is_stack_solved_or_empty(stack, self.max_stack_size) for stack in self.stacks])
        for stack in self.stacks:
            if not solver.is_stack_solved_or_empty(stack, self.max_stack_size):
                return False
        return True

    def undo(self):
        """Undo the last move done (for backtracking)"""
        if len(self.history) > 0:
            pair = self.history.pop()[::-1]  # opposite of last move done
            a = self.stacks[pair[0]]
            b = self.stacks[pair[1]]
            b.append(a.pop())
        if len(self.prev_moves) > 0:
            self.prev_moves.pop()

    def reset(self):
        """Reset the game to its original state"""
        while len(self.history) > 0:
            self.undo()

