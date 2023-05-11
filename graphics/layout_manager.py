"""
layout_manager
Author: Neil Balaskandarajah
Created on: 10/05/2023
Manage the layout
"""
import pygame
from display import Display

def create_layout(disp):
    """Create the layout of the window

    @param disp: Display object
    @return: The screen and the stack locations
    """
    num_stacks = disp.game.get_num_stacks()
    screen_width = 2 * Display.BORDER - Display.PADDING
    screen_height = 2 * Display.BORDER

    # Heights for the two rows
    ROW_ONE_HEIGHT = Display.BORDER + Display.HOOP_HEIGHT * disp.game.max_stack_size
    ROW_TWO_HEIGHT = 2 * (Display.BORDER + Display.HOOP_HEIGHT * disp.game.max_stack_size) + Display.BORDER
    stack_locs = []

    # Single-row
    if num_stacks <= 4:
        screen_width += (Display.PADDING + Display.TILE_SIZE) * num_stacks
        screen_height += Display.HOOP_HEIGHT * disp.game.max_stack_size

        for i in range(num_stacks):
            x = Display.BORDER + i * (Display.TILE_SIZE + Display.PADDING)
            stack_locs.append((x, ROW_ONE_HEIGHT))

    # Double-row
    else:
        if num_stacks in (5, 6):
            screen_width += (Display.PADDING + Display.TILE_SIZE) * 3

            for i in range(6):
                if i < 3:
                    x = Display.BORDER + i * (Display.TILE_SIZE + Display.PADDING)
                    y = ROW_ONE_HEIGHT
                else:
                    r = i-3
                    if num_stacks == 5:
                        x = Display.BORDER + int((r + 0.5) * (Display.TILE_SIZE + Display.PADDING))
                    else:
                        x = Display.BORDER + r * (Display.TILE_SIZE + Display.PADDING)
                    y = ROW_TWO_HEIGHT

                stack_locs.append((x, y))

        elif num_stacks in (7, 8):
            screen_width += (Display.PADDING + Display.TILE_SIZE) * 4

            for i in range(4):
                x = Display.BORDER + i * (Display.TILE_SIZE + Display.PADDING)
                stack_locs.append((x, ROW_ONE_HEIGHT))

            for i in range(4, 8, 1):
                r = i - 4
                if num_stacks == 7:
                    x = Display.BORDER + int((r + 0.5) * (Display.TILE_SIZE + Display.PADDING))
                else:
                    x = Display.BORDER + r * (Display.TILE_SIZE + Display.PADDING)
                stack_locs.append((x, ROW_TWO_HEIGHT))

        screen_height += 2 * (Display.HOOP_HEIGHT * disp.game.max_stack_size) + 2*Display.BORDER

    screen = pygame.display.set_mode((screen_width, screen_height))
    return screen, stack_locs
