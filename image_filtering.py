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

def _show_images(orig_list, image_list):
    """
    Display a list of images to the screen, before and after filtering
    """
    for orig, img in zip(orig_list, image_list):
        cv2.imshow('filtered', img)
        cv2.imshow('original', orig)
        cv2.waitKey(0)

def _scale_image(image, s):
    """
    Scale image by a factor of s
    """
    w = int(image.shape[1] * s); h = int(image.shape[0] * s)
    return cv2.resize(image, (w, h))

def _scale_images(image_list, s):
    """
    Scale the images down
    """
    #Scale the images
    for i, image in enumerate(image_list):
        image = image_list[i]
        w = int(image.shape[1] * s); h = int(image.shape[0] * s)
        image_list[i] = cv2.resize(image, (w, h))

def _find_stacks(img, show=False):
    """
    Find the stacks in the image
    """
    if show: orig = deepcopy(img)
    img = _filter_bg(img)

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
        cv2.imshow('stacks', orig)
        cv2.waitKey(0); cv2.destroyAllWindows()

    #Return the rectangles bounding each stack
    return stacks

def _test_filtering():
    """
    Test the filtering on all images
    """
    # Load all the images
    images = [cv2.imread(file) for file in listdir()]

    # Scale the images down
    _scale_images(images, 0.5)
    orig = deepcopy(images)

    # Find the stacks in the image
    stack_centers = dict(); STACK_LABELS = 'ABCDEFGH'
    for i, img in enumerate(images):
        stacks = _find_stacks(img)  # Value changes based on scale factor

        # Add the center point of each stack to its own list
        for s in stacks:
            x, y, w, h = stacks[s]
            p = x + w // 2, y + h // 2

            img = cv2.circle(img, p, 10, 0, -1)

    # Show all the images before and after filtering
    _show_images(orig, images)

    # Close all windows and end the program
    cv2.destroyAllWindows()

def game_from_browser(filename, display_image=False):
    """
    Create the game from an image from the browser
    """
    #Get the image and scale it
    img = cv2.imread(filename, cv2.COLOR_RGB2BGR)
    img = _scale_image(img, 2); orig = img

    #Get the bounds of each stack
    stack_bounds = _find_stacks(img, show=False)

    #Create smaller images for each stack
    stacks = [img[y:y+h, x:x+w] for x,y,w,h in stack_bounds.values()]

    #Show the smaller images
    for i,stack in enumerate(stacks):
        #Filter out background
        stack_mask = _filter_bg(stack, type='stack')

        stack = cv2.bitwise_and(stack, stack, mask=stack_mask)
        e = 8; stack = cv2.erode(stack, np.ones((e,e), np.uint8))
        stack = cv2.medianBlur(stack, 41)
        stack = _k_means(stack, 3)

        cv2.imshow('stack{}'.format(i), stack)

    cv2.waitKey(0); cv2.destroyAllWindows()
    #Show the image
    if display_image:
        cv2.imshow('browser_game', img)
        cv2.waitKey(0); cv2.destroyAllWindows()

def _k_means(img, k):
    """
    Apply k means clustering on an image given a number of clusters
    """
    # k means cluster
    z = np.float32(img.reshape((-1, 3)))
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(img.shape)
    return res2

def _filter_bg(img, type='loc'):
    """
    Filter out the background of an image of the game
    """
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Filter out the background color
    if type == 'loc':
        lower_clr = np.array([15, 0, 10])
    elif type == 'stack':
        lower_clr = np.array([30, 0, 10])
    upper_clr = np.array([255, 255, 255])
    img = cv2.inRange(hsv, lower_clr, upper_clr)

    # Remove small spots to make stacks uniform
    k = 9;
    kernel = np.ones((k, k), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img

if __name__ == '__main__':
    game_from_browser('lvl2.png', display_image=False)