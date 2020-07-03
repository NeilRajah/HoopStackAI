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
import numpy as np
import matplotlib.pyplot as plt
import image_filtering

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
    lower_clr = np.array([60, 0, 20]); upper_clr = np.array([255, 255, 255])
    no_bg = cv2.inRange(hsv, lower_clr, upper_clr)
    img = cv2.bitwise_and(img, img, mask=no_bg)

    # Blur to get a more consistent color per stack
    img = cv2.medianBlur(img, 5)

    # e = 5; img = cv2.erode(img, np.ones((e,e), np.uint8))
    # img = cv2.dilate(img, np.ones((3,3), np.uint8))

    cv2.imshow('img', img)

    #k means clustering
    z = np.float32(img.reshape((-1,3)))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 2
    ret, label, center = cv2.kmeans(z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    cv2.imshow('kmeans', res2)

    cv2.waitKey(0); cv2.destroyAllWindows()

    # cv2.imshow('game_img', img);
    cv2.waitKey(0); cv2.destroyAllWindows()

def _filter_window(img):
    """
    Window with trackbars for tuning filters
    """
    win_name = 'HSV Tuning'
    def nothing(x): pass
    cv2.namedWindow(win_name)
    cv2.createTrackbar('bottom H', win_name, 0, 255, nothing)
    cv2.createTrackbar('bottom S', win_name, 0, 255, nothing)
    cv2.createTrackbar('bottom V', win_name, 0, 255, nothing)
    cv2.createTrackbar('top H', win_name, 0, 255, nothing)
    cv2.createTrackbar('top S', win_name, 0, 255, nothing)
    cv2.createTrackbar('top V', win_name, 0, 255, nothing)
    # cv2.imshow('img', img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert BGR to HSV
    # cv2.imshow('img', img)

    while 1:
        k = cv2.waitKey(1) & 0xFF
        if k == 27: break

        H_bot = cv2.getTrackbarPos('bottom H', win_name)
        S_bot = cv2.getTrackbarPos('bottom S', win_name)
        V_bot = cv2.getTrackbarPos('bottom V', win_name)
        H_top = cv2.getTrackbarPos('top H', win_name)
        S_top = cv2.getTrackbarPos('top S', win_name)
        V_top = cv2.getTrackbarPos('top V', win_name)

        # Filter out the background
        lower_clr = np.array([H_bot, S_bot, V_bot]); upper_clr = np.array([H_top, S_top, V_top])
        no_bg = cv2.inRange(hsv, lower_clr, upper_clr)
        img = cv2.bitwise_and(img, img, mask=no_bg)

        # Blur to get a more consistent color per stack
        # img = cv2.medianBlur(img, 19)
        cv2.imshow('no_bg', no_bg)
        cv2.imshow(win_name, img)

    #17, 0, 239; 255, 255, 255

    cv2.destroyAllWindows()

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

def _play_hardcoded_game():
    """
    Play the game with hard-coded values
    """
    # Create the game
    game = Game(5, "Level 59")
    game.add_stack([1, 2, 3, 3])
    game.add_stack([4])
    game.add_stack([4, 4, 1, 5, 5])
    game.add_stack([5, 4, 6, 2, 2])
    game.add_stack([5, 2, 6, 3, 1])
    game.add_stack([2, 6, 3, 6, 6])
    game.add_stack([5, 4, 3, 1, 1])
    game.solve()

    # Set the (x,y) coordinates of each stack
    stack_locations6 = {'A': (2049, 1131), 'B': (2213, 1121), 'C': (2430, 1097), 'D': (2033, 1379), 'E': (2274, 1372), 'F': (2436, 1406)} #6
    stack_locations7 = {'A': (3906, -1210), 'B': (4075, -1201), 'C': (4248, -1213), 'D': (3769, -958), 'E': (3958, -954),
                       'F': (4179, -938), 'G': (4377, -965)}

    _play_game(game, stack_locations6)

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