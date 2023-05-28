"""
solver
Author: Neil Balaskandarajah
Created on: 11/05/2023
Solving the game with backtracking
"""
import copy
import itertools
import model.game as game
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

def clean_up_opposites(history):
    """Remove moves that are opposite one another as they have no impact on the game
    ie. BC AB BA AC --> BC AC
    ie. BC AD CB DB --> AD DB

    :param history: List of moves
    :return: New list of moves without opposites
    """
    removals = []
    # Loop through the array, and see if any move down the line is its opposite
    # Remove both of them only if the corresponding stacks are not touched in between
    # ie. AB CD CD BA --> CD CD but AB AC BA stays as is
    for i, move in enumerate(history):
        for j, future_move in enumerate(history[i+1:]):
            if move[0] in future_move and move[1] not in future_move \
                    or move[1] in future_move and move[0] not in future_move:
                break
            elif move[1] == future_move[0] and move[0] == future_move[1]:
                removals.append(i)
                removals.append(i + j + 1)
                break

    return [history[i] for i in range(len(history)) if i not in removals]

def clean_up_inbetweens(history):
    """Clean up redundant moves inbetween moves
    ie. AB BC --> AC
    ie. AB DE BC --> AC DE

    :param history: List of moves
    :return: Moves with redundant inbetween moves removed
    """
    return history

    # i = 0
    # while i < len(history):
    #     move = history[i]
    #     for j, future_move in enumerate(history[i+1:]):
    #         # Remove moves inline
    #         if move[0] != future_move[1] and move[1] == future_move[0]:
    #             print('Cleaning up inbetweens')
    #             # print(history, move, future_move)
    #             # print(move, history[i])
    #             # history.pop(i)
    #             # print(future_move, history[i+j])
    #             # history.pop(i+j-1)
    #             # history.remove(move)
    #             # history.remove(future_move)
    #             history = [move for idx, move in enumerate(history) if idx not in (i, i+j+1)]
    #             # history.pop(history.index(move, i-1))
    #             # history.pop(history.index(future_move, i-1))
    #             new_move = (move[0], future_move[1])
    #             history.insert(i-2, new_move)
    #             # print(history[i])
    #     i += 1
    #
    # return history

    # idx = 0
    # while idx < len(history) - 1:
    #     start = history[idx]
    #     end = history[idx + 1]
    #
    #     # turn AB BC to AC
    #     if start[1] == end[0] and start[0] != end[1]:
    #         history.pop(idx)
    #         history.pop(idx)
    #         history.insert(idx, (start[0], end[1]))
    #     idx += 1

def clean_up_moves(history):
    """Streamline the solution by removing redundant and inefficient moves

    :param history: All moves which have been performed
    :return: The entire set of movements without redundant moves
    """
    history = clean_up_opposites(history)
    history = clean_up_inbetweens(history)
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
    return [move for move in possible_moves if move not in remove]

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

    return [move for move in possible_moves if move not in remove]

def filter_moves(moves, game):
    """Return all possible moves

    :param moves: All 2-long permutations of the stack indices
    :param game: The game with all of the stacks
    :return: All the possible moves in (from, to) format
    """
    possible_moves = remove_incompatibles(game.stacks, moves, game.max_stack_size)
    possible_moves = remove_empty_solved(game.stacks, possible_moves, game.max_stack_size)
    possible_moves = remove_all_same_to_different(game.stacks, possible_moves)

    return possible_moves

def solve(game, num_loops=10000):
    """Solve the puzzle

    :param game: Game to solve
    :param num_loops: Number of loops to run before exiting the solver
    :return: Moves to play the game
    """
    game = copy.deepcopy(game)
    stack_indices = [i for i in range(game.get_num_stacks())]
    moves = list(itertools.permutations(stack_indices, 2))

    move_history = []                                   # All the moves the solver has performed
    possible_moves = {}                                 # All of the possible moves the can do in a given situation
    STARTING_STACKS = copy.deepcopy(game.stacks)        # Starting stack configuration
    stack_history = [(0, STARTING_STACKS)]              # The stack states the solution has passed through

    with open('model/log.txt', 'w') as file:
        file.write(f'{game.name}\n\n')
        loop = 0
        while not game.is_solved():
            if loop > num_loops:
                print('Out of loops!')
                file.write(f'Out of loops!\n***** SOLUTION *****\n{move_history}')
                return move_history
            loop += 1

            state_str = '\n'.join((str(stack) for stack in game.stacks))
            file.write(f'** {loop} **\n{state_str}\n')

            # Generate all possible moves and filter out those that are invalid
            if state_str not in possible_moves.keys():
                possible_moves[state_str] = filter_moves(moves, game)

                file.write('Generating new moves\n')
                file.write(f'{possible_moves[state_str]}\n')

            # No moves
            if len(possible_moves[state_str]) == 0:
                file.write('No possible moves at current state, backtracking\n\n')
                if len(stack_history) == 0:
                    stack_history.append((loop, copy.deepcopy(STARTING_STACKS)))
                game.stacks = stack_history.pop()[1]
                move_history.pop()

            # There are possible moves that can be performed
            else:
                file.write('Moves are available\n')
                stack_history.append((loop, copy.deepcopy(game.stacks)))

                chosen_move = possible_moves[state_str].pop(0)
                file.write(f'Chosen move: {chosen_move}\n')

                # Optimize the move if its filling a stack up
                chosen_move = fill_homog_efficiently(game.stacks, chosen_move)

                game.move_pieces(chosen_move)
                move_history.append(chosen_move)

                file.write('\n')

        # Clean up the moves by removing redundancies and inefficiencies
        move_history = clean_up_moves(move_history)
        file.write(f'\n**** SOLUTION *****\n{move_history}')

    return move_history
