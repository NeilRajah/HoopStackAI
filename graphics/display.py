"""
display
Author: Neil Balaskandarajah
Created on: 05/05/2023
Visualize the game
"""
import pygame
from model import game

class Display:
    # Constants
    TILE_SIZE = 150                                     # Dimensions of tile in pixels
    BORDER = int(0.5 * TILE_SIZE)                       # Fraction of cell to use as window border
    PADDING = int(0.1 * TILE_SIZE)                      # Fraction of cell to use as padding between stacks
    HOOP_WIDTH = int(1.0 * TILE_SIZE)                   # Width of cell
    HOOP_HEIGHT = int(0.3 * TILE_SIZE)                  # Height of hoop
    HOOP_CORNER_RAD = HOOP_HEIGHT//2                    # Corner radius of hoop
    FPS = 50                                            # Update rate of the screen

    def __init__(self, game: game.Game):
        """Create a new display to view the state of the game

        @param game: Game object to visualize
        """
        self.game = game
        # self.is_small_layout = self.game.get_num_stacks() <= 10
        self.is_small_layout = True

        # Create the PyGame screen
        pygame.display.set_caption(self.game.name)

        self.screen = self._init_screen()

        # Assign locations to each stack
        # self.stacks = self._update_stacks()
        self.stack_locs = self._assign_stack_locs()

        self._font = pygame.font.SysFont('Consolas', Display.HOOP_HEIGHT)       # Label font

    def _init_screen(self):
        """Determine the size of the screen

        @return: The PyGame screen
        """
        if self.is_small_layout:
            screen_width = 2*Display.BORDER + (Display.PADDING + Display.TILE_SIZE) * self.game.get_num_stacks() - Display.PADDING
            screen_height = Display.HOOP_HEIGHT * self.game.max_stack_size + 2 * Display.BORDER
        else:
            screen_width = 2*Display.BORDER + (Display.PADDING + Display.TILE_SIZE)*4 - Display.PADDING
            screen_height = Display.HOOP_HEIGHT * self.game.max_stack_size * 2 + 3*Display.BORDER

        return pygame.display.set_mode((screen_width, screen_height))

    def _assign_stack_locs(self):
        """Assign the locations for each stack based on the layout

        @return: The locations for each stack
        """
        if self.is_small_layout:
            return [(Display.BORDER + i * (Display.TILE_SIZE + Display.PADDING),
                           self.screen.get_height() - Display.BORDER)
                          for i in range(self.game.get_num_stacks())]
        else:
            # Stub
            pass

    def _draw_stacks(self):
        """Draw all of the stacks to the screen"""
        for stack, loc, label in zip(self.game.get_stack_list(), self.stack_locs, self.game.get_label_list()):
            self._draw_stack(stack, loc)
            self._draw_stack_base(label, loc)

    def _draw_stack(self, stack, stack_base_loc):
        """Draw a single stack to the screen

        @param stack: Stack to draw
        @param stack_base_loc: Coordinate of the bottom of the stack in pixels
        """
        BLACK = (0, 0, 0)

        # Start from bottom up
        for j in range(1, self.game.max_stack_size + 1, 1):
            if j <= len(stack):
                color = stack[j - 1]                                                        # Change this to a dict

                x = stack_base_loc[0]
                y = stack_base_loc[1] - j * Display.HOOP_HEIGHT
                rect = pygame.Rect(x,
                                   y,
                                   Display.TILE_SIZE,
                                   Display.HOOP_HEIGHT)

                pygame.draw.rect(self.screen, color, rect, border_radius=Display.HOOP_CORNER_RAD)
                pygame.draw.rect(self.screen, BLACK, rect, 3, border_radius=Display.HOOP_CORNER_RAD)

    def _draw_stack_base(self, stack_label, stack_base_loc):
        """Draw the base of the stack

        @param stack_label: The stack's label
        @param stack_base_loc: The x-location of the stack
        """
        # Draw base line
        x1 = (stack_base_loc[0])
        x2 = (stack_base_loc[0] + Display.TILE_SIZE)
        y = self.screen.get_height() - Display.BORDER + 2
        pygame.draw.line(self.screen, (0,0,0), (x1, y), (x2, y), 7)

        # Draw label
        label = self._font.render(stack_label, True, (0, 0, 0))
        self.screen.blit(label, (x1 + (Display.TILE_SIZE - int(label.get_width())) // 2 , y+10))

    def _get_stack_from_mouse(self):
        """Get the stack the mouse is currently over

        @return: The index of the stack
        """
        x, y = pygame.mouse.get_pos()
        for stack, loc in zip(self.game.get_stack_list(), self.stack_locs):
            within_x = loc[0] <= x <= loc[0] + Display.HOOP_WIDTH
            within_y = loc[1] >= y >= loc[1] - Display.HOOP_HEIGHT * len(stack)
            if within_x and within_y:
                return loc

        return None

    def _set_cursor(self):
        """Assign the cursor based on the position of the mouse"""
        if self._get_stack_from_mouse() is None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def run(self):
        """Start displaying to the screen"""
        # print('Number of rows: {}\nNumber of columns: {}'.format(self.num_rows, self.num_cols))
        num_loops = 0

        BACKGROUND = (217, 185, 155)
        # disp.game.solve()
        clock = pygame.time.Clock()

        while True:
            clock.tick(Display.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self._set_cursor()

            self.screen.fill(BACKGROUND)
            self._draw_stacks()

            pygame.display.update()
            num_loops += 1

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

    game = game.Game(5, name='App Level 63')
    game.add_stacks([
        [r, b, b, pi, pi],
        [g, g, db],
        [b, r, pi, pu, b],
        [db, r, pi, pi, g],
        [db, g, db, pu, pu],
        [pu, db, r, pu, r],
        [g, b]
    ])

    disp = Display(game)
    # game.solve()
    disp.run()