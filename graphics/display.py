"""
display
Author: Neil Balaskandarajah
Created on: 05/05/2023
Visualize the game
"""
import time
from model import solver
from graphics import layout_manager
from model import game
import pygame
from graphics import painter
from copy import deepcopy
import thorpy

class Display:
    def __init__(self, game: game.Game=None):
        """Create a new display to view the state of the game

        @param game: Game object to visualize
        """
        self.game = game                # The game to visualize
        self.screen = None              # The screen to draw to
        self.stack_locs = None          # The locations of each stack for drawing
        self.stack_states = None        # The states of each stack for drawing (selected T/F)
        self.clock = None               # PyGame clock for drawing
        self.painter = None             # Painter object for drawing
        self.FPS = 30                   # Screen update rate

        if game:
            self.setup()

    def setup(self):
        """Set up the related PyGame and thorpy assets"""
        self.stack_states = [False] * self.game.get_num_stacks()
        pygame.init()
        pygame.display.set_caption(self.game.name)
        self.screen, self.stack_locs = layout_manager.layout_game_scene(self)
        thorpy.init(self.screen, thorpy.theme_game1)
        self.painter = painter.Painter(self.game.get_num_stacks(), self.game.max_stack_size, self.stack_locs)
        self.clock = pygame.time.Clock()

    def get_stack_from_mouse(self):
        """Get the stack the mouse is currently over

        :return: The index of the stack the mouse is currently over (None if not over a stack)
        """
        # Could change this to using a pygame rect and collisions
        x, y = pygame.mouse.get_pos()
        for i, (stack, loc) in enumerate(zip(self.game.stacks, self.stack_locs)):
            within_x = loc[0] <= x <= loc[0] + layout_manager.HOOP_WIDTH
            within_y = loc[1] >= y >= loc[1] - layout_manager.HOOP_HEIGHT * self.game.max_stack_size
            if within_x and within_y:
                return i
        return None

    def update_stack_states(self, stack_idx, selected):
        """Update the stack states

        :param stack_idx: The index of the stack the mouse is over
        :param selected: If the most recent event was a selection
        """
        if selected and 0 <= stack_idx < self.game.get_num_stacks():
            stack_is_selected = self.stack_states[stack_idx]

            # If the stack that was just clicked on was already selected, unselect it
            if stack_is_selected:
                self.stack_states[stack_idx] = False

            # If the stack that was just selected was not already selected
            else:
                idx_already_selected_stack = self.stack_states.index(True) if True in self.stack_states else None

                # If there isn't another selected stack, select this stack
                if idx_already_selected_stack is None:
                    self.stack_states[stack_idx] = True

                # Else if there is a selected stack, make a move between the two stacks if they are compatible
                else:
                    pair_tup = (idx_already_selected_stack, stack_idx)
                    if self.game.is_pair_compatible(pair_tup):
                        self.game.move_pieces(pair_tup)
                        self.stack_states = [False] * self.game.get_num_stacks()

    def update_stacks(self, stack_idx, event):
        """Update the stacks

        @param stack_idx: The index of the stack the mouse is over
        @param event: The most recent input event
        """
        if stack_idx is None:
            return
        self.update_stack_states(stack_idx, event)

    def play_game(self, quit_on_finish=False):
        """Play the game

        :param quit_on_finish: Whether to quit the application on finish or not
        """
        self.painter.update(self)

        while True:
            self.clock.tick(30)

            mouse_stack = self.get_stack_from_mouse()
            set_cursor(mouse_stack)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    if quit_on_finish:
                        quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.update_stacks(mouse_stack, True)

            self.painter.draw_stacks(self)
            pygame.display.update()

    def solution_stacks(self, moves):
        """Generate the stacks at every step of a solution

        :param moves: Moves of solution
        :return: The stacks at each step of the solution
        """
        game_copy = deepcopy(self.game)
        all_stacks = [deepcopy(game_copy.stacks)]
        for move in moves:
            try:
                game_copy.move_pieces(move)
                all_stacks.append(deepcopy(game_copy.stacks))
            except game.IncompatibleStackError:
                print('Encountered bad move when creating solution stacks')
                break
        return all_stacks

    def play_moves(self, moves, animating=True):
        """Play out a sequence of moves on the screen

        :param moves: Sequence of moves to play
        :param animating: Whether the moves are being animated to the screen or not
        """
        move_idx = 0            # Index of the current move being animated
        selecting = True        # Whether the animator is selecting a stack or not

        self.FPS = 30
        self.painter.update(self)

        # Create all of the stacks
        stacks_from_solution = self.solution_stacks(moves)      # Can change this system to play moves from history

        # Only play as many moves as there are stacks from the solution (cuts off incorrect solutions)
        moves = moves[:len(stacks_from_solution)-1]
        slider, slider_updater = layout_manager.layout_slider(self, len(moves))

        playing = True
        while playing:
            # Draw to the screen
            self.painter.update(self)
            pygame.display.update()
            slider_updater.update(events=pygame.event.get(),
                                  mouse_rel=pygame.mouse.get_rel(),
                                  func_before=self.painter.draw_stacks)
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    print('quitting...')
                    playing = False

                # Move forwards and backwards between the moves
                elif not animating and event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and move_idx > 0:
                        move_idx -= 1
                    elif event.key == pygame.K_RIGHT and move_idx < len(moves):
                        move_idx += 1
                    slider.set_value(move_idx-1)

            if animating:
                # If there are moves to show
                if move_idx < len(moves):
                    if len(moves) > 50:
                        self.FPS = 30
                    elif len(moves) > 20:
                        self.FPS = 10
                    else:
                        self.FPS = 6
                    move = moves[move_idx]

                    # Simulate a mouse click happening on the stack
                    if selecting:
                        self.update_stacks(move[0], pygame.MOUSEBUTTONUP)
                        selecting = False
                    else:
                        self.update_stacks(move[1], pygame.MOUSEBUTTONUP)
                        move_idx += 1
                        selecting = True
                    slider.set_value(move_idx+1)

                # No more moves
                else:
                    print('Stopping animation')
                    self.stack_states = [False] * self.game.get_num_stacks()
                    animating = False

            else:
                self.FPS = 50
                # Show the step in the solution corresponding to the position of the slider
                self.game.stacks = stacks_from_solution[slider.get_value()]

def set_cursor(stack_idx):
    """Assign the cursor based on the position of the mouse

    :param stack_idx: Index of the stack
    """
    if stack_idx is None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
