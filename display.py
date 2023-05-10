"""
display
Author: Neil Balaskandarajah
Created on: 05/05/2023
Visualize the game
"""
import pygame
import game
import threading

class Display:
    TILE_SIZE = 100                     # Dimensions of tile in pixels
    BORDER = int(0.5 * TILE_SIZE)                       # Fraction of cell to use as window border
    PADDING = int(0.1 * TILE_SIZE)                       # Fraction of cell to use as padding between stacks
    HOOP_WIDTH = int(1.0 * TILE_SIZE)                   # Width of cell
    HOOP_HEIGHT = int(0.3 * TILE_SIZE)                 # Height of hoop
    LABEL_HEIGHT = int(0.8 * TILE_SIZE)                  # Height of the label row

    def __init__(self, game: game.Game):
        """Create a new display to view the state of the game

        @param game: Game object to visualize
        """
        self.game = game

        self.num_cols = game.get_num_stacks()
        self.num_rows = game.max_stack_size

        pygame.display.set_caption(self.game.name)
        self.screen_width = 2*Display.BORDER + (Display.PADDING + Display.TILE_SIZE) * self.num_cols
        self.screen_height = 2*Display.BORDER + (Display.PADDING + Display.TILE_SIZE) * self.num_rows + Display.LABEL_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.stack_locs = [Display.BORDER + i * (Display.TILE_SIZE + Display.PADDING) for i in range(self.num_cols)]

    def _draw_grid(self, border_color):
        """Draw the grid to the display

        @param border_color: Color to draw the border lines
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                rect = pygame.Rect(col * Display.TILE_SIZE,
                                   row * Display.TILE_SIZE,
                                   Display.TILE_SIZE,
                                   Display.TILE_SIZE)
                pygame.draw.rect(self.screen, border_color, rect, 1)

    def _draw_stacks(self):
        """Draw all of the stacks to the screen"""
        for i, stack_loc in enumerate(self.stack_locs):
            stack_label = self.game.STACK_LABELS[i]
            stack = self.game.stacks[stack_label]
            base_loc = (stack_loc, self.screen_height - Display.LABEL_HEIGHT)

            # Draw stacks
            self._draw_stack(stack, base_loc)
            self._draw_stack_base(stack_label, base_loc)

    def _draw_stack(self, stack, stack_base_loc):
        """Draw a single stack to the screen

        @param stack: Stack to draw
        @param stack_base_loc: Coordinate of the bottom of the stack in fractional cell units
        """
        GRAY = (100, 100, 100)
        BLACK = (0, 0, 0)

        # Start from bottom up
        for j in range(1, self.game.max_stack_size + 1, 1):
            if j <= len(stack):
                color = stack[j - 1]

                x = stack_base_loc[0]
                y = stack_base_loc[1] + (self.game.max_stack_size - j) * Display.HOOP_HEIGHT
                rect = pygame.Rect(x * Display.TILE_SIZE,
                                   y * Display.TILE_SIZE,
                                   Display.TILE_SIZE,
                                   Display.TILE_SIZE * Display.HOOP_HEIGHT)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)

    def _draw_stack_base(self, stack_label, stack_base_loc):
        OFFSET = 0.02
        x1 = (stack_base_loc[0] - OFFSET) * Display.TILE_SIZE
        x2 = (stack_base_loc[0] + Display.TILE_SIZE + OFFSET) * Display.TILE_SIZE
        y = Display.LABEL_HEIGHT + self.game.max_stack_size * Display.TILE_SIZE
        pygame.draw.line(self.screen, (0,0,0), (x1, y), (x2, y), 10)

    def _get_stack_from_mouse(self, mouse_pos):
        """Get the stack the mouse is currently over

        @param mouse_pos: Position of the mouse in pixels
        @return: The grid coordinate of the cell
        """
        x_mouse, y_mouse = mouse_pos
        CELL_SIDE = Display.TILE_SIZE * Display.TILE_SIZE

        for i, stack_loc in enumerate(self.stack_locs):
            stack_label = self.game.STACK_LABELS[i]
            stack = self.game.stacks[stack_label]

            x_min = stack_loc * Display.TILE_SIZE
            x_max = x_min + CELL_SIDE
            # y_min = Display.BASE_Y * Display.TILE_SIZE
            # y_max = y_min + CELL_SIDE * len(stack)
            y_max = Display.BORDER
            y_min = Display.LABEL_HEIGHT

            # print('{}: ({} | {}), ({} | {})'.format(i, x_min, x_max, y_min, y_max))
            within_x = x_min <= x_mouse <= x_max
            within_y = y_min <= y_mouse <= y_max
            if within_x and within_y:
                return i
        return None

    def _click_action(self):
        # print(pygame.mouse.get_pos())
        print(self._get_stack_from_mouse(pygame.mouse.get_pos()))

    def run(self):
        """Start displaying to the screen"""
        # print('Number of rows: {}\nNumber of columns: {}'.format(self.num_rows, self.num_cols))
        num_loops = 0
        print(self.game.max_stack_size)

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        disp.game.solve()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._click_action()

            self.screen.fill(WHITE)

            self._draw_stacks()

            # self._draw_grid(BLACK)

            pygame.display.update()
            num_loops += 1

if __name__ == '__main__':
    # Test drawing to the screen
    # Start this in another thread to cut loading time
    # Show name of Game object in PyGame window
    pygame.init()

    r = (255, 79, 0)
    g = (226, 255, 0)
    b = (0, 252, 255)

    game = game.Game(3)
    game.add_stacks([
        [b, r, r],
        [b, r],
        [b]
    ])

    # Print out the game
    # Show name of Game object in PyGame window

    disp = Display(game)
    # threading.Thread(target=disp.run).start()
    disp.run()

