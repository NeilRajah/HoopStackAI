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
    BORDER = 0.5                # Fraction of cell to use as window border
    PADDING = 0.1               # Fraction of cell to use as padding between stacks
    CELL_WIDTH = 1.0            # Width of cell
    LABEL_HEIGHT = 0.8          # Height of the label row

    def __init__(self, game: game.Game):
        """Create a new display to view the state of the game

        @param game: Game object to visualize
        """
        self.game = game

        self.num_cols = game.get_num_stacks()
        self.num_rows = game.max_stack_size
        self.tile_size_px = 100
        self.grid = [[0] * self.num_cols for _ in range (self.num_rows)]
        self.screen = self._init_screen()

    def _init_screen(self):
        """Initialize the screen

        @return: PyGame display object
        """
        pygame.display.set_caption(self.game.name)
        screen_width = (2*Display.BORDER + (1 + Display.PADDING) * self.num_cols) * self.tile_size_px
        screen_height = (2*Display.BORDER + (1 + Display.PADDING) * self.num_rows + Display.LABEL_HEIGHT) * self.tile_size_px
        return pygame.display.set_mode((int(screen_width), int(screen_height)))

    def _draw_grid(self, border_color):
        """Draw the grid to the display

        @param border_color: Color to draw the border lines
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                rect = pygame.Rect(col * self.tile_size_px,
                                   row * self.tile_size_px,
                                   self.tile_size_px,
                                   self.tile_size_px)
                pygame.draw.rect(self.screen, border_color, rect, 1)

    def _draw_stacks(self):
        """Draw all of the stacks to the screen"""
        stack_base_loc = [-Display.BORDER, 0]       # Bottom of the first stack

        for i in range(self.game.get_num_stacks()):
            stack_base_loc[0] += Display.CELL_WIDTH + Display.PADDING
            stack_base_loc[1] = Display.BORDER + Display.CELL_WIDTH
            stack_label = self.game.STACK_LABELS[i]
            stack = self.game.stacks[stack_label]

            # Draw stacks
            self._draw_stack(stack, stack_base_loc)
            self._draw_stack_label(stack_label, stack_base_loc) ###

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
                y = stack_base_loc[1] + self.game.max_stack_size - j
                rect = pygame.Rect(x * self.tile_size_px,
                                   y * self.tile_size_px,
                                   self.tile_size_px,
                                   self.tile_size_px)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)

    def _draw_stack_label(self, stack_label, stack_base_loc):
        pass

    def _get_cell_from_mouse(self, mouse_pos):
        """Get the cell corresponding to the mouse location

        @param mouse_pos: Position of the mouse in pixels
        @return: The grid coordinate of the cell
        """
        return mouse_pos[0] // self.tile_size_px, mouse_pos[1] // self.tile_size_px

    def _click_action(self):
        print(self._get_cell_from_mouse(pygame.mouse.get_pos()))

    def run(self):
        """Start displaying to the screen"""
        # print('Number of rows: {}\nNumber of columns: {}'.format(self.num_rows, self.num_cols))
        num_loops = 0
        print(self.game.max_stack_size)

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

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
        [r, r, b],
        [r, b],
        [b],
        [g, g, g]
    ])

    # Print out the game
    # Show name of Game object in PyGame window

    disp = Display(game)
    # threading.Thread(target=disp.run).start()
    disp.run()

