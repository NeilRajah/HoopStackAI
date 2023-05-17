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
    # Constants
    FPS = 50        # Update rate of the screen

    def __init__(self, game: game.Game):
        """Create a new display to view the state of the game

        @param game: Game object to visualize
        """
        self.game = game
        num_stacks = self.game.get_num_stacks()
        max_stack_size = self.game.max_stack_size

        # Create the PyGame screen
        pygame.init()
        pygame.display.set_caption(self.game.name)
        self.screen, self.stack_locs = layout_manager.layout_game_scene(self)
        thorpy.init(self.screen, thorpy.theme_game1)
        self.stack_states = [False] * num_stacks
        self.painter = painter.Painter(num_stacks, max_stack_size, self.stack_locs)
        self.clock = pygame.time.Clock()

    def get_stack_from_mouse(self):
        """Get the stack the mouse is currently over

        @return: The index of the stack
        """
        # Could change this to using a pygame rect and collisions
        x, y = pygame.mouse.get_pos()
        i = -1
        for stack, loc in zip(self.game.stacks, self.stack_locs):
            i += 1
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
                    stack1_idx = idx_already_selected_stack
                    stack2_idx = stack_idx
                    pair_tup = (stack1_idx, stack2_idx)
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

    def play_game(self):
        """Play the game"""
        self.painter.update(self)

        while True:
            self.clock.tick(Display.FPS)

            mouse_stack = self.get_stack_from_mouse()
            set_cursor(mouse_stack)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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
            game_copy.move_pieces(move, bypassing=True)
            all_stacks.append(deepcopy(game_copy.stacks))
        return all_stacks

    def play_moves(self, moves, animating=True):
        """Play out a sequence of moves on the screen

        :param moves: Sequence of moves to play
        :param animating: Whether the moves are being animated to the screen or not
        """
        move_idx = 0            # Index of the current move being animated
        selecting = True        # Whether the animator is selecting a stack or not
        self.FPS = 50

        self.painter.update(self)
        stacks_from_solution = self.solution_stacks(moves)
        slider, slider_updater = layout_manager.layout_slider(self, len(moves))

        while True:
            self.painter.update(self)
            pygame.display.update()
            slider_updater.update(events=pygame.event.get(),
                                  mouse_rel=pygame.mouse.get_rel(),
                                  func_before=self.painter.draw_stacks)
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif not animating and event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move_idx = max(0, move_idx-1)
                    elif event.key == pygame.K_RIGHT:
                        move_idx = min(len(moves), move_idx+1)
                    slider.set_value(move_idx)

            if animating:
                if move_idx >= len(moves):
                    animating = False
                else:
                    self.FPS = 4
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
            else:
                self.FPS = 50
                # Show a snapshot of the solution with the slider
                self.game.stacks = stacks_from_solution[slider.get_value()]

def set_cursor(stack_idx):
    """Assign the cursor based on the position of the mouse

    @param stack_idx: Index of the stack
    """
    if stack_idx is None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

if __name__ == '__main__':
    pygame.init()

    # game = game.Game(3, name='Simple Test')
    # game.add_stacks([
    #     [b, r, r],
    #     [b, r],
    #     [b]
    # ])

    # game = game.Game(5, name='App Level 60')
    # game.add_stacks([
    #     [g, r, b, r, r],
    #     [r, g, pu, b, b],
    #     [b, g],
    #     [g, r, pu, pi, pi],
    #     [g, pi, pi, pu, pu],
    #     [b, pu, pi]
    # ])

    # game = game.Game(5, name='App Level 63')
    # game.add_stacks([
    #     [r, b, b, pi, pi],
    #     [g, g, db],
    #     [b, r, pi, pu, b],
    #     [db, r, pi, pi, g],
    #     [db, g, db, pu, pu],
    #     [pu, db, r, pu, r],
    #     [g, b],
    #     []
    # ])

    # game = game.Game(5, name='App Level 64')
    # game.add_stacks([
    #     [r, pi, b],
    #     [g, pu, g, pu, r],
    #     [r, pi],
    #     [b, r, b, pu, pu],
    #     [pi, r, pi, g, g],
    #     [g, pu, b, b, pi]
    # ])

    game = game.Game(3)
    game.add_stacks([
        ['cyan', 'red', 'red'],
        ['cyan', 'red'],
        ['cyan']
    ])
    print(game.stacks)

    pygame.init()
    game.display()
    t1 = time.time()
    disp = Display(game)
    s = solver.Solver()
    solution = s.solve(deepcopy(game))
    # solution = [(1, 2), (0, 2), (1, 0)]

    # disp.run()
    disp.play_moves(solution, animating=True)