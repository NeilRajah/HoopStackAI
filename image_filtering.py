"""
image_filtering
Author: Neil Balaskandarajah
Created on: 24/06/2020
Image of game in -> model of game out
"""
from game import Game
import cv2
import numpy as np
from os import listdir
from copy import deepcopy
from matplotlib import pyplot as plt

def scale_image(image, s):
    """
    Scale image by a factor of s
    """
    w = int(image.shape[1] * s); h = int(image.shape[0] * s)
    return cv2.resize(image, (w, h))

def filter_bg(img, lower_clr=None):
    """
    Filter out the background of an image of the game
    """
    # Convert to HSV
    if lower_clr is None:
        lower_clr = np.array([15, 0, 10])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Filter out the background color
    upper_clr = np.array([255, 255, 255])
    img = cv2.inRange(hsv, lower_clr, upper_clr)

    # Remove small spots to make stacks uniform
    k = 11; kernel = np.ones((k, k), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    return img

def find_stacks(img, show=False):
    """
    Find the stacks in the image
    """
    if show: orig = deepcopy(img)
    img = filter_bg(img)

    #Find the contours in the image
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Find the bounding rectangle for each contour and get its center
    rects = [cv2.boundingRect(c) for c in contours]
    stacks = dict(); STACK_LABELS = 'ABCDEFGH'; idx = 0; all_stacks = []
    for r in rects:
        stacks[STACK_LABELS[idx]] = r
        idx += 1

    if show:
        for x,y,w,h in rects:
            orig = cv2.rectangle(orig, (x,y), (x+w,y+h), 255, 3)
        orig = scale_image(orig, 0.5)
        cv2.imshow('stacks', orig)
        cv2.waitKey(0); cv2.destroyAllWindows()

    #Return the rectangles bounding each stack
    return stacks

def game_from_browser(filename, display_image=False):
    """
    Create the game from an image from the browser
    """
    #Get the image and scale it
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    img = scale_image(img, 1); orig = img

    #Show the image
    if display_image:
        cv2.imshow('browser_game', img)
        cv2.waitKey(0); cv2.destroyAllWindows()

    #Get the bounds of each stack
    stack_bounds = find_stacks(img)

    #Create smaller images for each stack
    stacks = [scale_image(img[y:y+h, x:x+w], 1) for x,y,w,h in stack_bounds.values()]

    #Filter the smaller images
    for i,stack in enumerate(stacks):
        #Remove the background
        stack_mask = filter_bg(stack, lower_clr=np.array([30,0,10]))
        stacks[i] = cv2.bitwise_and(stack, stack, mask=stack_mask)
        # cv2.imshow('stack', stacks[i]); cv2.waitKey(0)
    game_stacks = [get_game_stack(stack) for stack in stacks]

    cv2.waitKey(0); cv2.destroyAllWindows()

def get_game_stack(stack):
    """
    Create a stack from the game with the sub-image of that stack
    """
    #Blur out and convert to HSV
    game_stacks = []
    stack = cv2.medianBlur(stack, 19)  #; orig = stack
    stack = cv2.cvtColor(stack, cv2.COLOR_BGR2HSV)

    #Search down a strip of pixels to distinct colors (H values)
    x = int(stack.shape[1] * 0.25); colors = []
    for y in range(stack.shape[0]):
        h,s,v = stack[y,x]
        #Get non-black or very dark colors
        if v > 20:  #[0,255], 20 is ~9 on [0,100]
            colors.append(h)

    if len(colors) > 0: plt.plot(colors); plt.show()

    cv2.waitKey(0); cv2.destroyAllWindows()

def _split_list(lst, n):
    """
    Split the list lst into n-sized chunks
    """
    if len(lst) == 0: return []
    n = len(lst) // n
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def _avg(lst):
    """
    Return the average of a list
    """
    return sum(lst) / len(lst)

if __name__ == '__main__':
    game_from_browser('lvl3.png', display_image=False)