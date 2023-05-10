"""
game
Author: Neil Balaskandarajah
Created on: 18/06/2020
Game class with all interactions
"""
import time
from itertools import permutations
from copy import deepcopy
import util
import random
import matplotlib.pyplot as plt

class Game:
    def __init__(self, max_stack_size, name='Game'):
        """Create a Game object

        @param max_stack_size: The max size of a stack
        @param name: Name of the game
        """
        self.name = name
        self.max_stack_size = max_stack_size        # Max number of pieces in a stack

        # Attributes for solving
        self.stacks = dict()                # Stacks containing pieces
        self.STACK_LABELS = 'ABCDEFGH'      # Alphabetical labels for each stack
        self.label_idx = 0                  # Index of the current label for adding stacks
        self.history = []                   # History of moves the solver has performed
        self.prev_moves = []                # Previous move
        self.prev_pairs = []                # Moves that could be performed last iteration
        self.prev_stacks = []               # Previous state of all of the stacks for backtracking
        self.is_backtracking = False        # Whether the solver is currently backtracking or not

        # Attributes for debugging
        self.print_moves = False            # Whether to print the moves out to the screen or not
        self.debug = False                  # Whether the solver is in debug mode or not

    def add_stack(self, stack):
        """Add a stack to the game

        @param stack: Stack of hoops ordered top to bottom (ie. index 0 is top, -1 is bottom)
        @return: A debug message containing the name of the stack and its contents
        """
        if self.label_idx > len(self.STACK_LABELS):
            raise Exception('Cannot have more than {} stacks!'.format(len(self.STACK_LABELS)))
        if not isinstance(stack, list):
            raise Exception('Stack must be a Python list!')

        # Reverse stack so stack.pop() removes the top piece
        stack.reverse()
        self.stacks[self.STACK_LABELS[self.label_idx]] = stack
        self.label_idx += 1
        return "Stack {} added: {}".format(self.STACK_LABELS[self.label_idx-1], stack)

    def add_stacks(self, stacks):
        """Add multiple stacks to the game

        @param stacks: List of stacks to add
        """
        for stack in stacks:
            self.add_stack(stack)

    def move_pieces(self, pair_tup):
        """Move a piece from the top of one stack to the other

        @param pair_tup: The pair of stacks in (from, to) format (ie. move_pieces (x,y) moves from stack x to stack y)
        @return: A debug message saying which piece was moved between which stacks
        """
        if not self.is_pair_compatible(pair_tup):
            msg = "Stacks {} and {} are not compatible!".format(pair_tup[0], pair_tup[1])
            msg = msg + "\n{} | {}".format(self.stacks[pair_tup[0]], self.stacks[pair_tup[1]])
            raise Exception(msg)

        # Move from top of the first stack to the second
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]
        b.append(a.pop())

        # Save to history
        self.history.append(pair_tup)
        self.prev_moves.append(pair_tup)
        return "Moved {} from {} to {}".format(b[-1], pair_tup[0], pair_tup[1])

    def is_pair_compatible(self, pair_tup):
        """Check if a pair of stacks are compatible

        @param pair_tup: The pair of stacks identified by their stack label
        @return:
        """
        a = self.stacks[pair_tup[0]]
        b = self.stacks[pair_tup[1]]

        # Can't move from an empty stack
        if len(a) == 0:
            return False

        # Can't move to a full stack
        if len(b) == self.max_stack_size:
            return False

        # Can move to empty stack
        if len(b) == 0:
            return True

        # Can move if top pieces are same
        if a[-1] == b[-1]:
            return True
        return False

    def display(self):
        """Print the game out to the console"""
        # print(self.stacks)
        s = ''
        for stack in self.stacks:
            if len(self.stacks[stack]) > 0:
                s = self.stacks[stack][0]
                break
        blank = '_' * len(s) + ' '
        spacer = '-' * (7 * len(self.stacks))
        for i in reversed(range(self.max_stack_size)):
            row = ""
            for lbl in self.stacks:
                if i > len(self.stacks[lbl])-1:
                    row = row + blank
                else:
                    row = row + "{} ".format(self.stacks[lbl][i])
            print(row)
        print(spacer)

    def display_history(self):
        """Print the move history to the console"""
        util.print_tup(self.history, len(self.history))

    def move_and_display(self, pair_tup):
        """Move a piece and print game information to the console

        @param pair_tup: The pair of stacks identified by their stack label
        """
        self.move_pieces(pair_tup)
        self.display()
        self.display_history()

    def get_num_stacks(self):
        """Get the number of stacks in the game

        @return: Total number of stacks
        """
        return self.label_idx

    def _is_solved(self):
        """Return if the game is solved or not

        @return: True if all of the stacks are solved or empty, else false
        """
        for stack in self.stacks:
            if not self._is_stack_solved_or_empty(stack):
                return False
        return True

    def _is_stack_solved_or_empty(self, lbl):
        """Return if the stack is solved, empty or neither

        @param lbl: Label of the stack
        @return: True if it is solved (all of same color and of max length) or empty (no hoops)
        """
        stack = self.stacks[lbl]
        stack_is_empty = len(stack) == 0
        stack_is_solved = self._is_stack_homog(lbl) and len(stack) == self.max_stack_size
        return stack_is_empty or stack_is_solved

    def _is_stack_homog(self, lbl):
        """Return if a stack is all the same color or not (False if empty)

        @param lbl: Label of the stack
        @return: Whether there is only one unique color present in the stack
        """
        return len(set(self.stacks[lbl])) == 1

    def _undo(self):
        """Undo the last move done (for backtracking)"""
        if len(self.history) > 0:
            pair = self.history.pop()[::-1]  # opposite of last move done
            a = self.stacks[pair[0]]
            b = self.stacks[pair[1]]
            b.append(a.pop())
        if len(self.prev_moves) > 0: self.prev_moves.pop()

    def solve(self, print_moves=False, debug=False):
        """Solve the puzzle

        @param print_moves: Whether to print the moves out or ont
        @param debug: Whether to display debug messages or not
        @return:
        """
        self.print_moves = print_moves
        self.debug = debug
        print("*******START*******")

        #Start the solution by calculating all possible moves
        moves = list(permutations(self.stacks, 2)) #change to local?
        self.prev_pairs.append(deepcopy(moves))
        move_num = []
        t1 = time.time()

        log_file = 'log.txt'
        open(log_file, 'w').close()
        file = open(log_file, 'a')
        file.write('\n')
        
        # For preventing infinite loops
        num_loops = 10000
        loop = 0  
        while not self._is_solved():
            if loop >= num_loops: print("\nToo many loops"); break

            if self.is_backtracking:
                #Undo the last move, reset the pairs to the last set and move forward
                if self.debug: util.print_tup(pairs, 'pre-backtracking pairs')
                pairs = self.prev_pairs.pop()
                if len(self.prev_moves) > 0 and self.prev_moves[-1] in pairs:
                    pairs.remove(self.prev_moves[-1])
                self._undo()
                self.is_backtracking = False
                if self.debug: print(pairs, 'post-backtracking pairs')
            else:
                #Generate all moves and filter out invalid moves
                pairs = deepcopy(moves)
                if self.debug: util.print_tup(pairs, "{} inital".format(len(self.history))); print()

                self._remove_empty_solved(pairs)
                self._remove_opposite(pairs)
                self._remove_incompatibles(pairs)
                self._remove_homog_to_homog(pairs)
                if self.debug: util.print_tup(pairs, "remaining")

            if len(pairs) == 0:
                #No moves can be performed
                self.is_backtracking = True
                if self.debug: move_num.append(len(self.history)); print('BACKTRACKING on move', len(self.history))
            else:
                #There are possible moves that can be performed
                # if self.debug: print('choosing: ', pairs[0])

                self.prev_stacks.append(deepcopy(self.stacks))
                self.prev_pairs.append(deepcopy(pairs))

                #Choose first move in remaining set
                chosen_move = pairs[0]
                # random.seed(time.time())
                # chosen_move = pairs[int(random.random() * len(pairs))]
                # print('{} options, chose {}'.format(len(pairs), index))
                pairs_str = ''
                for pair in pairs:
                    pairs_str = pairs_str + ''.join(pair) + ' '

                chosen_move = self._fill_efficiently(chosen_move)  #Optimize the move if its filling a stack up
                file.write('{:2d}: {} - {}\n'.format(loop, ''.join(chosen_move), pairs_str))

                if self.print_moves:
                    self.move_and_display(chosen_move)
                else:
                    self.move_pieces(chosen_move)

            loop += 1
            if self.debug: print()

        file.close()
        if self._is_solved():
            print("*******SOLVED******")
            self.display_history()
            self._clean_up_moves()
            print()
        print('time to solve: {}s'.format(round(time.time() - t1, 3)))
        # if self.debug: plt.plot(move_num); plt.ylabel = 'Backtrack move'; plt.show()
        self.display()
        self.display_history()

    def _fill_efficiently(self, move):
        """Fill stacks efficiently by moving from small homogenous stacks to large ones instead of vice versa

        @param move: Move of (from, to) stack labels
        @return: Return the move that moves the hoop from the smaller stack to the larger one
        """
        if self._is_stack_homog(move[0]) and self._is_stack_homog(move[1]):
            if len(self.stacks[move[0]]) > len(self.stacks[move[1]]):
                return move[::-1]  #Flip the move if going from large homog to small homog
        return move

    def _clean_up_moves(self):
        """Streamline the solution by removing redundant moves"""
        # Remove moves with intermediate steps
        idx = 0
        while idx < len(self.history)-1:
            start = self.history[idx]; end = self.history[idx+1]
            # turn AB BC to AC
            if start[1] == end[0]:
                self.history.pop(idx); self.history.pop(idx)
                self.history.insert(idx, (start[0], end[1]))
            idx += 1

            # Replace moves that don't fill stacks efficiently

    def _remove_empty_solved(self, pairs):
        """Remove the empty and solved stacks from the current set of moves

        @param pairs: Pairs of moves in (from, to) stack label format
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
                if pair[0] == stack:
                    remove.append(pair)

        if len(remove) > 0:
            # if self.debug: self._print_tup(pairs, "pre-emptysolved")
            # if self.debug: self._print_tup(remove, "remove emptysolved")
            util.subtract_lists(pairs, remove)
            # if self.debug: self._print_tup(pairs, "post-emptysolved")

    def _remove_opposite(self, pairs):
        """Remove the opposite of the last move to avoid getting stuck in a two-move loop

        @param pairs: Pairs of moves in (from, to) stack label format
        """
        if len(self.prev_moves) > 0:
            opp = self.prev_moves[-1][::-1]
            if opp in pairs:
                # self._print_tup(pairs, 'pre-opposite')
                # print('opposite: ' + ''.join(opp))
                pairs.remove(opp)
                # self._print_tup(pairs, 'post-opposite')

    def _remove_incompatibles(self, pairs):
        """Remove moves between incompatible stacks

        @param pairs: Pairs of moves in (from, to) stack label format
        """
        remove = []
        for pair in pairs:
            if not self.is_pair_compatible(pair):
                remove.append(pair)
        if len(remove) > 0:
            # if self.debug: self._print_tup(pairs, "pre-incompatibles")
            # if self.debug: self._print_tup(remove, "remove incompatibles")
            util.subtract_lists(pairs, remove)
            # if self.debug: self._print_tup(pairs, "post-incompatibles")

    def _remove_homog_to_homog(self, pairs):
        """Remove moves coming from a stack with all of the same colors to a stack that's not the same color

        @param pairs: Pairs of moves in (from, to) stack label format
        """
        remove = []
        for pair in pairs:
            if self._is_stack_homog(pair[0]) and not self._is_stack_homog(pair[1]):
                remove.append(pair)
        if len(remove) > 0:
            # if self.debug: self._print_tup(pairs, "pre-homogenous")
            # if self.debug: self._print_tup(remove, "remove homogenous")
            util.subtract_lists(pairs, remove)
            # if self.debug: self._print_tup(pairs, "post-homogenous")

    def add_piece(self, stack, piece):
        """Add a piece to a stack when creating the game

        @param stack: Stack of pieces
        @param piece: Piece to add to stack
        """
        self.stacks[stack].append(piece)