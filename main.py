"""
main
Author: Neil Balaskandarajah
Created on: 17/06/2020
AI for solving hoop stack game
"""
from game import Game
from copy import deepcopy
from itertools import permutations

def is_solved(maxSize, stacks):
    """Check if all stacks are solved"""
    for lis in stacks:
        if len(lis) != 0 and len(lis) != maxSize:
            return False
    return True

def can_move(a, b):
    """If top of stacks are same, or if b is empty"""
    return not len(a) == 0 and (len(b) == 0 or a[-1] == b[-1])

def solve(maxSize, s):
    all_moves = list(permutations(s, 2))
    print (all_moves)

    # if perms.__contains__(('A', 'C')):
    #     print("yes")
    # removals = set()
    # for p in perms:
    #     if 'A' in p:
    #         removals.add(p)
    # perms = perms - removals 
    # print(perms)
    
#------------------------Main Script------------------------#

#Create stacks
# s = dict()
# maxSize = 3
# s['A'] = [1, 2, 2]
# s['B'] = [2, 2, 1]
# s['C'] = []
# so = deepcopy(s) #for printing after
 
# solve(maxSize, s)

game = Game(3)
print(game.add_stack([1, 2, 2]))
print(game.add_stack([2, 2, 1]))
print(game.add_stack([]))
game.display()

game.move_piece(('A', 'C'))
game.display()