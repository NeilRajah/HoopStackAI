"""
browser
Author: Neil Balaskandarajah
Created on: 20/06/2020
Play the browser version of Hoop Stack
"""
import pyautogui as pag
from game import Game
from time import sleep
import cv2
import numpy as np
import matplotlib.pyplot as plt

def _get_click_locations():
    """
    Get the click locations from the user using a series of prompts
    """
    pag.alert('Press OK when browser page is open')
    labels = 'ABCDEFG'; idx = 0
    num_stacks = int(pag.prompt('How many stacks?'))
    clicks = dict()
    for stack in range(num_stacks):
        done = False
        while not done:
            x, y = pag.position()
            done = pag.confirm("Is this correct for stack {}?\n{} {}".format(labels[idx], x, y)) == 'OK'
            sleep(1)
        clicks[labels[idx]] = (x, y)
        idx += 1
    print("stack_locations = {}".format(clicks))

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
    Click between to pairs
    """
    delay = 0.1
    moveTime = 0.001
    x, y = stack_locations[pair[0]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)
    x, y = stack_locations[pair[1]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)

def _game_from_image(img):
    """
    Return a Game created with an image
    """


if __name__ == '__main__':
    #Create the game
    game = Game(5, "Level 59")
    game.add_stack([1, 2, 3, 3])
    game.add_stack([4])
    game.add_stack([4, 4, 1, 5, 5])
    game.add_stack([5, 4, 6, 2, 2])
    game.add_stack([5, 2, 6, 3, 1])
    game.add_stack([2, 6, 3, 6, 6])
    game.add_stack([5, 4, 3, 1, 1])
    game.solve()

    #Set the (x,y) coordinates of each stack
    stack_locations6 = {'A': (2049, 1131), 'B': (2213, 1121), 'C': (2430, 1097), 'D': (2033, 1379), 'E': (2274, 1372), 'F': (2436, 1406)} #6
    stack_locations7 = {'A': (3906, -1210), 'B': (4075, -1201), 'C': (4248, -1213), 'D': (3769, -958), 'E': (3958, -954),
                       'F': (4179, -938), 'G': (4377, -965)}

    try:
        _play_game(game, stack_locations6)
    except KeyboardInterrupt:
        print('keyboard exit')
    # _get_click_locations()