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
    TILE_SIZE = 250                                     # Dimensions of tile in pixels
    BORDER = int(0.5 * TILE_SIZE)                       # Fraction of cell to use as window border
    PADDING = int(0.1 * TILE_SIZE)                      # Fraction of cell to use as padding between stacks
    HOOP_WIDTH = int(1.0 * TILE_SIZE)                   # Width of cell
    HOOP_HEIGHT = int(0.3 * TILE_SIZE)                  # Height of hoop
    HOOP_CORNER_RAD = int(0.2 * TILE_SIZE)              # Corner radius of hoop

    def __init__(self, game: game.Game):
        """Create a new display to view the state of the game

        @param game: Game object to visualize
        """
        self.game = game

        # Create the PyGame screen
        pygame.display.set_caption(self.game.name)
        self.screen_width = 2*Display.BORDER + (Display.PADDING + Display.TILE_SIZE) * self.game.get_num_stacks()
        self.screen_height = Display.HOOP_HEIGHT * self.game.max_stack_size + 2*Display.BORDER
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Assign locations to each stack
        stack_locs = [Display.BORDER + i * (Display.TILE_SIZE + Display.PADDING) for i in range(self.game.get_num_stacks())]
        game_stacks = [self.game.stacks[self.game.STACK_LABELS[i]] for i in range(self.game.max_stack_size)]
        self.stacks = [(stack, loc) for stack, loc in zip(game_stacks, stack_locs)]
        self.font = pygame.font.SysFont('Consolas', Display.HOOP_HEIGHT)

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
        for i, stack_and_loc in enumerate(self.stacks):
            stack, loc = stack_and_loc
            base_loc = (loc, self.screen_height - Display.BORDER)

            # Draw stacks
            self._draw_stack(stack, base_loc)
            self._draw_stack_base(self.game.STACK_LABELS[i], base_loc)

    def _draw_stack(self, stack, stack_base_loc):
        """Draw a single stack to the screen

        @param stack: Stack to draw
        @param stack_base_loc: Coordinate of the bottom of the stack in fractional cell units
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

                # print('color: {}'.format(color))
                pygame.draw.rect(self.screen, color, rect, border_radius=Display.HOOP_CORNER_RAD)
                pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=Display.HOOP_CORNER_RAD)

    def _draw_stack_base(self, stack_label, stack_base_loc):
        """Draw the base of the stack

        @param stack_label: The stack's label
        @param stack_base_loc: The x-location of the stack
        """
        # Draw base line
        OFFSET = 0.02
        x1 = (stack_base_loc[0] - OFFSET)
        x2 = (stack_base_loc[0] + Display.TILE_SIZE + OFFSET)
        y = self.screen_height - Display.BORDER + 2
        pygame.draw.line(self.screen, (0,0,0), (x1, y), (x2, y), 7)

        # Draw label
        label = self.font.render(stack_label, True, (0,0,0))
        self.screen.blit(label, (x1 + (Display.TILE_SIZE - int(label.get_width())) // 2 , y+5))

    def _get_stack_from_mouse(self, mouse_pos):
        """Get the stack the mouse is currently over

        @param mouse_pos: Position of the mouse in pixels
        @return: The index of the stack
        """
        for i, stack_and_loc in enumerate(self.stacks):
            _, loc = stack_and_loc
            within_x = loc <= mouse_pos[0] <= loc + Display.HOOP_WIDTH
            within_y = Display.BORDER <= mouse_pos[1] <= self.screen_height - Display.BORDER
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

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        # disp.game.solve()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._click_action()

            self.screen.fill((217, 185, 155))
            self._draw_stacks()

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

