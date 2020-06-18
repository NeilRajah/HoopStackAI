"""
game
Author: Neil Balaskandarajah
Created on: 18/06/2020
Game class with all interactions
"""

class Game():
    def __init__(self, num_rings):
        """
        Create a game by declaring its max size
        """
        self.num_rings = num_rings
        self.stacks = dict()
        self.STACK_LABELS = 'ABCDEFGH'
        self.label_idx = 0

    def add_stack(self, stack):
        """
        Add a stack to the game
        return - Information on stack added
        """
        if self.label_idx > len(self.STACK_LABELS):
            raise Exception('Cannot have more than {} stacks!'.format(len(self.STACK_LABELS)))
        if not isinstance(stack, list):
            raise Exception('Stack must be a Python list!')
        self.stacks[self.STACK_LABELS[self.label_idx]] = stack
        self.label_idx += 1
        return "Stack {} added: {}".format(self.STACK_LABELS[self.label_idx-1], stack)

    def move_piece(self, pair_tup):
        """
        Move a piece from the top of one stack to the other
        """
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]
        b.append(a.pop())

    def display(self):
        """
        Print the game out to the console
        """
        print('-' * (len(self.stacks) + 2))
        for i in reversed(range(self.num_rings)):
            row = ""
            for lbl in self.stacks:
                if i > len(self.stacks[lbl])-1:
                    row = row + "  "
                else:
                    row = row + "{} ".format(self.stacks[lbl][i])
            print(row)
        print('-' * (len(self.stacks) + 2))

