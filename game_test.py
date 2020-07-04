"""
main
Author: Neil Balaskandarajah
Created on: 17/06/2020
AI for solving hoop stack game
"""
import time

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
# game.add_stack([1])
# game.add_stack([2])
# game.add_stack([3])
# game.add_stack([2, 1, 4])
# game.add_stack([4, 3, 1])
# game.add_stack([2, 4, 3])

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
c = '1'; b = '2'; g = '3'; r = '4'; pi = '5'; pu = '6'; o = '7'
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
game = Game(3)
game.add_stacks([
    [r,c],
    [g],
    [g,c,pi],
    [r,pi,pu],
    [g,c,r],
    [pu,b,b],
    [pi,b,pu]
])

game.display()
t1 = time.time()
game.solve(print_moves=False, debug=True)
game.display_history()