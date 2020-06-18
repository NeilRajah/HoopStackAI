"""
hoop
Author: Neil Balaskandarajah
Created on: 17/06/2020
AI for solving hoop stack game
"""
from tree import Tree
from copy import deepcopy
from itertools import permutations

class Node(object):
    #For creating tree
    pass

def move_elem(a, b):
    #Move an element from a to b
    b.append(a.pop())

def is_solved(maxSize, stacks):
    #Check if all stacks are solved
    for lis in stacks:
        if len(lis) != 0 and len(lis) != maxSize:
            return False
    return True

def can_move(a, b):
    #If top of stacks are same, or if b is empty
    return not len(a) == 0 and (len(b) == 0 or a[-1] == b[-1])

def solve(maxSize, stacksP):
    stacks = list(stacksP)
    #Solve the puzzle by forward stepping
    for i in range(len(stacks)-1): #pairs
        if (can_move(stacks[i], stacks[i+1])):
            move_elem(stacks[i], stacks[i+1])
            if is_solved(maxSize, stacks):
                return ("{}{}".format(i, i+1), stacks)

        if can_move(stacks[i+1], stacks[i]): 
            move_elem(stacks[i+1], stacks[i])
            if is_solved(maxSize, stacks):
                return ("{}{}".format(i+1, i), stacks)
    return ("NS", stacks)

s1 = [1,2,2]
s2 = [2,2,1]
s3 = []
s = [s1, s2, s3]
so = deepcopy(s)

# print(can_move([1], [1]))
# print(can_move(s1, s2))

moves, final = solve(3, s)
# print("{}: {} -> {}".format(moves, so, final))

perms = set(permutations('ABC', 2))
print(perms)
#check if permutations contains a specific pair (remove one element)
if perms.__contains__(('A', 'C')):
    print("yes")

#remove all permutations containing a single element
removals = set()
for p in perms:
    if 'A' in p:
        removals.add(p)
perms = perms - removals 

#2, 6, 12, 20, 30, 42, 56 - perm sizes for each num_stack [2,inf)