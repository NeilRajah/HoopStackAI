"""
main
Author: Neil Balaskandarajah
Created on: 17/06/2020
AI for solving hoop stack game
"""
import time
import pygame
from game import Game
import solver
from graphics import display
import itertools
import copy
import levels

# game = Game(3, 'Sort Hoop Level 3')
# game.add_stacks([
#     [pi, o, pi],
#     [],
#     [pi, o, o]
# ])

def solution_test(max_stack_size, game_name, stacks):
    game = Game(max_stack_size, game_name)
    game.add_stacks(stacks)
    disp = display.Display(game)
    # disp.play_game()

    s = solver.Solver()
    solution = s.solve(game)
    print_n_at_a_time(solution, 3)
    disp.play_moves(solution, animating=True)

#lvl 1
# game = Game(3)
# print(game.add_stack([c]))
# print(game.add_stack([c,c]))

#lvl 2
# game = Game(3)
# game.add_stack([1, 2, 2])
# game.add_stack([1, 1, 2])
# game.add_stack([])

#lvl 3
# game = Game(3)
# print(game.add_stack([1, 2, 2]))
# print(game.add_stack([1, 1, 2]))
# print(game.add_stack([]))

#lvl 4
# game = Game(4)
# print(game.add_stack([1, 1, 2, 1]))
# print(game.add_stack([2, 2, 1, 2]))
# print(game.add_stack([]))
# print(game.add_stack([]))

#lvl 5
# game = Game(5)
# print(game.add_stack([1, 2, 1, 1, 2]))
# print(game.add_stack([]))
# print(game.add_stack([2, 1, 2, 1, 2]))
# print(game.add_stack([]))

#lvl 6, inefficiently fills stacks
# game = Game(3)
# print(game.add_stack([1, 2, 3]))
# print(game.add_stack([1, 3, 2]))
# print(game.add_stack([2, 1, 3]))
# print(game.add_stack([]))
# print(game.add_stack([]))

#lvl 7, inefficiently fills stacks; move empty to end case
# game = Game(3)
# print(game.add_stack([1, 2, 3]))
# print(game.add_stack([]))
# print(game.add_stack([3, 1, 2]))
# print(game.add_stack([3, 2, 1]))
# print(game.add_stack([]))

#lvl 8
# game = Game(4)
# print(game.add_stack([1, 1, 2, 1]))
# print(game.add_stack([2, 1, 2, 2]))
# print(game.add_stack([]))
# print(game.add_stack([]))

#lvl 9, inefficient filling case
# game = Game(5)
# print(game.add_stack([1, 2, 2, 1, 2]))
# print(game.add_stack([]))
# print(game.add_stack([1, 1, 2, 2, 1]))
# print(game.add_stack([]))

#lvl 10
# game = Game(3, name="Level 10")
# print(game.add_stack([]))
# print(game.add_stack([1, 2, 2]))
# print(game.add_stack([2, 1, 3]))
# print(game.add_stack([3, 1, 3]))
# print(game.add_stack([]))

#lvl 11, inefficient filling at end
# game = Game(3, "Level 11")
# print(game.add_stack([1, 2]))
# print(game.add_stack([2, 3, 4]))
# print(game.add_stack([2, 1, 3]))
# print(game.add_stack([3, 5, 4]))
# print(game.add_stack([1]))
# print(game.add_stack([4, 5, 5]))

#lvl 12, inefficient filling at end
# game = Game(4, "Level 12")
# print(game.add_stack([1, 2, 3]))
# print(game.add_stack([2, 1, 1]))
# print(game.add_stack([3, 2]))
# print(game.add_stack([3, 1, 2, 3]))

#lvl 13, inefficient filling throughout
# game = Game(5, "Level 13")
# print(game.add_stack([1,2,1,3,2]))
# print(game.add_stack([4]))
# print(game.add_stack([3]))
# print(game.add_stack([4,3,4,1]))
# print(game.add_stack([3,4,2,1,1]))
# print(game.add_stack([4,2,2,3]))

#lvl 14, inefficient filling
# game = Game(4, "Level 14")
# print(game.add_stack([1]))
# print(game.add_stack([2, 3, 2]))
# print(game.add_stack([4, 2]))
# print(game.add_stack([4, 2]))
# print(game.add_stack([1, 3, 1, 3]))
# print(game.add_stack([4, 3, 1, 4]))

