"""
test_solver
Author: Neil Balaskandarajah
Created on: 15/05/2023
Testing functions from solver
"""
import game
import solver
from graphics import display
import itertools
import copy
import levels
from util import print_n_at_a_time

def test_is_stack_solved_or_empty():
    print('Testing is_stack_solved_or_empty')
    assert solver.is_stack_solved_or_empty([], 3) == True, 'should be true'
    assert solver.is_stack_solved_or_empty([1, 1, 1], 3) == True, 'should be true'
    assert solver.is_stack_solved_or_empty([2, 1], 3) == False, 'should be false'

def test_is_stack_homog():
    print('Testing is_stack_homog')
    assert solver.is_stack_homog([]) == False
    assert solver.is_stack_homog([1, 1, 1]) == True
    assert solver.is_stack_homog([1, 2, 3]) == False

def test_fill_homog_efficiently():
    print('Testing fill_homog_efficiently')
    stacks = [[2, 1, 1, 1], [1], [1, 1]]
    assert solver.fill_homog_efficiently(stacks, (1, 2)) == (1, 2)
    assert solver.fill_homog_efficiently(stacks, (2, 1)) == (1, 2)
    assert solver.fill_homog_efficiently(stacks, (0, 1)) == (0, 1)
    assert solver.fill_homog_efficiently(stacks, (1, 0)) == (1, 0)

def test_clean_up_moves():
    print('Testing clean_up_moves')
    ans = solver.clean_up_moves([(0, 1), (1, 2)])
    solution = [(0, 2)]
    if not all([move == sol_move for move, sol_move in zip(ans, solution)]):
        raise AssertionError('Lol not right')
    ans = solver.clean_up_moves([(0, 1), (0, 1)])
    solution = [(0, 1), (0, 1)]
    if not all([move == sol_move for move, sol_move in zip(ans, solution)]):
        raise AssertionError('Lol not right')

def test_remove_empty_solved(printing=False):
    print('Testing remove_empty_solved')
    stacks = [[], [1, 1, 1], [2, 2], [2]]
    possible_moves = list(itertools.permutations([i for i in range(len(stacks))], 2))
    max_stack_size = 3

    if printing:
        print('Possible moves: {}'.format(len(possible_moves)))
        print_n_at_a_time(possible_moves, 3)

        ans = solver.remove_empty_solved(stacks, copy.deepcopy(possible_moves), max_stack_size)
        print('Answer: {}'.format(len(ans)))
        print_n_at_a_time(ans, 3)
        # if len(possible_moves) == len(ans):
        #     print('lol wut r u doing... should be less moves styll....')

def test_remove_opposite():
    print('Testing remove_opposite')
    possible_moves = list(itertools.permutations([i for i in range(3)], 2))
    last_move = (1, 0)
    # print_n_at_a_time(possible_moves, 3, msg='possible_moves')

    ans = solver.remove_opposite(possible_moves, last_move)
    # print_n_at_a_time(ans, 3, msg='\nanswer')
    # print()

def test_remove_incompatibles():
    print('Testing remove_incompatibles')
    # stacks = [[1, 1, 1], []]
    stacks = levels.level_16
    possible_moves = list(itertools.permutations([i for i in range(len(stacks))], 2))
    max_stack_size = game.get_max_stack_size(stacks)

    ans = solver.remove_incompatibles(stacks, possible_moves, max_stack_size)
    print_n_at_a_time(ans, 3)

def test_remove_all_same_to_diferent():
    print('Testing remove_all_same_to_different')
    stacks = [[1, 1], [2, 1], [2, 2]]
    possible_moves = list(itertools.permutations([i for i in range(len(stacks))], 2))

    ans = solver.remove_all_same_to_different(stacks, possible_moves)
    # print_n_at_a_time(ans, 3)

def test_levels(testcases, num_loops=100, animating=False):
    # test_game = game.Game(game.get_max_stack_size(testcases[0]), stacks=testcases[0])
    disp = display.Display(None)

    for name in testcases:
        print(name)
        case = testcases[name]
        test_game = game.Game(game.get_max_stack_size(case), stacks=case, name=name)
        disp.game = test_game
        disp.setup()

        solution = solver.solve(test_game, num_loops=num_loops)
        print_n_at_a_time(solution, 5)

        # input()
        disp.play_moves(solution, animating=animating)
        # disp.play_game()

if __name__ == '__main__':
    # test_is_stack_solved_or_empty()
    # test_is_stack_homog()
    # test_fill_homog_efficiently()
    # test_clean_up_moves()
    # test_remove_empty_solved()
    # test_remove_opposite()
    # test_remove_incompatibles()
    # test_remove_all_same_to_diferent()
    # test_remove_infinite_loops()

    # test_game = Game(3, 'Test Game')
    # test_game.add_stacks([[1, 1, 1], []])
    # print(test_game.is_solved())

    # level = levels.level_2
    # game_to_play = game.Game(game.get_max_stack_size(level), 'Level 2', level)
    # disp = display.Display(game_to_play)
    # disp.play_game()

    test_levels({
                 'Level 1': levels.level_1,
                 'Level 2': levels.level_2,
                 'Level 3': levels.level_3,
                 'Level 4': levels.level_4,
                 'Level 5': levels.level_5,
                 'Level 6': levels.level_6,
                 'Level 7': levels.level_7,
                 'Level 11': levels.level_11,
                 'Level 16': levels.level_16,
                 'Level 68': levels.level_68_app,
                 'Level 70': levels.level_70_app,
                 'Level 23': levels.level_23,
                 'Level 24': levels.level_24
                }, num_loops=100, animating=True)
