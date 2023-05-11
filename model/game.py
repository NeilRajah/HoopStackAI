"""
game
Author: Neil Balaskandarajah
Created on: 18/06/2020
Game class with all interactions
"""
import time
from itertools import permutations
from copy import deepcopy
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
        self.stacks = dict()                # Stacks containing pieces
        self.STACK_LABELS = 'ABCDEFGH'      # Alphabetical labels for each stack
        self.label_idx = 0                  # Index of the current label for adding stacks
        self.history = []                   # History of moves the solver has performed
        self.prev_moves = []                # Previous move
        self.prev_pairs = []                # Moves that could be performed last iteration
        self.prev_stacks = []               # Previous state of all of the stacks for backtracking
        self.is_backtracking = False        # Whether the solver is currently backtracking or not

        # Attributes for debugging
        self.print_moves = False            # Whether to print the moves out to the screen or not
        self.debug = False                  # Whether the solver is in debug mode or not

    def add_stack(self, stack):
        """Add a stack to the game

        @param stack: Stack of hoops ordered top to bottom (ie. index 0 is top, -1 is bottom)
        @return: A debug message containing the name of the stack and its contents
        """
        if self.label_idx > len(self.STACK_LABELS):
            raise Exception('Cannot have more than {} stacks!'.format(len(self.STACK_LABELS)))
        if not isinstance(stack, list):
            raise Exception('Stack must be a Python list!')

        # Reverse stack so stack.pop() removes the top piece
        stack.reverse()
        self.stacks[self.STACK_LABELS[self.label_idx]] = stack
        self.label_idx += 1
        return "Stack {} added: {}".format(self.STACK_LABELS[self.label_idx-1], stack)

    def add_stacks(self, stacks):
        """Add multiple stacks to the game

        @param stacks: List of stacks to add
        """
        for stack in stacks:
            self.add_stack(stack)

    def move_pieces(self, pair_tup):
        """Move a piece from the top of one stack to the other

        @param pair_tup: The pair of stacks in (from, to) format (ie. move_pieces (x,y) moves from stack x to stack y)
        @return: A debug message saying which piece was moved between which stacks
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
        self.history.append(pair_tup)
        self.prev_moves.append(pair_tup)
        return "Moved {} from {} to {}".format(b[-1], pair_tup[0], pair_tup[1])

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
            if len(self.stacks[stack]) > 0:
                s = self.stacks[stack][0]
                break
        blank = '_' * len(s) + ' '
        spacer = '-' * (7 * len(self.stacks))
        for i in reversed(range(self.max_stack_size)):
            row = ""
            for lbl in self.stacks:
                if i > len(self.stacks[lbl])-1:
                    row = row + blank
                else:
                    row = row + "{} ".format(self.stacks[lbl][i])
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
        return self.label_idx

    def is_solved(self):
        """Return if the game is solved or not

        @return: True if all of the stacks are solved or empty, else false
        """
        # return any([solver.is_stack_solved_or_empty(stack, self.max_stack_size) for stack in self.stacks])
        for stack in self.stacks:
            if not solver.is_stack_solved_or_empty(stack, self.max_stack_size):
                return False
        return True

    def _undo(self):
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
            self._undo()

    def solve(self, print_moves=False, debug=False):
        """Solve the puzzle

        @param print_moves: Whether to print the moves out or not
        @param debug: Whether to display debug messages or not
        """
        self.print_moves = print_moves
        self.debug = debug
        print("*******START*******")

        #Start the solution by calculating all possible moves
        moves = list(permutations(self.stacks, 2)) #change to local?
        self.prev_pairs.append(deepcopy(moves))
        move_num = []
        t1 = time.time()

        log_file = '../log.txt'
        open(log_file, 'w').close()
        file = open(log_file, 'a')
        file.write('\n')
        
        # For preventing infinite loops
        num_loops = 10000
        loop = 0  
        pairs = []
        while not self.is_solved():
            if loop >= num_loops:
                print("\nToo many loops"); break

            if self.is_backtracking:
                # Undo the last move, reset the pairs to the last set and move forward
                if self.debug:
                    util.print_tup(pairs, 'pre-backtracking pairs')

                pairs = self.prev_pairs.pop()
                if len(self.prev_moves) > 0 and self.prev_moves[-1] in pairs:
                    pairs.remove(self.prev_moves[-1])
                self._undo()
                self.is_backtracking = False

                if self.debug:
                    print(pairs, 'post-backtracking pairs')
            else:
                # Generate all possible moves and filter out those that are invalid
                pairs = deepcopy(moves)
                if self.debug:
                    util.print_tup(pairs, "{} inital\n".format(len(self.history)))

                pairs = solver.remove_empty_solved(self.stacks, pairs, self.max_stack_size)
                pairs = solver.remove_opposite(pairs, self.prev_moves)
                pairs = solver.remove_incompatibles(self.stacks, pairs, self.max_stack_size)
                pairs = solver.remove_homog_to_homog(self.stacks, pairs)

                if self.debug:
                    util.print_tup(pairs, "remaining")

            if len(pairs) == 0:
                # No moves can be performed
                self.is_backtracking = True
                if self.debug:
                    move_num.append(len(self.history))
                    print('BACKTRACKING on move', len(self.history))
            else:
                # There are possible moves that can be performed
                self.prev_stacks.append(deepcopy(self.stacks))
                self.prev_pairs.append(deepcopy(pairs))

                # Choose a move
                chosen_move = pairs[-1]

                pairs_str = ''
                for pair in pairs:
                    pairs_str = pairs_str + ''.join(pair) + ' '

                # Optimize the move if its filling a stack up
                chosen_move = solver.fill_efficiently(self.stacks, chosen_move)
                file.write('{:2d}: {} - {}\n'.format(loop, ''.join(chosen_move), pairs_str))

                if self.print_moves:
                    self.move_and_display(chosen_move)
                else:
                    self.move_pieces(chosen_move)

            loop += 1
            if self.debug:
                print()

        file.close()
        if self.is_solved():
            print("*******SOLVED******")
            # self.display_history()
            self.history = solver.clean_up_moves(self.history)
            # print()
        print('Time to solve: {}s'.format(round(time.time() - t1, 3)))
        # if self.debug: plt.plot(move_num); plt.ylabel = 'Backtrack move'; plt.show()
        # self.display()
        self.display_history()

    def add_piece(self, stack, piece):
        """Add a piece to a stack when creating the game

        @param stack: Stack of pieces
        @param piece: Piece to add to stack
        """
        self.stacks[stack].append(piece)

    def get_stack_list(self):
        """Get the stacks as a list

        @return: List of stacks
        """
        return [self.stacks[self.STACK_LABELS[i]] for i in range(len(self.stacks))]

    def get_label_list(self):
        """

        :return:
        """
        return self.STACK_LABELS[:self.label_idx]