#lvl 15, inefficient filling, moved to empty (wasn't high priority)
# game = Game(4, "Level 15")
# print(game.add_stack([1]))
# print(game.add_stack([2, 1, 3, 2]))
# print(game.add_stack([3]))
# print(game.add_stack([3, 1, 2]))
# print(game.add_stack([3, 2, 1]))

#lvl 16, lots of inefficient stacking
# game = Game(5, "Level 16")
# game.add_stack([])
# game.add_stack([1, 2, 1])
# game.add_stack([3, 2, 4, 5])
# game.add_stack([1, 3, 5, 3, 2])
# game.add_stack([5, 4, 2, 4, 4])
# game.add_stack([3, 5, 4, 2, 1])
# game.add_stack([3, 5, 1])

#lvl 41, inefficient stacking
# game = Game(5)
# game.add_stack([1, 2])
# game.add_stack([3,2,1,1])
# game.add_stack([3,1,3,3])
# game.add_stack([1,2,3,2,2])

#lvl 57
# game = Game(5)
# game.add_stack([1, 2, 3, 3])
# game.add_stack([4, 3, 2, 1, 1])
# game.add_stack([5, 2, 5, 1, 4])
# game.add_stack([3, 1, 5, 2, 2])
# game.add_stack([4, 3, 5, 5])
# game.add_stack([4, 4])

#lvl 58, efficient solve
# game = Game(4, "Level 58")
# game.add_stack([1, 2, 1, 1])
# game.add_stack([3, 4, 3, 2])
# game.add_stack([3, 1, 4])
# game.add_stack([2, 4, 5, 5])
# game.add_stack([3])
# game.add_stack([2, 4, 5, 5])

#lvl 59
# game = Game(5)
# game.add_stack([1, 2, 3, 3])
# game.add_stack([4])
# game.add_stack([4, 4, 1, 5, 5])
# game.add_stack([5, 4, 6, 2, 2])
# game.add_stack([5, 2, 6, 3, 1])
# game.add_stack([2, 6, 3, 6, 6])
# game.add_stack([5, 4, 3, 1, 1])

#lvl 60, inefficient stacking
# game = Game(3)
# game.add_stack([c])
# game.add_stack([pi])
# game.add_stack([g])
# game.add_stack([pi, c, pu])
# game.add_stack([pu, g, c])
# game.add_stack([pi, pu, g])

#lvl 61, efficient solve
# game = Game(3)
# game.add_stack([1])
# game.add_stack([2, 3, 4])
# game.add_stack([4, 2])
# game.add_stack([1, 4, 5])
# game.add_stack([3, 5, 5])
# game.add_stack([2, 6, 3])
# game.add_stack([1, 7, 7])
# game.add_stack([7, 6, 6])

#lvl 62, inefficient stacking right at end
# game = Game(4)
# game.add_stack([1, 2, 3, 3])
# game.add_stack([4, 5, 4])
# game.add_stack([6, 4, 5, 6])
# game.add_stack([7, 6, 2, 2])
# game.add_stack([5, 7, 1, 1])
# game.add_stack([7])
# game.add_stack([2, 7, 4, 5])
# game.add_stack([6, 3, 3, 1])

#lvl 69, deadlock
# game = Game(5, "Nice!")
# game.add_stack([1, 2, 3, 3, 4])
# game.add_stack([4, 3])
# game.add_stack([2, 4, 5, 5, 2])
# game.add_stack([3, 4, 1])
# game.add_stack([1, 5, 2, 5, 5])
# game.add_stack([4, 3, 1, 1, 2])

#app level 107, solved but weird backtracking issue (seems to be with self.history)
# game = Game(4, "App Level 107")
# game.add_stack([1, 2, 3, 3])
# game.add_stack([4, 5, 6])
# game.add_stack([6, 2, 1, 1])
# game.add_stack([5, 4])
# game.add_stack([3, 5, 2, 7])
# game.add_stack([7, 3, 6, 2])
# game.add_stack([4, 5, 4])
# game.add_stack([6, 7, 7, 1])

