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
    Click between two pairs
    """
    delay = 0.1
    moveTime = 0.001
    x, y = stack_locations[pair[0]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)
    x, y = stack_locations[pair[1]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)

def _get_image_file(file):
    """
    Return the location of image of the stacks
    """
    pag.alert('Hit ENTER when mouse is at the top left of the stacks bound')
    x1, y1 = pag.position()
    pag.alert('Hit ENTER when mouse is at the bottom right of the stacks bound')
    x2, y2 = pag.position()
    sleep(0.25); pag.screenshot(file, region=(x1, y1, x2-x1, y2-y1))
    return x1, y1

def _get_stack_locations(file, show_image=False):
    """
    Return a Game created with an image
    """
    #Get the image from the file
    img = cv2.imread(file, cv2.IMREAD_COLOR)

    #Filter out the background
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert BGR to HSV
    lower_clr = np.array([60, 0, 20]); upper_clr = np.array([255, 255, 255])
    no_bg = cv2.inRange(hsv, lower_clr, upper_clr)

    #filter out to black and white
    filtered = cv2.bitwise_and(no_bg, no_bg, mask=no_bg)

    #Blur the image so each stack becomes an individual contour
    median = cv2.medianBlur(filtered, 21)

    #get the bounding rectangle for each stack
    contours, _ = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(c) for c in contours]

    STACK_LABELS = 'ABCDEFG'; stack_locations = {}; idx = 0

    #Get the center points each stack to click
    for x,y,w,h in rects:
        x_c = x + w//2; y_c = y + h//2
        stack_locations[STACK_LABELS[idx]] = (x_c, y_c)
        idx += 1

    #Draw to the image and display it
    if show_image:
        idx = 0
        for x,y,w,h in rects:
            # Label each stack
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
            img = cv2.putText(img, STACK_LABELS[idx], (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
            idx += 1

        #show the image and wait until the pop-up closes until resuming
        cv2.imshow('Stacks', img); cv2.waitKey(0); cv2.destroyAllWindows()

    return stack_locations

def _create_game_from_image(file, stack_locations):
    """
    Create a Game instance from an image
    """
    img = cv2.imread(file, cv2.IMREAD_COLOR)

    #Filter out the background
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert BGR to HSV
    lower_clr = np.array([60, 0, 235]); upper_clr = np.array([255, 255, 255])
    no_bg = cv2.inRange(hsv, lower_clr, upper_clr)
    img = cv2.bitwise_and(img, img, mask=no_bg)

    #Erode out stacks to get each hoop individually
    m = 6; morph_kernel = np.ones((m,m), np.uint8)
    img = cv2.erode(img, morph_kernel, iterations=1)

    # Blur to get a more consistent color per stack
    img = cv2.medianBlur(img, 19)

    #Get the individual contours
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Filter out tiny contours

    #Add to this to determine number
    colors = {}; idx = 1; TOL = 5

    #Create the stacks from the contours
    for c in contours:
        #Get the color
        final = np.zeros(img.shape, np.uint8)       #Matrix of the original image
        mask = np.zeros(imgray.shape, np.uint8)     #Matrix of the gray image
        cv2.drawContours(mask, [c], 0, 255, -1)     #Draw to the mask first
        a,b,c,d = cv2.mean(img, mask)               #Before getting the color
        color = np.uint8([[[a, b, c]]])
        h = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)[0][0][0]  #Compare hue values

        if len(colors) > 0:     #There are colors, need to check if is new or not
            for color in colors:
                if abs(h - color) > TOL:  #different color
                    colors[h] = idx; idx += 1

        else:   #no colors in list, add the first color
            colors[h] = idx; idx += 1

        #Check which stack to put it in (min dist from contour to that location)
        closest_loc = stack_locations.get('A')
        min_dist = _distsq(_rect_center(), closest_loc)
        for lbl in stack_locations[1:]:
            print(min_dist)
            dist = _distsq(_rect_center(cv2.boundingRect(c)), stack_locations[lbl])
            if dist < min_dist:
                min_dist = dist
                closest_loc = lbl
        print(closest_loc)


    # cv2.imshow('game_img', img); cv2.waitKey(0); cv2.destroyAllWindows()

def _distsq(p1, p2):
    """
    Get the distance squared between two points
    """
    return (p2[0] - p1[0])**2 + (p2[1] - p1[0])**2

def _rect_center(r):
    """
    Return the center of a rectangle in (x,y)
    """
    return r.x + r.w // 2, r.y + r.h // 2

if __name__ == '__main__':
    #Create the game
    # game = Game(5, "Level 59")
    # game.add_stack([1, 2, 3, 3])
    # game.add_stack([4])
    # game.add_stack([4, 4, 1, 5, 5])
    # game.add_stack([5, 4, 6, 2, 2])
    # game.add_stack([5, 2, 6, 3, 1])
    # game.add_stack([2, 6, 3, 6, 6])
    # game.add_stack([5, 4, 3, 1, 1])
    # game.solve()

    #Set the (x,y) coordinates of each stack
    # stack_locations6 = {'A': (2049, 1131), 'B': (2213, 1121), 'C': (2430, 1097), 'D': (2033, 1379), 'E': (2274, 1372), 'F': (2436, 1406)} #6
    # stack_locations7 = {'A': (3906, -1210), 'B': (4075, -1201), 'C': (4248, -1213), 'D': (3769, -958), 'E': (3958, -954),
    #                    'F': (4179, -938), 'G': (4377, -965)}

    # _play_game(game, stack_locations6)
    # _get_click_locations()

    file = 'stacks.png'
    # x1, y1 = _get_image_file(file)
    stacks = _get_stack_locations(file, show_image=False)
    game = _create_game_from_image(file, stacks)
    # #Offset stack position based on where the top left was
    # for lbl in stacks:
    #     stacks[lbl] = (x1 + stacks[lbl][0], y1 + stacks[lbl][0])