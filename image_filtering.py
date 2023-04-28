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
    """Draw a rectangle onto an image

    @param image: Image to draw onto
    @param rect: Rectangle object in (top_left_x, top_left_y,
    @return: Image with the rectangle drawn over
    """
    x,y,w,h = rect
    return cv2.rectangle(image, (x,y), (x+w,y+h), [0,255,0], 2)

def scale_image(image, s):
    """Scale an image up by a factor s

    @param image: Image to scale
    @param s: Scale factor
    @return: Scaled image
    """
    w = int(image.shape[1] * s); h = int(image.shape[0] * s)
    return cv2.resize(image, (w, h))

#--------------Functions--------------#

def filter_bg(image, lower=(0,0,250), upper=(255,255,255), e=5):
    """Filter the background out for an image given lower and upper bounds
    Convert to HSV -> threshold in range -> morphologically close

    @param image: Image to filter
    @param lower: Lower bound (h, s, v)
    @param upper: Upper bound (h, s, v)
    @param e: Erosion size (integer)
    @return: Image with the background filtered out
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.inRange(image, np.array(lower), np.array(upper))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, np.ones((e, e), np.uint8))

    return image

def get_stack_bounds(image):
    """Get the bounds of the stacks from the image

    @param image: Image to find the stacks within
    @return: List of bounding rects in the image
    """
    # Backgroundless
    no_bg = filter_bg(image)

    # Get the bounding box for each stack
    contours, _ = cv2.findContours(no_bg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    no_bg = cv2.drawContours(no_bg, contours, 0, (255, 0, 0))
    cv2.imshow('no bg', no_bg); cv2.waitKey(0); cv2.destroyAllWindows()

    return [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 5]  #remove erroneous small contours

def get_click_locations(stack_bounds):
    """Get the coordinates of the clicking location for each boundingRect

    @param stack_bounds: boundingRects
    @return: The centers of each stack bound
    """
    STACK_LABELS = 'ABCDEFGHIJ'; stacks = dict()
    for i, r in enumerate(stack_bounds):
        x,y,w,h = r
        stacks[STACK_LABELS[i]] = (x+w//2, y+h//2)
    return stacks

def get_stack_images(image, bounds=None):
    """Return the subimage of each stack in the image

    @param image: Image to pull stack images from
    @param bounds: The bounds of each stack
    @return: The image for each stack
    """
    if bounds is None: bounds = get_stack_bounds(image)
    return [image[y:y + h, x:x + w] for x, y, w, h in bounds]

def game_from_image(img):
    """Create a Game object that the backtracking algorithm can solve from an image

    @param img: Snapshot of all stacks
    @return: Game object (list of stacks)
    """
    #Get the bounding box of each stack
    stack_bounds = get_stack_bounds(img)

    #Get the click locations for each stack
    clicks = get_click_locations(stack_bounds)

    #Get the image for each stack
    stack_imgs = get_stack_images(img, stack_bounds)

    #Create the Game object and the stacks to it
    # TO-DO: Move this to the Game object
    stacks = [get_game_stack(stack_img) for stack_img in stack_imgs]
    num_pieces = calc_num_pieces(stacks)
    game = Game(num_pieces)
    game.add_stacks(stacks)

    return game, clicks

def calc_num_pieces(stacks):
    # TO-DO: Move this to game
    """Calculate the number of pieces in all of the stacks

    @param stacks: List of stacks
    @return: Number of pieces in a single stack
    """
    #Choose a color
    color = None
    for stack in stacks:
        if len(stack) > 0:
            color = stack[0]

    #Max number of pieces is how many of any color is in all the stacks
    num_pieces = 0
    for stack in stacks:
        for piece in stack:
            if piece == color:
                num_pieces += 1
    return num_pieces

def get_game_stack(stack_img):
    """Create a stack that can be added to a Game object from an image of the stack

    @param stack_img: Image of a single stack
    @return: List of hoops (each hoop is represented by a color)
    """
    img = stack_img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    stack = []
    for color in Colors:
        contours = thresh_color(img, hsv, Colors[color])
        for contour in contours:
            stack.append((color, cv2.boundingRect(contour)[1]))  #Color name, y value

    stack = sorted(stack, key=lambda x: x[1])  #Sort by y value
    return [hoop[0] for hoop in stack]  #Return just the names

def thresh_color(img, img_hsv, clr):
    """Return the vertical positions of the contours of the color clr
    clr - (Hue, Hue Tolerance, Close Size, V Min)

    @param img: Image to filter
    @param img_hsv: The hsv version of the image
    @param clr: Color to filter
    @return: Vertical positions of all contours of the color clr
    """
    lowerb = (clr[0] - clr[1], 0, clr[3])
    upperb = (clr[0] + clr[1], 255, 255)

    mask = cv2.inRange(img_hsv, lowerb, upperb)
    img = cv2.bitwise_and(img, img, mask=mask)

    #Open up the image to remove spots inside
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((clr[2], clr[2]), np.uint8))

    #Find contours
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cont_mask = cv2.inRange(hsv, lowerb, upperb)
    contours, _ = cv2.findContours(cont_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Filter out bad contours
    contours = filter_out_contours(contours)

    return contours

def filter_out_contours(contours):
    """Filter out bad contours that are not hoops

    @param contours: List of contours
    @return: Contours that are/contain hoops
    """
    i = 0
    while i < len(contours):
        area = -cv2.contourArea(contours[i], True)

        if abs(area) < 180:  # Small area
            contours.pop(i)
            continue

        if area < 0:  # Black contour
            contours.pop(i)
            continue
        i += 1
    return contours

def subtract_lists(a, b):
    """Subtract b from a (a - b)

    :param a: First list
    :parma b: Second list
    :return: List a without everything in b
    """
    for x in b:
        if x in a:
            a.remove(x)

def is_black(img):
    """Return whether an image is all black or not

    :param img: Image to check
    :return: True if the image is all black, false if not
    """
    return cv2.countNonZero(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)) == 0

# logging.basicConfig(level=logging.DEBUG)
Colors = {
    'gren': (63, 5, 1, 240),
    'red ': (176, 3, 3, 250),
    'cyan': (95, 5, 3, 250),
    'blue': (109, 3, 1, 240),
    'purp': (144, 3, 1, 206),
    'pink': (153, 4, 1, 253),
    'orng': (25, 5, 1, 0)
}