#app level 108
# game = Game(4, "App Level 108")
# game.add_stack([1, 2, 3, 2])
# game.add_stack([2, 4, 5, 5])
# game.add_stack([6])
# game.add_stack([4, 5, 7, 7])
# game.add_stack([6, 6, 3, 1])
# game.add_stack([3, 1, 2, 3])
# game.add_stack([6, 1, 4])
# game.add_stack([4, 5, 7, 7])

#app lvl 109, weird backtracking issue
# game = Game(5, "App Level 109")
# game.add_stack([1, 2, 3, 3])
# game.add_stack([3, 2, 4, 4])
# game.add_stack([2, 1, 2])
# game.add_stack([2, 3, 1, 1])
# game.add_stack([4, 1, 3, 4, 4])

#app level 110, stuck in forced deadlock from repeating moves, explodes somewhere along the way
# game = Game(5)
# game.add_stack([1,2,1,1])
# game.add_stack([3,2])
# game.add_stack([2,1,3,3,4])
# game.add_stack([5,4,4,6,6])
# game.add_stack([6,7,7,4,4])
# game.add_stack([7,2,2,5,5])
# game.add_stack([3,5,5,3])
# game.add_stack([1,6,7,6,7])

#App level 123
# game = Game(4)
# game.add_stack([1,2,2,3])
# game.add_stack([4])
# game.add_stack([5,6,5,6])
# game.add_stack([1,3,1,7])
# game.add_stack([4,4,5,6])
# game.add_stack([4,6,1])
# game.add_stack([5,7,7,2])
# game.add_stack([2,3,3,7])

#Test for non-numbers
# game = Game(3)
# game.add_stack(['A'])
# game.add_stack(['A', 'A'])

#App level 124
# game = Game(5)
# game.add_stack([1,2,3])
# game.add_stack([2,1,4,4])
# game.add_stack([4,1,1,])
# game.add_stack([2,4,1,3,3])
# game.add_stack([2,4,3,3,2])

#App level 129
# game = Game(5)
# game.add_stack(['pink', 'red', 'red', 'pink', 'pink'])
# game.add_stack(['blue', 'green', 'green'])
# game.add_stack(['blue', 'cyan', 'cyan', 'pink', 'pink'])
# game.add_stack(['green', 'cyan', 'purple', 'purple'])
# game.add_stack(['blue', 'purple', 'green', 'red', 'red'])
# game.add_stack(['blue', 'green', 'blue'])
# game.add_stack(['purple', 'red', 'purple', 'cyan', 'cyan'])

#App level 130
# game = Game(5)
# game.add_stacks([
#     [c],
#     [c,c,b,g,g],
#     [pi,c,b,pi,pi],
#     [b,g,r,pu,pu],
#     [r,g,pu,r,r],
#     [c,r,b,b],
#     [pu,g,pu,pi,pi]
# ])

#App level 131
# game = Game(5)
# game.add_stacks([
#     [r,g],
#     [pu,c,pi,r,g],
#     [pu,r,pi],
#     [pi,pu,g,pu],
#     [c,pi,c,r],
#     [r,pu,g,c,g],
#     [c,pi]
# ])

#App level 132
# game = Game(5)
# game.add_stacks([
#     [g,c,c,g],
#     [pi,g,pi,pi,g],
#     [c,g,pi,pi],
#     [c,c]
# ])

#App level 133
# game = Game(5)
# game.add_stacks([
#     [pi,pu,c,c],
#     [pi,g,pu,pi,pu],
#     [g,pi,g,pi],
#     [c,pu,g,c,c],
#     [g,pu]
# ])

#App level 134
# game = Game(5)
# game.add_stacks([
#     [c,pi,c],
#     [g,c,g,pi,pi],
#     [c,pi],
#     [c,pi,g,pu,pu],
#     [g,pu,g,pu,pu]
# ])

#App level 135, backtracking on move 0 error
# game = Game(5)
# game.add_stacks([
#     [g,r,r,c,c],
#     [pu,pi,pu,g,g],
#     [pi,pi,pu],
#     [pi,pu],
#     [c,pu,r,g,r],
#     [g,pi,c,c,r]
# ])

