"""
browser
Author: Neil Balaskandarajah
Created on: 20/06/2020
Play the browser version of Hoop Stack
"""
import pyautogui as pag
from game import Game
from time import sleep
from time import time
import cv2
import image_filtering

def _play_game(game, stack_locations):
    """
    Create the game to solve
    """
    pag.alert('Click OK when ready to begin')
    sleep(1)
    for move in game.history:
        _pair_click(stack_locations, move)

def _pair_click(stack_locations, pair):
    """
    Click between two pairs
    """
    delay = 0.1
    moveTime = 0.001
    x, y = stack_locations[pair[0]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)
    x, y = stack_locations[pair[1]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)

def _take_screenshots():
    """
    Take screenshots of stacks for testing
    """
    pag.alert('Hit ENTER when mouse is at the top left of the stacks bound')
    x1, y1 = pag.position()
    pag.alert('Hit ENTER when mouse is at the bottom right of the stacks bound')
    x2, y2 = pag.position()

    i = 0; done = False
    while not done:
        file = 'tests\\lvl{}.png'.format(i)
        sleep(0.25)
        pag.screenshot(file, region=(x1, y1, x2-x1, y2-y1))
        i += 1
        done = pag.confirm('Press OK if done, Cancel if continuing') == 'OK'
        if not done:
            pag.alert('Press OK when next level is open')

def _play_game():
    """
    Play the game in the browser

    PROCESS
    (debugging)
    get_game_bounds
        Get the image bounds
            store the x,y point of the top left

    play_level
        screenshot_game
            Take a screenshot of the image
                (show the image with cv2)
                - save to a global file name so it can be accessed within play_level

        create_game
            Create the Game object with the image
                Create all the stacks
                (print each stack)
            Set num_pieces
                Loop through all the stacks, return the first hoop
                Loop through all the stacks and count how many of that color hoop there is
                That number is num_pieces
                    ie. level 1, three cyan hoops, total stack height is three

        get_click_locations
            Center of the stack bounds of the image
            (show the image with the click locations drawn on for each stack)
            Offset with the top left of the x,y to get the screen position

        play_game
            Solve the game
            (Print with display_moves)
            (display_history)
            Play the game
                For each pair in move history, go to those locations

        next_level
            # need to get next_level button location
            Click the next level button
            Wait 1-2s for the screen to load

    Write settings to file when exiting? (ie. image bounds, next button location)
    """


if __name__ == '__main__':
    img = cv2.imread('tests//lvl2.png', cv2.IMREAD_COLOR)
    init = time()
    game = image_filtering.game_from_image(img)
    print('Create time is {0:0.3f}s'.format(time() - init))

    game.display()
    init = time()
    game.solve()
    print('Solve time is {0:0.3f}s'.format(time() - init))
    game.display_history()

    clicks = image_filtering.get_click_locations(image_filtering.get_stack_bounds(img))
    print(clicks)