"""
main
Author: Neil Balaskandarajah
Created on: 17/06/2020
AI for solving hoop stack game
"""
from game import Game

#lvl 1
# game = Game(3)
# print(game.add_stack([1]))
# print(game.add_stack([1, 1]))

#lvl 2
# game = Game(3)
# print(game.add_stack([1, 2, 2]))
# print(game.add_stack([1, 1, 2]))
# print(game.add_stack([]))

#lvl 3
# game = Game(3)
# print(game.add_stack([1, 2, 1]))
# print(game.add_stack([]))
# print(game.add_stack([1, 2, 2]))

#lvl 4
# game = Game(4)
# print(game.add_stack([1, 1, 2, 1]))
# print(game.add_stack([2, 2, 1, 2]))
# print(game.add_stack([]))
# print(game.add_stack([]))

#lvl 5, stuck in repeating loop with red hoops
# game = Game(5)
# print(game.add_stack([1, 2, 1, 1, 2]))
# print(game.add_stack([]))
# print(game.add_stack([2, 1, 2, 1, 2]))
# print(game.add_stack([]))

#lvl 6
# game = Game(3)
# print(game.add_stack([1, 2, 3]))
# print(game.add_stack([1, 3, 2]))
# print(game.add_stack([2, 1, 3]))
# print(game.add_stack([]))
# print(game.add_stack([]))

#lvl 7, stuck in classic 3-way repetition
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

#lvl 9, stuck in repeating loop with green hoop
# game = Game(5)
# print(game.add_stack([1, 2, 2, 1, 2]))
# print(game.add_stack([]))
# print(game.add_stack([1, 1, 2, 2, 1]))
# print(game.add_stack([]))

#lvl 10, stuck in deep repeating loop
# game = Game(3)
# print(game.add_stack([]))
# print(game.add_stack([1, 2, 2]))
# print(game.add_stack([2, 1, 3]))
# print(game.add_stack([3, 1, 3]))
# print(game.add_stack([]))

#lvl 11, hit deadlock
# game = Game(3)
# print(game.add_stack([1, 2]))
# print(game.add_stack([2, 3, 4]))
# print(game.add_stack([3, 5, 4]))
# print(game.add_stack([1]))
# print(game.add_stack([4, 5, 5]))

#lvl 12
game = Game(4)
print(game.add_stack([1, 2, 3]))
print(game.add_stack([2, 1, 1]))
print(game.add_stack([3, 2]))
print(game.add_stack([3, 1, 2, 3]))

#lvl 13, hoops repeatedly moving to empty stack
game = Game(5)
print(game.add_stack([1,2,1,3,2]))
print(game.add_stack([4]))
print(game.add_stack([3]))
print(game.add_stack([4,3,4,1]))
print(game.add_stack([3,4,2,1,1]))
print(game.add_stack([4,2,2,3]))

game.display()
game.solve()