#App level 136
# game = Game(5)
# game.add_stacks([
#     [pu,r],
#     [g],
#     [c,r,pi],
#     [g,c,pi,g,pu],
#     [pu,g,r,c,pi],
#     [pi,c,pi,r,r],
#     [c,pu,g,pu]
# ])

#App level 137
# game = Game(5)
# game.add_stacks([
#     [c,b,b,c,c],
#     [pi,g,g],
#     [pu,pu,pi,pi],
#     [g,c,c,pu,pu],
#     [b,r,g,g,r],
#     [pu,pi,b],
#     [r,b,pi,r,r]
# ])

#Browser level 19
# game = Game(3)
# game.add_stacks([
#     [r,c],
#     [g],
#     [g,c,pi],
#     [r,pi,pu],
#     [g,c,r],
#     [pu,b,b],
#     [pi,b,pu]
# ])

#App level 140
# game = Game(5)
# game.add_stacks([
#     [g,r,b,r,c],
#     [c,g],
#     [pu,pi,pu,pi,pi],
#     [b,pu,pu,b,r],
#     [c,g,r,r],
#     [c,c,g,b],
#     [g,b,pi,pu,pi]
# ])

#App level 141
# game = Game(4)
# game.add_stacks([
#     [pu,o,c,c],
#     [o,g,pi,g],
#     [pu],
#     [c,pi,g,pu],
#     [r,g,r,r],
#     [b,r,b,b],
#     [pu,o,o],
#     [c,b,pi,pi]
# ])

#Level 49
# game = Game(4)
# game.add_stacks([
#     [pu,c,b,pu],
#     [b,c,g,g],
#     [r,pu,pi],
#     [r],
#     [r,pi,pu,c],
#     [r,pi,b,b],
#     [pi,c,g,g]
# ])
#
# game = Game(3)
# game.add_stacks([
#     [b, r, r],
#     [b, r],
#     [b]
# ])

#Image created game
# game = Game(4)
# stacks = [
#     ['red '],
#     ['blue', 'blue', 'pink', 'red '],
#     ['gren', 'gren', 'cyan', 'pink'],
#     ['cyan', 'purp', 'pink', 'red '],
#     ['pink', 'purp', 'red '],
#     ['gren', 'gren', 'cyan', 'blue'],
#     ['purp', 'blue', 'cyan', 'purp']
# ]
# game.add_stacks([stack[::-1] for stack in stacks])

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

def print_n_at_a_time(lis, n, msg=''):
    if msg != '':
        print(msg)
    for i, elem in enumerate(lis):
        print(elem, end=' ')
        if (i + 1) % n == 0:
            print()

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
    prev_moves = [(0, 1), (0, 2), (1, 0), (1, 2)]
    # print_n_at_a_time(possible_moves, 3, msg='possible_moves')
    # print_n_at_a_time(prev_moves, 3, msg='prev_moves')

    ans = solver.remove_opposite(possible_moves, prev_moves)
    # print_n_at_a_time(ans, 3, msg='\nanswer')

def test_remove_incompatibles():
    print('Testing remove_incompatibles')
    possible_moves = list(itertools.permutations([i for i in range(5)], 2))
    stacks = [[1, 1], [1], [2, 3], [3, 3, 2], []]
    max_stack_size = 3

    ans = solver.remove_incompatibles(stacks, possible_moves, max_stack_size)
    # print_n_at_a_time(ans, 3)

def test_remove_all_same_to_diferent():
    print('Testing remove_all_same_to_different')
    stacks = [[1, 1], [2, 1], [2, 2]]
    possible_moves = list(itertools.permutations([i for i in range(len(stacks))], 2))

    ans = solver.remove_all_same_to_different(stacks, possible_moves)
    # print_n_at_a_time(ans, 3)

if __name__ == '__main__':
    test_is_stack_solved_or_empty()
    test_is_stack_homog()
    test_fill_homog_efficiently()
    test_clean_up_moves()
    test_remove_empty_solved()
    test_remove_opposite()
    test_remove_incompatibles()
    test_remove_all_same_to_diferent()

    solution_test(4, 'App Level 68', levels.level_68_app)
    # solution_test(5, 'App Level 69', levels.level_69_app)
    # solution_test(5, 'App Level 70', levels.level_70_app)