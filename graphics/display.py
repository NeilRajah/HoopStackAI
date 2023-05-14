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
        pygame.display.set_caption(self.game.name)
        self.screen, self.stack_locs = layout_manager.create_layout(self)
        self.stack_states = [False] * num_stacks
        self.painter = painter.Painter(num_stacks, max_stack_size, self.stack_locs)
        self.clock = pygame.time.Clock()

    def get_stack_from_mouse(self):
        """Get the stack the mouse is currently over

        @return: The index of the stack
        """
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
            # self.stack_states = [False] * self.game.get_num_stacks()

            # If the stack that was just clicked on was selected, unselect it
            if stack_is_selected:
                self.stack_states[stack_idx] = False

            # If the stack that was just clicked was not selected
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

    def run(self):
        """Start displaying to the screen"""
        num_loops = 0

        BACKGROUND = (217, 185, 155)
        # disp.game.solve()

        while True:
            self.clock.tick(Display.FPS)

            mouse_stack = self.get_stack_from_mouse()
            set_cursor(mouse_stack)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.update_stacks(mouse_stack, True)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        self.game.reset()

            self.screen.fill(BACKGROUND)
            self.painter.draw_stacks(self.screen, self.game.stacks, self.stack_states)

            pygame.display.update()
            num_loops += 1

    def play_moves(self, moves, fps):
        BACKGROUND = (217, 185, 155)

        move_idx = 0
        selecting = True
        t1 = time.time()
        while True:
            self.screen.fill(BACKGROUND)
            self.painter.draw_stacks(self.screen, self.game.stacks, self.stack_states)
            pygame.display.update()
            self.clock.tick(2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if move_idx < len(moves):
                print(round(time.time() - t1, 3) * 1000, move_idx, selecting)
                move = moves[move_idx]

                if selecting:
                    self.update_stacks(move[0], pygame.MOUSEBUTTONUP)
                    selecting = False
                else:
                    self.update_stacks(move[1], pygame.MOUSEBUTTONUP)
                    move_idx += 1
                    selecting = True


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

    r = pygame.Color('#ff0000')
    g = pygame.Color('#a1ff0a')
    b = pygame.Color('#0aefff')
    pu = pygame.Color('#580aff')
    pi = pygame.Color('#ff928b')
    org = pygame.Color('#ff8700')
    db = pygame.Color('#147df5')

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
        [b, r, r],
        [b, r],
        [b]
    ])

    pygame.init()
    game.display()
    t1 = time.time()
    disp = Display(game)
    # disp.run()
    s = solver.Solver()
    solution = s.solve(deepcopy(game))

    disp.play_moves(solution, 0.5)