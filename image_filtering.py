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
import logging

def draw_rect(image, rect):
    """
    Draw a rectangle onto image based on its top left (x,y) and width and height
    """
    x,y,w,h = rect
    return cv2.rectangle(image, (x,y), (x+w,y+h), [0,255,0], 2)

def scale_image(image, s):
    """
    Scale image by a factor of s
    """
    w = int(image.shape[1] * s); h = int(image.shape[0] * s)
    return cv2.resize(image, (w, h))

#--------------Functions--------------#

def contrast_brightness(image, alpha, beta):
    """
    Change the contrast and brightness of an image
    """
    new_image = np.zeros(image.shape, image.dtype)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)
    return new_image

def filter_bg(image, lower=(16,0,0), upper=(255,255,255), e=14):
    """
    Filter the background out for an image given lower and upper bounds
    Convert to HSV -> threshold in range -> morphologically close
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.inRange(image, np.array(lower), np.array(upper))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, np.ones((e, e), np.uint8))
    return image

def get_stack_bounds(image):
    """
    Get the bounds of each stack in that image
    """
    # Backgroundless
    no_bg = filter_bg(image)

    # Get the bounding box for each stack
    contours, _ = cv2.findContours(no_bg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return [cv2.boundingRect(c) for c in contours]

def get_click_locations(stack_bounds):
    """
    Return the click locations for each stack
    """
    STACK_LABELS = 'ABCDEFGHIJ'; stacks = dict()
    for i, r in enumerate(stack_bounds):
        x,y,w,h = r
        stacks[STACK_LABELS[i]] = (x+w//2, y+h//2)
    return stacks

def get_stack_images(image, bounds=None):
    """
    Return the subimage of each stack in the image
    """
    if bounds is None: bounds = get_stack_bounds(image)
    return [image[y:y + h, x:x + w] for x, y, w, h in bounds]

def game_from_image(img):
    """
    Create a Game object from an image
    """
    #Get the bounding box of each stack
    stack_bounds = get_stack_bounds(img)

    #Get the click locations for each stack
    clicks = get_click_locations(stack_bounds)

    #Get the image for each stack
    stacks = get_stack_images(img, stack_bounds)

    #Create the Game object and the stacks to it
    num_pieces = 0
    game = Game(num_pieces)
    for stack in stacks:
        s = get_game_stack(stack)
        game.add_stack(s)
        if len(s) > num_pieces: num_pieces = len(s)
    game.num_pieces = num_pieces

    return game

def get_game_stack(stack_img):
    """
    Create a stack that can be added to a Game object from an image of the stack
    """
    img = stack_img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    stack = []
    for color in Colors:
        contours = thresh_color(img, hsv, Colors[color])
        for contour in contours:
            stack.append((color, cv2.boundingRect(contour)[1]))  #Color name, y value

    stack = sorted(stack, key=lambda x: x[1], reverse=True)  #Sort by y value
    return [hoop[0] for hoop in stack]  #Return just the names

def thresh_color(img, img_hsv, clr):
    """
    Return the vertical positions of the contours of the color clr
    clr - (Hue, Hue Tolerance, Close Size, V Min)
    """
    lowerb = (clr[0] - clr[1], 0, clr[3])
    upperb = (clr[0] + clr[1], 255, 255)
    logging.debug('thresh_color: {}, {}'.format(lowerb, upperb))

    mask = cv2.inRange(img_hsv, lowerb, upperb)
    img = cv2.bitwise_and(img, img, mask=mask)

    #If image is all black, return an empty list (that color isn't present
    if is_black(img):
        logging.debug('thresh_color: no {} found in img'.format(clr))
    # return []

    #Open up the image to remove spots inside
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((clr[2], clr[2]), np.uint8))

    #Find contours
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cont_mask = cv2.inRange(hsv, lowerb, upperb)
    contours, _ = cv2.findContours(cont_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    logging.debug('There are {} contours before filtering'.format(len(contours)))

    #Filter out bad contours
    contours = filter_out_contours(contours)
    logging.debug('There are {} contours after filtering'.format(len(contours)))

    return contours

def filter_out_contours(contours):
    """
    Filter out bad contours that are not hoops
    """
    i = 0
    while i < len(contours):
        area = -cv2.contourArea(contours[i], True)
        logging.debug('area is {}'.format(area))

        if abs(area) < 180:  # Small area
            contours.pop(i)
            logging.debug('removed contour because of small area')
            continue

        if area < 0:  # Black contour
            contours.pop(i)
            logging.debug('removed contour because only black pixels')
            continue
        i += 1
    return contours

def subtract_lists(a, b):
    """
    Subtract b from a (a - b)
    """
    for x in b:
        if x in a:
            a.remove(x)

def is_black(img):
    """
    Return whether an image is all black or not
    """
    return cv2.countNonZero(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)) == 0

# logging.basicConfig(level=logging.DEBUG)
Colors = {
    'green': (63, 5, 1, 240),
    'red': (176, 3, 3, 250),
    'cyan': (95, 5, 3, 250),
    'blue': (109, 3, 1, 240),
    'purple': (144, 4, 1, 241),
    'pink': (153, 4, 1, 255),
    'orange': (25, 5, 1, 0)
}