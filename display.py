"""
display
Author: Neil Balaskandarajah
Created on: 05/05/2023
Visualize the game
"""
import pygame
import game

class Display:
    def __init__(self, game: game.Game):
        """Create a new display to view the state of the game

        @param game: Game object to visualize
        """
        self.game = game

        self.num_cols = 2 * game.get_num_stacks() + 1
        self.num_rows = game.max_stack_size + 2
        self.tile_size_px = 100
        self.grid = [[0] * self.num_cols for _ in range (self.num_rows)]
        self.screen = self._init_screen()

    def _init_screen(self):
        """Initialize the screen

        @return: PyGame display object
        """
        screen_width = self.num_cols * self.tile_size_px
        screen_height = self.num_rows * self.tile_size_px
        return pygame.display.set_mode((screen_width, screen_height))

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

    def show(self):
        """Start displaying to the screen"""
        print('Number of rows: {}\nNumber of columns: {}'.format(self.num_rows, self.num_cols))
        num_loops = 0
        print(self.game.max_stack_size)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            WHITE = (255, 255, 255)
            BLUE = (0, 0, 255)
            BLACK = (0, 0, 0)
            GRAY = (127, 127, 127)

            self.screen.fill(WHITE)

            stack_base_loc = [-1, self.num_rows - 1]
            for i in range(self.game.get_num_stacks()):
                stack_base_loc[0] += 2
                stack_base_loc[1] = 1
                stack_label = self.game.STACK_LABELS[i]
                stack = self.game.stacks[stack_label]

                for j in range(1, self.game.max_stack_size+1, 1):
                    if j > len(stack):
                        color = GRAY
                    else:
                        color = stack[j - 1]

                    x = stack_base_loc[0]
                    y = stack_base_loc[1] + self.game.max_stack_size - j
                    rect = pygame.Rect(x * self.tile_size_px,
                                       y * self.tile_size_px,
                                       self.tile_size_px,
                                       self.tile_size_px)

                    pygame.draw.rect(self.screen, color, rect)

            self._draw_grid(BLACK)

            # rect = pygame.Rect(1 * self.tile_size_px,
            #                    1 * self.tile_size_px,
            #                    self.tile_size_px,
            #                    self.tile_size_px)
            # pygame.draw.rect(self.screen, BLUE, rect)

            pygame.display.update()
            num_loops += 1

if __name__ == '__main__':
    # Test drawing to the screen
    # Start this in another thread to cut loading time
    pygame.init()

    r = (255, 0, 0)
    g = (0, 255, 0)
    b = (0, 0, 255)

    game = game.Game(3)
    game.add_stacks([
        [r, r, b],
        [r, b],
        [b]
    ])

    # Print out the game
    # Show name of Game object in PyGame window

    disp = Display(game)
    disp.show()

