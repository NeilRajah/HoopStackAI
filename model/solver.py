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
CHOSEN_MOVE_IDX = -1

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
    if len(stack) == 0:
        return False

    uniques = [stack[0]]

    for item in stack[1:]:
        if item not in uniques:
            return False
    return True

def fill_homog_efficiently(stacks, move):
    """Fill homogenous stacks efficiently by moving from small stacks to large ones instead of vice versa

    :param stacks: Dictionary of stacks in the game
    :param move: Move of (from, to) stack labels
    :return: Return the move that moves the hoop from the smaller stack to the larger one
    """
    stack1 = stacks[move[0]]
    stack2 = stacks[move[1]]

    if is_stack_homog(stack1) and is_stack_homog(stack2) and len(stack1) > len(stack2):
        return move[::-1]  # Flip the move if going from large homog to small homog
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
    solved_or_empty = [stack for stack in stacks if is_stack_solved_or_empty(stack, max_stack_size)]

    remove = []
    for move in possible_moves:
        if stacks[move[0]] in solved_or_empty:
            remove.append(move)
    return util.subtract_lists(possible_moves, remove)

def remove_opposite(possible_moves, last_move):
    """Remove the opposite of the last move to avoid getting stuck in a two-move loop

    :param possible_moves: Possible moves in (from, to) stack label format
    :param last_move: The last move performed by the solver
    :return: The new subset of moves
    """
    opp = last_move[::-1]
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

    return [move for move in possible_moves if move not in remove]
    # return [move for move in possible_moves if game.are_stacks_compatible(stacks[move[0]], stacks[move[1]], max_stack_size)]

def remove_all_same_to_different(stacks, possible_moves):
    """Remove moves coming from a stack with all of the same colors to a stack that's not the same color

    :param stacks: Dictionary of stacks
    :param possible_moves: Possible moves in (from, to) stack label format
    :return: The new set of moves without moves from a homogenous stack to a non-homogenous stack
    """
    remove = []
    for move in possible_moves:
        stack1 = stacks[move[0]]
        stack2 = stacks[move[1]]
        if is_stack_homog(stack1) and not is_stack_homog(stack2):
            remove.append(move)

    return util.subtract_lists(possible_moves, remove)

def remove_infinite_loops(stacks, possible_moves, max_stack_size):
    """Remove all moves that would result in the solver cycling the hoop between a number of stacks indefinitely

    :param stacks: Dictionary of stacks
    :param possible_moves: Possible moves in (from, to) stack label format
    :param max_stack_size: The maximum number of hoops in a stack
    :return: Moves that would cause an infinite loop
    """
    remove = []
    for move in possible_moves:
        stack1 = stacks[move[0]]
        stack2 = stacks[move[1]]

        stack1_after_move = stack1[:-1]
        stack2_after_move = stack2 + [stack1[-1]]

        print(stack1, stack2)
        print(stack1_after_move, stack2_after_move)
        print()

        if game.are_stacks_compatible(stack1, stack2, max_stack_size) \
            and game.are_stacks_compatible(stack1_after_move, stack2_after_move, max_stack_size):
            print(move)
            remove.append(move)

    return util.subtract_lists(possible_moves, remove)

class Solver:
    def __init__(self):
        """Create a new Solver object"""

    def filter_moves(self, moves, game):
        """Return all possible moves

        :param moves: All 2-long permutations of the stack indices
        :param game: The game with all of the stacks
        :return: All the possible moves in (from, to) format
        """
        # print(self.move_history[str(game.stacks)])
        # possible_moves = [move for move in moves if move not in self.move_history[str(game.stacks)]]
        possible_moves = remove_incompatibles(game.stacks, moves, game.max_stack_size)
        possible_moves = remove_empty_solved(game.stacks, possible_moves, game.max_stack_size)
        possible_moves = remove_all_same_to_different(game.stacks, possible_moves)

        return possible_moves

    def solve(self, game, num_loops=10000):
        """Solve the puzzle

        :param game: Game to solve
        :param num_loops: Number of loops to run before exiting the solver
        :return: Moves to play the game
        """
        game = copy.deepcopy(game)
        # Start the solution by calculating all possible moves
        stack_indices = [i for i in range(len(game.stacks))]
        moves = list(itertools.permutations(stack_indices, 2))
        move_history = []

        t1 = time.time()
        possible_moves = {}
        stack_history = []

        # For preventing infinite loops
        loop = 0
        while not game.is_solved():
            if loop > num_loops:
                print('No solution found!')
                return move_history
            loop += 1

            state_str = str(game.stacks)

            # Generate all possible moves and filter out those that are invalid
            if state_str not in possible_moves.keys():
                possible_moves[state_str] = self.filter_moves(moves, game)

            if len(possible_moves[state_str]) == 0:
                # No moves can be performed
                # self.is_backtracking = True
                game.stacks = stack_history.pop()
            else:
                # There are possible moves that can be performed
                stack_history.append(copy.deepcopy(game.stacks))

                chosen_move = possible_moves[state_str].pop()

                # Optimize the move if its filling a stack up
                chosen_move = fill_homog_efficiently(game.stacks, chosen_move)

                try:
                    game.move_pieces(chosen_move)
                except Exception:
                    print('lol bad move: {}'.format(chosen_move))
                    move_history.append(chosen_move)
                    return move_history

                move_history.append(chosen_move)

        if game.is_solved():
            # print("*******SOLVED******")
            move_history = clean_up_moves(move_history)
            print('Time to solve: {}s'.format(round(time.time() - t1, 3)))
        return move_history