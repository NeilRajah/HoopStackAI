"""
game
Author: Neil Balaskandarajah
Created on: 18/06/2020
Game class with all interactions
"""
from itertools import permutations
from copy import deepcopy

class Game():
    def __init__(self, num_rings):
        """
        Create a game by declaring its max size
        """
        self.num_pieces = num_rings         #Max number of pieces on a stack
        self.stacks = dict()                #Stacks containing pieces
        self.STACK_LABELS = 'ABCDEFGH'      #Alphabetical labels for each stack
        self.label_idx = 0                  #Index of the current label for adding stakcs
        self.history = []                   #Move history
        self.prev_move = ''                 #Previous move

    def add_stack(self, stack):
        """
        Add a stack to the game, ordered top to bottom (ie. index 0 is top, index -1 is bottom)
        """
        if self.label_idx > len(self.STACK_LABELS):
            raise Exception('Cannot have more than {} stacks!'.format(len(self.STACK_LABELS)))
        if not isinstance(stack, list):
            raise Exception('Stack must be a Python list!')
        
        stack.reverse()
        self.stacks[self.STACK_LABELS[self.label_idx]] = stack
        self.label_idx += 1
        return "Stack {} added: {}".format(self.STACK_LABELS[self.label_idx-1], stack)

    def move_pieces(self, pair_tup):
        """
        Move a piece from the top of one stack to the other
        """
        if not self.is_pair_compatible(pair_tup):
            raise Exception("Stacks {} and {} are not compatible!".format(pair_tup[0], pair_tup[1]))
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]
        b.append(a.pop())
        self.history.append(pair_tup)
        self.prev_move = pair_tup
        return "Moved {} from {} to {}".format(b[-1], pair_tup[0], pair_tup[1])

    def is_pair_compatible(self, pair_tup):
        """
        Check if a pair of stacks are compatible
        """
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]

        if len(a) == 0: return False
        if len(b) == 0: return True
        if len(b) == self.num_pieces: return False
        if a[-1] == b[-1]: return True
        return False

    def display(self):
        """
        Print the game out to the console
        """
        print('-' * (len(self.stacks) + 4))
        for i in reversed(range(self.num_pieces)):
            row = ""
            for lbl in self.stacks:
                if i > len(self.stacks[lbl])-1:
                    row = row + "  "
                else:
                    row = row + "{} ".format(self.stacks[lbl][i])
            print(row)
        print('-' * (len(self.stacks) + 4))

    def display_history(self):
        """
        Print the move history to the console
        """
        out = "{}: ".format(len(self.history))
        for move in self.history:
            for stack_label in move:
                out = out + stack_label
            out = out + " "
        print(out)

    def move_and_display(self, pair_tup):
        """
        Move a piece and print game information to the console
        """
        self.move_pieces(pair_tup)
        self.display()
        self.display_history()

    def is_solved(self):
        """
        Return if the game is solved or not
        """
        for stack in self.stacks:
            if not self.is_stack_solved_or_empty(stack):
                return False
        return True

    def is_stack_solved_or_empty(self, lbl):
        """
        Return if the stack is solved or not
        """
        return len(self.stacks[lbl]) == 0 or \
            (len(set(self.stacks[lbl])) == 1 and len(self.stacks[lbl]) == self.num_pieces)

    def solve(self):
        """
        Solve the puzzle
        """
        print("*******START*******")

        #Start the solution by calculating all possible moves
        self.moves = list(permutations(self.stacks, 2))

        num_loops = 50
        loop = 0
        while not self.is_solved():
            if loop >= num_loops: print("too many loops"); break

            #Create a copy of the moves for this iteration
            pairs = deepcopy(self.moves)

            #Check for empty or solved stacks
            solved_empty = []
            for stack in self.stacks:
                if self.is_stack_solved_or_empty(stack):
                    solved_empty.append(stack)

            #Eliminate all moves with pieces going from empty or solved pairs
            remove = list()
            for pair in pairs:
                for stack in solved_empty:
                    if pair[0] == stack:
                        remove.append(pair)
            pairs = [item for item in pairs if item not in remove] #subtract the lists

            #Eliminate the move that is the opposite as the previous move
            if (self.prev_move != ''):
                for pair in pairs:
                    if pair[0] == self.prev_move[1] and pair[1] == self.prev_move[0]:
                        pairs.remove(pair)
                        break

            #Eliminate all moves between incompatible stacks
            remove.clear()
            for pair in pairs:
                if not self.is_pair_compatible(pair):
                    remove.append(pair)
            pairs = [item for item in pairs if item not in remove]

            #Move the piece at the first of the moves left
            self.move_pieces(pairs[0])

            loop += 1
        if self.is_solved():
            print("*******SOLVED*******")
        self.display()
        self.display_history()
        