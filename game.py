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
        self.states = dict()                #All moves done and stack state

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
                    row = row + "_ "
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

    def solve(self, display=False):
        """
        Solve the puzzle
        """
        print("*******START*******")

        #Start the solution by calculating all possible moves
        self.moves = list(permutations(self.stacks, 2))

        num_loops = 50; loop = 0 #for preventing infinite loops
        while not self.is_solved():
            if loop >= num_loops: print("\nToo many loops"); break

            #Create a copy of the moves for this iteration
            pairs = deepcopy(self.moves)
            self._print_tup(pairs, "inital")

            #Filter out invalid moves
            self._remove_empty_solved(pairs)
            self._remove_opposite(pairs)
            self._remove_incompatibles(pairs)            

            self._print_tup(pairs, "remaining")

            #Move the piece at the first of the moves left
            if len(pairs) == 0: raise Exception("Deadlock!")
            if display: self.move_and_display(pairs[0])
            else: self.move_pieces(pairs[0])

            loop += 1
            
        if self.is_solved():
            print("*******SOLVED******")
        self.display()
        self.display_history()

    def _remove_empty_solved(self, pairs):
        """
        Remove the empty and solved stacks from the current set of moves
        """
        #Check for empty or solved stacks
        solved_empty = []
        for stack in self.stacks:
            if self.is_stack_solved_or_empty(stack):
                solved_empty.append(stack)

        #Eliminate all moves with pieces going from empty or solved pairs
        remove = []
        for pair in pairs:
            for stack in solved_empty:
                if pair[0] == stack:
                    remove.append(pair)
        self._print_tup(remove, "empty/solved")
        pairs = [item for item in pairs if item not in remove] #subtract the lists

    def _remove_opposite(self, pairs):
        """
        Remove the opposite of the last move to avoid getting stuck in a loop
        """
        if (self.prev_move != ''):
            for pair in pairs:
                if pair[0] == self.prev_move[1] and pair[1] == self.prev_move[0]:
                    self._print_tup(pair, "opposites")
                    pairs.remove(pair)
                    break

    def _remove_incompatibles(self, pairs):
        """
        Remove moves between incompatible stacks
        """
        remove = []
        for pair in pairs:
            if not self.is_pair_compatible(pair):
                remove.append(pair)
        self._print_tup(remove, "incompatibles")
        
        pairs = [item for item in pairs if item not in remove]

    def _print_tup(self, group, msg):
        """
        All elements of a tuple in a String
        """
        elements = ''
        for tup in group:
            elements = elements + ''.join(tup) + ' '
        print("{}: {}".format(msg, elements))