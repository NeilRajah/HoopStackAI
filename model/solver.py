"""
solver
Author: Neil Balaskandarajah
Created on: 11/05/2023
Functions related to solving the game
"""
import copy
import itertools
import model.game as game
import time
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

class Solver:
    def __init__(self):
        """Create a new Solver object"""
        self.history = []                   # History of moves the solver has performed
        self.prev_moves = []                # Previous move
        self.prev_pairs = []                # Moves that could be performed last iteration
        self.prev_stacks = []               # Previous state of all of the stacks for backtracking
        self.is_backtracking = False        # Whether the solver is currently backtracking or not

    def solve(self, game):
        """Solve the puzzle

        :param game: Game to solve
        :return: Moves to play the game
        """
        print("*******START*******")

        # Start the solution by calculating all possible moves
        moves = list(itertools.permutations(game.stacks, 2))  # change to local?
        self.prev_pairs.append(copy.deepcopy(moves))
        t1 = time.time()

        log_file = '../log.txt'
        open(log_file, 'w').close()
        file = open(log_file, 'a')
        file.write('\n')

        # For preventing infinite loops
        num_loops = 10000
        loop = 0
        pairs = []
        while not game.is_solved():
            if loop >= num_loops:
                print("\nToo many loops")
                break

            if self.is_backtracking:
                # Undo the last move, reset the pairs to the last set and move forward

                pairs = self.prev_pairs.pop()
                if len(self.prev_moves) > 0 and self.prev_moves[-1] in pairs:
                    pairs.remove(self.prev_moves[-1])
                game.undo()
                self.is_backtracking = False

            else:
                # Generate all possible moves and filter out those that are invalid
                pairs = copy.deepcopy(moves)

                pairs = remove_empty_solved(game.stacks, pairs, game.max_stack_size)
                pairs = remove_opposite(pairs, self.prev_moves)
                pairs = remove_incompatibles(game.stacks, pairs, game.max_stack_size)
                pairs = remove_homog_to_homog(game.stacks, pairs)

            if len(pairs) == 0:
                # No moves can be performed
                self.is_backtracking = True
            else:
                # There are possible moves that can be performed
                self.prev_stacks.append(copy.deepcopy(game.stacks))
                self.prev_pairs.append(copy.deepcopy(pairs))

                # Choose a move
                chosen_move = pairs[-1]

                pairs_str = ''
                for pair in pairs:
                    pairs_str = pairs_str + ''.join(pair) + ' '

                # Optimize the move if its filling a stack up
                chosen_move = fill_efficiently(game.stacks, chosen_move)
                file.write('{:2d}: {} - {}\n'.format(loop, ''.join(chosen_move), pairs_str))

                game.move_pieces(chosen_move)

            loop += 1

        file.close()
        if self.is_solved():
            print("*******SOLVED******")
            self.history = solver.clean_up_moves(self.history)
        print('Time to solve: {}s'.format(round(time.time() - t1, 3)))
        self.display_history()

    def undo(self, game):
        """Undo in the game and edit the solver data

        :param game:
        :return:
        """

    def play_solution(self, disp, pause):
        pass