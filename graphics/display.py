"""
display
Author: Neil Balaskandarajah
Created on: 05/05/2023
Visualize the game
"""
import layout_manager
from model import game
import pygame

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

        # Create the PyGame screen
        pygame.display.set_caption(self.game.name)

        # self.screen = self._init_screen()

        # Assign locations to each stack
        # self.stacks = self._update_stacks()
        # self.stack_locs = self._assign_stack_locs()

        self.screen, self.stack_locs = layout_manager.create_layout(self)
        self.stack_states = [False] * self.game.get_num_stacks()
        self.stack_targets = [(0,0)] * self.game.get_num_stacks()

        self._font = pygame.font.SysFont('Consolas', Display.HOOP_HEIGHT)       # Label font

    def draw_stacks(self):
        """Draw all of the stacks to the screen"""
        for i in range(self.game.get_num_stacks()):
            stack = self.game.get_stack_list()[i]
            label = self.game.get_label_list()[i]
            loc = self.stack_locs[i]
            state = self.stack_states[i]

            self.draw_stack(stack, loc, state)
            self.draw_stack_base(label, loc)

    def draw_stack(self, stack, stack_loc, stack_is_selected):
        """Draw a single stack to the screen

        @param stack: Stack to draw
        @param stack_loc: Coordinate of the bottom of the stack in pixels
        @param stack_is_selected: Whether the stack is selected or not
        """
        BLACK = (0, 0, 0)

        # Start from bottom up
        for j in range(1, len(stack) + 1, 1):
            color = stack[j - 1]        # Change this to a dict

            x = stack_loc[0]
            y = stack_loc[1] - j * Display.HOOP_HEIGHT

            if j == len(stack) and stack_is_selected:
                y -= 3 * Display.BORDER // 4  + (self.game.max_stack_size - len(stack)) * Display.HOOP_HEIGHT

            rect = pygame.Rect(x, y, Display.TILE_SIZE, Display.HOOP_HEIGHT)

            pygame.draw.rect(self.screen, color, rect, border_radius=Display.HOOP_CORNER_RAD)
            pygame.draw.rect(self.screen, BLACK, rect, 3, border_radius=Display.HOOP_CORNER_RAD)

    def draw_stack_base(self, stack_label, stack_base_loc):
        """Draw the base of the stack

        @param stack_label: The stack's label
        @param stack_base_loc: The x-location of the stack
        """
        # Draw base line
        x1 = (stack_base_loc[0])
        x2 = (stack_base_loc[0] + Display.TILE_SIZE)
        y = stack_base_loc[1]
        pygame.draw.line(self.screen, (0,0,0), (x1, y), (x2, y), 7)

        # Draw label
        label = self._font.render(stack_label, True, (0, 0, 0))
        self.screen.blit(label, (x1 + (Display.TILE_SIZE - int(label.get_width())) // 2 , y+10))

    def get_stack_from_mouse(self):
        """Get the stack the mouse is currently over

        @return: The index of the stack
        """
        x, y = pygame.mouse.get_pos()
        i = -1
        for stack, loc in zip(self.game.get_stack_list(), self.stack_locs):
            i += 1
            within_x = loc[0] <= x <= loc[0] + Display.HOOP_WIDTH
            within_y = loc[1] >= y >= loc[1] - Display.HOOP_HEIGHT * self.game.max_stack_size
            if within_x and within_y:
                return i

        return None

    def update_stack_states(self, stack_idx, event):
        """Update the states

        @param stack_idx: The indexs of the stack the mouse is over
        @param event: The most recent input event
        """
        if stack_idx is None:
            return

        if event.type == pygame.MOUSEBUTTONUP:
            old_state = self.stack_states[stack_idx]
            self.stack_states = [False] * self.game.get_num_stacks()

            # Toggle state
            self.stack_states[stack_idx] = not old_state

    def run(self):
        """Start displaying to the screen"""
        # print('Number of rows: {}\nNumber of columns: {}'.format(self.num_rows, self.num_cols))
        num_loops = 0

        BACKGROUND = (217, 185, 155)
        # disp.game.solve()
        clock = pygame.time.Clock()

        while True:
            clock.tick(Display.FPS)

            mouse_stack = self.get_stack_from_mouse()
            set_cursor(mouse_stack)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.update_stack_states(mouse_stack, event)

            self.screen.fill(BACKGROUND)
            self.draw_stacks()

            pygame.display.update()
            num_loops += 1

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

    game = game.Game(5, name='App Level 64')
    game.add_stacks([
        [r, pi, b],
        [g, pu, g, pu, r],
        [r, pi],
        [b, r, b, pu, pu],
        [pi, r, pi, g, g],
        [g, pu, b, b, pi]
    ])

    disp = Display(game)
    game.solve()
    disp.run()