"""
layout_manager
Author: Neil Balaskandarajah
Created on: 10/05/2023
Manage the layout
"""
import pygame
import display
import thorpy

# Game scene constants
TILE_SIZE = 150                             # Dimensions of tile in pixels
BORDER = int(0.5 * TILE_SIZE)               # Fraction of cell to use as window border
PADDING = int(0.1 * TILE_SIZE)              # Fraction of cell to use as padding between stacks
HOOP_WIDTH = int(1.0 * TILE_SIZE)           # Width of cell
HOOP_HEIGHT = int(0.3 * TILE_SIZE)          # Height of hoop
HOOP_CORNER_RAD = HOOP_HEIGHT//2            # Corner radius of hoop
PEG_WIDTH = int(0.12 * HOOP_WIDTH)          # Width of the peg

# Slider constants
SLIDER_HEIGHT = int(0.5 * TILE_SIZE)        # Height of the slider

def layout_game_scene(disp):
    """Create the layout of the game window

    @param disp: object
    @return: The screen and the stack locations
    """
    num_stacks = disp.game.get_num_stacks()
    screen_width = 2 * BORDER - PADDING
    screen_height = 2 * BORDER

    # Heights for the two rows
    ROW_ONE_HEIGHT = BORDER + HOOP_HEIGHT * disp.game.max_stack_size
    ROW_TWO_HEIGHT = 2 * (BORDER + HOOP_HEIGHT * disp.game.max_stack_size) + BORDER
    stack_locs = []

    # Single-row
    if num_stacks <= 4:
        screen_width += (PADDING + TILE_SIZE) * num_stacks
        screen_height += HOOP_HEIGHT * disp.game.max_stack_size

        for i in range(num_stacks):
            x = BORDER + i * (TILE_SIZE + PADDING)
            stack_locs.append((x, ROW_ONE_HEIGHT))

    # Double-row
    else:
        if num_stacks in (5, 6):
            screen_width += (PADDING + TILE_SIZE) * 3

            for i in range(6):
                if i < 3:
                    x = BORDER + i * (TILE_SIZE + PADDING)
                    y = ROW_ONE_HEIGHT
                else:
                    r = i-3
                    if num_stacks == 5:
                        x = BORDER + int((r + 0.5) * (TILE_SIZE + PADDING))
                    else:
                        x = BORDER + r * (TILE_SIZE + PADDING)
                    y = ROW_TWO_HEIGHT

                stack_locs.append((x, y))

        elif num_stacks in (7, 8):
            screen_width += (PADDING + TILE_SIZE) * 4

            for i in range(4):
                x = BORDER + i * (TILE_SIZE + PADDING)
                stack_locs.append((x, ROW_ONE_HEIGHT))

            for i in range(4, 8, 1):
                r = i - 4
                if num_stacks == 7:
                    x = BORDER + int((r + 0.5) * (TILE_SIZE + PADDING))
                else:
                    x = BORDER + r * (TILE_SIZE + PADDING)
                stack_locs.append((x, ROW_TWO_HEIGHT))

        screen_height += 2 * (HOOP_HEIGHT * disp.game.max_stack_size) + 2*BORDER

    screen = pygame.display.set_mode((screen_width, screen_height))
    return screen, stack_locs

def layout_slider(disp: display.Display, num_moves):
    # Create the slider
    scene_width = disp.screen.get_width()
    scene_height = disp.screen.get_height()
    disp.screen = pygame.display.set_mode((scene_width, scene_height + SLIDER_HEIGHT//2))
    thorpy.init(disp.screen, thorpy.theme_classic)

    slider = thorpy.SliderWithText("Move number: ",
                                0, num_moves-1, 0,  # min, max and initial values
                                int(0.6 * scene_width), "h",  # length and orientation
                                dragger_size=(10, 20),
                                show_value_on_right_side=True,
                                edit=False)  # allow to edit value as a text
    group = thorpy.Group([slider])
    group.set_center(scene_width//2, scene_height//2)

    return slider, group.get_updater()

def layout_move_history_window(disp):
    pass