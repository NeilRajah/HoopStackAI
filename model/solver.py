"""
solver
Author: Neil Balaskandarajah
Created on: 11/05/2023
Functions related to solving the game as well as the Solver object
"""
import copy
import itertools
import model.game as game
import time
import util

STACK_LABELS = 'ABCDEFGH'

def is_stack_solved_or_empty(stack, max_stack_size):
    """Return if the stack is solved, empty or neither

    :param stack: The stack to check
    :param max_stack_size: The maximum size of a stack
    :return: True if it is solved (all of same color and of max length) or empty (no hoops)
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

def remove_empty_solved(stacks, possible_moves, max_stack_size):
    """Remove the empty and solved stacks from the current set of moves

    :param stacks: List of stacks
    :param possible_moves: Possible moves in (from, to) stack label format
    :param max_stack_size: Greatest number of hoops in a stack
    """
    # Check for empty or solved stacks
    solved_or_empty = []
    for stack in stacks:
        if is_stack_solved_or_empty(stack, max_stack_size):
            solved_or_empty.append(stack)

    # Eliminate all moves with pieces going from empty or solved pairs
    remove = []
    for move in possible_moves:
        for stack in solved_or_empty:
            if move[0] == stack:
                remove.append(move)
    if len(remove) > 0:
        util.subtract_lists(possible_moves, remove)

    return possible_moves

def remove_opposite(possible_moves, prev_moves):
    """Remove the opposite of the last move to avoid getting stuck in a two-move loop

    :param possible_moves: Possible moves in (from, to) stack label format
    :param prev_moves: List of previous moves
    """
    if len(prev_moves) > 0:
        opp = prev_moves[-1][::-1]
        if opp in possible_moves:
            possible_moves.remove(opp)

    return possible_moves

def remove_incompatibles(stacks, possible_moves, max_stack_size):
    """Remove moves between incompatible stacks

    :param stacks: Dictionary of stacks
    :param possible_moves: Possible moves in (from, to) stack label format
    :param max_stack_size: The maximum number of hoops in a stack
    :return: The new set of moves without moves to/from incompatible stacks
    """
    remove = []
    for pair in possible_moves:
        stack1 = stacks[pair[0]]
        stack2 = stacks[pair[1]]
        if not game.are_stacks_compatible(stack1, stack2, max_stack_size):
            remove.append(pair)
    if len(remove) > 0:
        util.subtract_lists(possible_moves, remove)

    return possible_moves

def remove_homog_to_homog(stacks, possible_moves):
    """Remove moves coming from a stack with all of the same colors to a stack that's not the same color

    :param stacks: Dictionary of stacks
    :param possible_moves: Possible moves in (from, to) stack label format
    """
    remove = []
    for move in possible_moves:
        stack1 = stacks[move[0]]
        stack2 = stacks[move[1]]
        if is_stack_homog(stack1) and not is_stack_homog(stack2):
            remove.append(move)
    if len(remove) > 0:
        util.subtract_lists(possible_moves, remove)

    return possible_moves

class Solver:
    def __init__(self):
        """Create a new Solver object"""
        self.history = []                   # History of moves the solver has performed
        self.prev_moves = []                # Moves the solver attempted last step
        self.prev_possible_moves = []       # Moves that could be performed last iteration
        self.prev_stacks = []               # Previous state of all of the stacks for backtracking
        self.is_backtracking = False        # Whether the solver is currently backtracking or not

    def display_history(self):
        """Print the move history to the console"""
        # util.print_tup(self.history, '{}:\n'.format(len(self.history)))
        print('------')
        for move in self.history:
            print('{} -> {}'.format(move[0], move[1]))
        print('------')

    def possible_moves(self, moves, game):
        """Return all possible moves

        :param moves: All 2-long permutations of the stack indices
        :param game: The game with all of the stacks
        :return: All the possible moves in (from, to) format
        """
        possible_moves = copy.deepcopy(moves)

        possible_moves = remove_empty_solved(game.stacks, possible_moves, game.max_stack_size)
        possible_moves = remove_opposite(possible_moves, self.prev_moves)
        possible_moves = remove_incompatibles(game.stacks, possible_moves, game.max_stack_size)
        possible_moves = remove_homog_to_homog(game.stacks, possible_moves)

        return possible_moves

    def solve(self, game):
        """Solve the puzzle

        :param game: Game to solve
        :return: Moves to play the game
        """
        # Start the solution by calculating all possible moves
        stack_indices = [i for i in range(len(game.stacks))]
        moves = list(itertools.permutations(stack_indices, 2))  # change to local?
        self.prev_possible_moves.append(copy.deepcopy(moves))
        t1 = time.time()

        # For preventing infinite loops
        num_loops = 10000
        loop = 1
        while not game.is_solved():
            if loop > num_loops:
                raise Exception('No solution found!')

            # print('Loop {}{}'.format(loop, ', solver is backtracking' if self.is_backtracking else ''))
            if self.is_backtracking:
                # Undo the last move, reset the pairs to the last set and move forward
                possible_moves = self.prev_possible_moves.pop()
                if len(self.prev_moves) > 0 and self.prev_moves[-1] in possible_moves:
                    possible_moves.remove(self.prev_moves[-1])
                game.undo()
                self.is_backtracking = False

            else:
                # Generate all possible moves and filter out those that are invalid
                possible_moves = self.possible_moves(moves, game)

            if len(possible_moves) == 0:
                # No moves can be performed
                self.is_backtracking = True
            else:
                # There are possible moves that can be performed
                self.prev_stacks.append(copy.deepcopy(game.stacks))
                self.prev_possible_moves.append(copy.deepcopy(possible_moves))

                # Choose a move
                chosen_move = possible_moves[-1]

                # moves_str = ''
                # for move in possible_moves:
                #     moves_str = moves_str + ''.join(str(move)) + ' '

                # Optimize the move if its filling a stack up
                chosen_move = fill_efficiently(game.stacks, chosen_move)

                game.move_pieces(chosen_move)
                self.history.append(chosen_move)

            loop += 1

        if game.is_solved():
            # print("*******SOLVED******")
            self.history = clean_up_moves(self.history)
        print('Time to solve: {}s'.format(round(time.time() - t1, 3)))
        # self.display_history()
        # game.display()
        return self.history

    def undo(self, game):
        """Undo in the game and edit the solver data

        :param game:
        :return:
        """
        pass
