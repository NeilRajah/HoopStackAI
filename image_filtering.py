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

def get_stack_images(image):
    """
    Return the subimage of each stack in the image
    """
    return [image[y:y + h, x:x + w] for x, y, w, h in get_stack_bounds(image)]

#HAVE TO CHANGE TO USING ENTIRE GAME IMAGE TO BE ABLE TO LABEL, THIS IS POC
#Consistently splits green hoops into two pieces
#Not creating one contour per hoop consistently
def get_game_stack(stack):
    """
    Get the game version of a stack from an image of one
    """
    COLORS = {
        'CYAN': (90, 5, 5),
        'PINK': (146, 3, 5),  #doesn't work with multiple stacked on top
        'RED': (179, 2, 1),
        'PURPLE': (140, 5, 5),
        'GREEN': (60, 5, 5),
        'ORANGE': (21, 3, 5),
    }

    #Make copy of original for showing later
    orig = deepcopy(stack)

    #Filter the image
    #Filter out background
    mask = filter_bg(stack, lower=(18,0,0), e=7)
    stack = cv2.bitwise_and(stack, stack, mask=mask)

    des_color = 'CYAN'

    #Get rid of any residual pieces
    o = COLORS[des_color][2]
    stack = cv2.morphologyEx(stack, cv2.MORPH_OPEN, np.ones((o,o), np.uint8))

    #Check if black
    logging.debug('{} non-black pixels'.format(cv2.countNonZero(cv2.cvtColor(stack, cv2.COLOR_BGR2GRAY))))

    #Isolate a color
    #Represent each color by its Hue and Tolerance
    stack = cv2.cvtColor(stack, cv2.COLOR_BGR2HSV)
    hue = COLORS[des_color][0]; tol = COLORS[des_color][1]
    stack = cv2.inRange(stack, np.array([hue-tol,0,0]), np.array([hue+tol,255,255]))
    o = COLORS[des_color][2]
    stack = cv2.morphologyEx(stack, cv2.MORPH_OPEN, np.ones((o,o), np.uint8))

    # Get contours
    contours, _ = cv2.findContours(stack, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cont_mask = stack
    logging.debug('{} contours'.format(len(contours)))

    #Impose color back onto the stack image and normalize to one color
    stack = cv2.bitwise_and(orig, orig, mask=stack)
    stack = k_means(stack, 1)

    if len(contours) > 0:
        #Draw contours onto the original image
        orig = cv2.drawContours(orig, contours, -1, (0, 255, 0), 3)

        for c in contours:
            #Get the pixels on the original image within the contours
            cont_img = np.zeros_like(stack)
            cv2.drawContours(cont_img, [c], -1, 255, -1)
            pts = np.where(cont_img == 255)  # Pixels that are from the contours
            y = cv2.boundingRect(c)[1]

            #Print the unique HSV values from the contours
            hsv = cv2.cvtColor(stack, cv2.COLOR_BGR2HSV)
            color = np.unique(hsv[pts[0], pts[1]])
            print('{} found at {}'.format(color, y))
    else:
        logging.debug('no hoops in stack')

    #Show results
    cv2.imshow('original', orig)
    cv2.imshow('stack', scale_image(stack, 3))
    cv2.waitKey(0)

def unique_colors(stack):
    """
    Cluster the unique colors in the image of the stack together
    """
    # Make copy of original for showing later
    orig = deepcopy(stack)

    # Filter the image
    # Filter out background
    mask = filter_bg(stack, lower=(18, 0, 0), e=2)
    stack = cv2.bitwise_and(stack, stack, mask=mask)
    e = 3
    stack = cv2.erode(stack, np.ones((e,e), np.uint8))

    #Get the unique colors
    hsv = cv2.cvtColor(stack, cv2.COLOR_BGR2HSV)
    uniques, freq = np.unique(hsv, return_counts=True)
    for val, count in zip(uniques, freq):
        print(val, count)
    #Remove black
    # uniques = np.delete(uniques, np.where(uniques == 0))

    #Show the image and the plot
    cv2.imshow('stack', stack)
    if len(uniques) > 0:
        # Values come sorted, black is always first
        uniques = np.delete(uniques, 0)
        if len(uniques) > 0: uniques = np.delete(uniques, len(uniques)-1)
        freq = np.delete(freq, 0)
        if len(freq) > 0: freq = np.delete(freq, len(freq) - 1)

        # np.flip(uniques, 0)
        plt.plot(uniques, freq); plt.title = 'Uniques vs. Frequency'
        plt.show()
        plt.plot(uniques); plt.title = 'Uniques'
        plt.show()

def k_means(img, k):
    """
    Color quantization on an image using k-means
    """
    Z = np.float32(img.reshape((-1, 3)))
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, k+1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(img.shape)
    return res2

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