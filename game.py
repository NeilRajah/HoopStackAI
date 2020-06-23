"""
game
Author: Neil Balaskandarajah
Created on: 18/06/2020
Game class with all interactions
"""
import time
from itertools import permutations
from copy import deepcopy
import matplotlib.pyplot as plt

class Game():
    def __init__(self, num_rings, name=None):
        """
        Create a game by declaring its max size
        """
        if name: print(name)
        self.num_pieces = num_rings         #Max number of pieces on a stack
        self.stacks = dict()                #Stacks containing pieces
        self.STACK_LABELS = 'ABCDEFGH'      #Alphabetical labels for each stack
        self.label_idx = 0                  #Index of the current label for adding stakcs
        self.history = []                   #Move history
        self.prev_moves = []                #Previous move
        self.prev_pairs = []                #Moves that could be performed last iteration
        self.prev_stacks = []               #Remember the previous state of stacks for backtracking
        self.backtracking = False           #Whether backtracking or not

    def add_stack(self, stack):
        """
        Add a stack to the game, ordered top to bottom (ie. index 0 is top, index -1 is bottom)
        """
        if self.label_idx > len(self.STACK_LABELS):
            raise Exception('Cannot have more than {} stacks!'.format(len(self.STACK_LABELS)))
        if not isinstance(stack, list):
            raise Exception('Stack must be a Python list!')
        
        #Reverse stack so stack.pop() removes the top piece
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
        
        #Move from top of the first stack to the second
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]
        b.append(a.pop())

        #Save to history
        self.history.append(pair_tup)
        self.prev_moves.append(pair_tup)
        return "Moved {} from {} to {}".format(b[-1], pair_tup[0], pair_tup[1])

    def is_pair_compatible(self, pair_tup):
        """
        Check if a pair of stacks are compatible
        """
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]

        if len(a) == 0: return False                #Can't move from empty stack
        if len(b) == 0: return True                 #Can move to empty stack
        if len(b) == self.num_pieces: return False  #Can't move to full stack
        if a[-1] == b[-1]: return True              #Can move if top pieces are same
        return False

    def display(self):
        """
        Print the game out to the console
        """
        print('-' * (2*len(self.stacks)))
        for i in reversed(range(self.num_pieces)):
            row = ""
            for lbl in self.stacks:
                if i > len(self.stacks[lbl])-1:
                    row = row + "  "
                else:
                    row = row + "{} ".format(self.stacks[lbl][i])
            print(row)
        print('-' * (2*len(self.stacks)))

    def display_history(self):
        """
        Print the move history to the console
        """
        self._print_tup(self.history, len(self.history))

    def move_and_display(self, pair_tup):
        """
        Move a piece and print game information to the console
        """
        self.move_pieces(pair_tup)
        self.display()
        self.display_history()

    def _is_solved(self):
        """
        Return if the game is solved or not
        """
        for stack in self.stacks:
            if not self._is_stack_solved_or_empty(stack):
                return False
        return True

    def _is_stack_solved_or_empty(self, lbl):
        """
        Return if the stack is solved, empty or neither
        """
        return len(self.stacks[lbl]) == 0 or \
            (len(set(self.stacks[lbl])) == 1 and len(self.stacks[lbl]) == self.num_pieces)

    def _is_stack_homog(self, lbl):
        """
        Return if a stack is all the same color or not (False if empty)
        """
        return len(set(self.stacks[lbl])) == 1

    def _undo(self):
        """
        Undo the last move done (for backtracking)
        """
        if len(self.history) > 0:
            pair = self.history.pop()[::-1]  # opposite of last move done
            a = self.stacks[pair[0]]
            b = self.stacks[pair[1]]
            b.append(a.pop())
        if len(self.prev_moves) > 0: self.prev_moves.pop()

    def solve(self, print_moves=False, debug=False):
        """
        Solve the puzzle
        """
        self.print_moves = print_moves
        self.debug = debug
        print("*******START*******")

        #Start the solution by calculating all possible moves
        moves = list(permutations(self.stacks, 2)) #change to local?
        self.prev_pairs.append(deepcopy(moves))
        move_num = []
        t1 = time.time()

        num_loops = 100; loop = 0 #for preventing infinite loops
        while not self._is_solved():
            if loop >= num_loops: print("\nToo many loops"); break

            if self.backtracking:
                #Undo the last move, reset the pairs to the last set and move forward
                if self.debug: self._print_tup(pairs, 'pre-backtracking pairs')
                pairs = self.prev_pairs.pop()
                if len(self.prev_moves) > 0 and self.prev_moves[-1] in pairs: pairs.remove(self.prev_moves[-1])
                self._undo()
                self.backtracking = False
                if self.debug: print(pairs, 'post-backtracking pairs')
            else:
                #Generate all moves and filter out invalid moves
                pairs = deepcopy(moves)
                if self.debug: self._print_tup(pairs, "{} inital".format(len(self.history))); print()
                
                self._remove_empty_solved(pairs)
                self._remove_opposite(pairs)
                self._remove_incompatibles(pairs)
                self._remove_homog_to_homog(pairs)
                if self.debug: self._print_tup(pairs, "remaining")

            if len(pairs) == 0: 
                #No moves can be performed
                self.backtracking = True
                if self.debug: move_num.append(len(self.history)); print('BACKTRACKING on move', len(self.history))
            else: 
                #There are possible moves that can be performed
                # if self.debug: print('choosing: ', pairs[0])

                self.prev_stacks.append(deepcopy(self.stacks))
                self.prev_pairs.append(deepcopy(pairs))
                # print('current and prev', pairs, '|||', self.prev_pairs[-2])

                if self.print_moves: self.move_and_display(pairs[0])
                else: self.move_pieces(pairs[0])

            loop += 1
            if self.debug: print()
            
        if self._is_solved():
            print("*******SOLVED******")
            self.display_history()
            self._clean_up_moves(); print()
        print('time to solve: {}s'.format(time.time() - t1))
        if self.debug: plt.plot(move_num); plt.ylabel = 'Backtrack move'; plt.show()
        self.display()
        self.display_history()

    def _clean_up_moves(self):
        """
        Streamline the solution by removing redundant moves
        """
        #Remove moves with intermediate steps
        idx = 0
        while idx < len(self.history)-1:
            start = self.history[idx]; end = self.history[idx+1]
            #turn AB BC to AC
            if start[1] == end[0]:
                self.history.pop(idx); self.history.pop(idx) 
                self.history.insert(idx, (start[0], end[1]))
            idx += 1      

        #Replace moves that don't fill stacks efficiently

    def _remove_empty_solved(self, pairs):
        """
        Remove the empty and solved stacks from the current set of moves
        """
        #Check for empty or solved stacks
        solved_empty = []
        for stack in self.stacks:
            if self._is_stack_solved_or_empty(stack):
                solved_empty.append(stack)

        #Eliminate all moves with pieces going from empty or solved pairs
        remove = []
        for pair in pairs:
            for stack in solved_empty:
                if pair[0] == stack: remove.append(pair)
                    
        if len(remove) > 0:
            # if self.debug: self._print_tup(pairs, "pre-emptysolved")
            # if self.debug: self._print_tup(remove, "remove emptysolved")
            self._subtract_lists(pairs, remove)
            # if self.debug: self._print_tup(pairs, "post-emptysolved")

    def _remove_opposite(self, pairs):
        """
        Remove the opposite of the last move to avoid getting stuck in a two-move loop
        """
        if len(self.prev_moves) > 0:
            opp = self.prev_moves[-1][::-1]
            if opp in pairs:
                # self._print_tup(pairs, 'pre-opposite')
                # print('opposite: ' + ''.join(opp))
                pairs.remove(opp)
                # self._print_tup(pairs, 'post-opposite')

    def _remove_incompatibles(self, pairs):
        """
        Remove moves between incompatible stacks
        """
        remove = []
        for pair in pairs:
            if not self.is_pair_compatible(pair):
                remove.append(pair)
        if len(remove) > 0:
            # if self.debug: self._print_tup(pairs, "pre-incompatibles")
            # if self.debug: self._print_tup(remove, "remove incompatibles")
            self._subtract_lists(pairs, remove)
            # if self.debug: self._print_tup(pairs, "post-incompatibles")

    def _remove_homog_to_homog(self, pairs):
        """
        Remove moves coming from a stack with all of the same colors to a stack that's not the same color
        """
        remove = []
        for pair in pairs:
            if self._is_stack_homog(pair[0]) and not self._is_stack_homog(pair[1]):
                remove.append(pair)
        if len(remove) > 0:
            # if self.debug: self._print_tup(pairs, "pre-homogenous")
            # if self.debug: self._print_tup(remove, "remove homogenous")
            self._subtract_lists(pairs, remove)
            # if self.debug: self._print_tup(pairs, "post-homogenous")

    def _print_tup(self, group, msg):
        """
        All elements of a tuple in a String
        """
        elements = ''
        for tup in group:
            elements = elements + ''.join(tup) + ' '
        print("{}: {}".format(msg, elements))

    def _subtract_lists(self, a, b):
        """
        Subtract b from a (a - b)
        """
        for x in b: 
            if x in a: a.remove(x)

    def add_piece(self, stack, piece):
        """
        Add a piece to a stack when creating the game
        """
        self.stacks[stack].append(piece)