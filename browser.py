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

def _game_from_image(file):
    """
    Return a Game created with an image
    """
    #Get the image from the file
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    # cv2.imshow('img', img)

    #Filter out the background
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert BGR to HSV
    lower_clr = np.array([60, 0, 20]); upper_clr = np.array([255, 255, 255])
    no_bg = cv2.inRange(hsv, lower_clr, upper_clr)

    #filter out to black and white
    filtered = cv2.bitwise_and(no_bg, no_bg, mask=no_bg)
    # cv2.imshow('filtered', filtered)

    #Blur the image so each stack becomes an individual contour
    median = cv2.medianBlur(filtered, 21)
    # cv2.imshow('median', median)

    contours, _ = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #can only take black and white
    # img = cv2.drawContours(img, cnt, -1, (0,255,0), 3)

    STACK_LABELS = 'ABCDEFG'; idx = 0

    #get all the bounding rectangles for the contours
    rects = [cv2.boundingRect(c) for c in contours];

    #Draw on the image
    for x,y,w,h in rects:
        #draw bounding rectangle and its label
        img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,0), 2)
        img = cv2.putText(img, STACK_LABELS[idx], (x,y), cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,0), 3)
        idx += 1

        #draw the centers of each bounding rect
        # x_c = x + w//2; y_c = y + h//2
        # img = cv2.circle(img, (x_c, y_c), 5, (0, 0, 0), -1)

        #draw potential stack points
        n = 6; h_step = h//n
        for i in range(1, n):
            img = cv2.circle(img, (x + w//2, y + h_step*i), 5, (0,0,0), -1)

    #resize image to show
    s = 3; size_dim = (int(img.shape[1]*s), int(img.shape[0]*s))
    img = cv2.resize(img, size_dim)
    cv2.imshow('with contours', img)

    # def nothing(x): pass

    # win_name = 'finding contours'
    # cv2.namedWindow(win_name)
    # cv2.createTrackbar('bot', win_name, 0, 255, nothing)
    # cv2.createTrackbar('top', win_name, 0, 255, nothing)
    #
    # while 1:
    #     cv2.imshow(win_name, mask)
    #     k = cv2.waitKey(1) & 0xFF
    #     if k == 27:
    #         break
    #
    #     bot = cv2.getTrackbarPos('bot', win_name)
    #     top = cv2.getTrackbarPos('top', win_name)
    #     ret, mask = cv2.threshold(median, bot, top,cv2.THRESH_BINARY)

    cv2.waitKey(0); cv2.destroyAllWindows()

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
    # game.solve()

    #Set the (x,y) coordinates of each stack
    stack_locations6 = {'A': (2049, 1131), 'B': (2213, 1121), 'C': (2430, 1097), 'D': (2033, 1379), 'E': (2274, 1372), 'F': (2436, 1406)} #6
    stack_locations7 = {'A': (3906, -1210), 'B': (4075, -1201), 'C': (4248, -1213), 'D': (3769, -958), 'E': (3958, -954),
                       'F': (4179, -938), 'G': (4377, -965)}

    # _play_game(game, stack_locations6)
    # _get_click_locations()
    _game_from_image('lvl58.png')