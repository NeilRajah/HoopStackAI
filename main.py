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

#lvl 41
game = Game(5)
game.add_stack([1, 2])
game.add_stack([3,2,1,1])
game.add_stack([3,1,3,3])
game.add_stack([1,2,3,2,2])

game.display()
game.solve(print_moves=False, debug=False)