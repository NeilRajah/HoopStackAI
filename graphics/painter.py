"""
painter
Author: Neil Balaskandarajah
Created on: 11/05/2023
Painting to the screen
"""
from graphics import layout_manager
import pygame

BACKGROUND_COLOR = (217, 185, 155)

class Painter:

    def __init__(self, num_stacks, max_stack_size, locs):
        """Create a new Painter to draw to the screen

        :param num_stacks: Total number of stacks
        :param max_stack_size: Maximum number of hoops in a stack
        :param locs: Locations of each stack
        """
        self.num_stacks = num_stacks
        self.max_stack_size = max_stack_size
        self.locs = locs
        self.labels = '12345678'[:num_stacks]
        self.font = pygame.font.SysFont('Consolas', layout_manager.HOOP_HEIGHT)

    def draw_stacks(self, screen, stacks, states):
        """Draw all of the stacks to the screen

        :param screen: Screen to draw to
        :param stacks: The stacks to draw
        :param states: The states of the stacks
        """
        for stack, label, loc, state in zip(stacks, self.labels, self.locs, states):
            self.draw_peg(screen, loc)
            self.draw_stack_base(screen, label, loc)
            self.draw_stack(screen, stack, loc, state)

    def draw_stack(self, screen, stack, loc, state):
        """Draw a single stack to the screen

        @param screen: PyGame screen to draw to
        @param stack: Stack to draw
        @param loc: Coordinate of the bottom of the stack in pixels
        @param state: Whether the stack is selected or not
        """
        # Start from bottom up
        for j in range(1, len(stack) + 1, 1):
            color = stack[j - 1]  # CHANGE THIS TO A DICT

            x = loc[0]
            y = loc[1] - j * layout_manager.HOOP_HEIGHT

            if j == len(stack) and state:
                y -= 3 * layout_manager.BORDER // 4 + (self.num_stacks - len(stack)) * layout_manager.HOOP_HEIGHT

            rect = pygame.Rect(x, y, layout_manager.TILE_SIZE, layout_manager.HOOP_HEIGHT)

            pygame.draw.rect(screen, color, rect, border_radius=layout_manager.HOOP_CORNER_RAD)
            pygame.draw.rect(screen, pygame.color.Color('black'), rect, 3, border_radius=layout_manager.HOOP_CORNER_RAD)

    def draw_stack_base(self, screen, label, loc):
        """Draw the base of the stack to the screen

        :param screen: Screen to draw to
        :param label: Label of the stack
        :param loc: Location of the stack
        """
        # Draw base line
        x1 = (loc[0])
        x2 = (loc[0] + layout_manager.TILE_SIZE)
        y = loc[1]
        pygame.draw.line(screen, (0, 0, 0), (x1, y), (x2, y), 7)

        # Draw label
        label = self.font.render(label, True, (0, 0, 0))
        screen.blit(label, (x1 + (layout_manager.TILE_SIZE - int(label.get_width())) // 2, y + 10))

    def draw_peg(self, screen, loc):
        """Draw the peg of the stack

        :param screen: PyGame screen to draw to
        :param loc: Location of the stack
        """
        x = loc[0] + layout_manager.TILE_SIZE//2
        y1 = loc[1]
        y2 = loc[1] - self.max_stack_size * layout_manager.HOOP_HEIGHT

        pygame.draw.line(screen, (0, 0, 0), (x, y1), (x, y2), layout_manager.PEG_WIDTH)