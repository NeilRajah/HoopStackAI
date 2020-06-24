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

def _scale_images(image_list, s):
    """
    Scale the images down
    """
    #Scale the images
    for i, image in enumerate(image_list):
        image = images[i]
        w = int(image.shape[1] * s); h = int(image.shape[0] * s)
        image_list[i] = cv2.resize(image, (w, h))

def _find_stacks(img, modify_images=False):
    """
    Find the stacks in the image
    """
    #Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Filter out the background
    lower_clr = np.array([15, 0, 10]);upper_clr = np.array([255, 255, 255])
    img = cv2.inRange(hsv, lower_clr, upper_clr)

    #Remove small spots to make stacks uniform
    k = 9; kernel = np.ones((k,k), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    #Find the contours in the image
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Find the bounding rectangle for each contour and get its center
    rects = [cv2.boundingRect(c) for c in contours]
    stacks = dict(); STACK_LABELS = 'ABCDEFGH'; idx = 0; all_stacks = []
    for r in rects:
        stacks[STACK_LABELS[idx]] = r
        idx += 1

    #Return the centers of all the stacks
    return stacks

if __name__ == '__main__':
    #Load all the images
    images = [cv2.imread(file) for file in listdir()]

    #Scale the images down
    _scale_images(images, 0.5)
    orig = deepcopy(images)

    #Find the stacks in the image
    for i, img in enumerate(images):
        stacks = _find_stacks(img)  #Value changes based on scale factor

        #Draw the center of each stack onto the image
        for s in stacks:
            x,y,w,h = stacks[s]
            p = x+w//2, y+h//2
            img = cv2.circle(img, p, 10, 0, -1)

    #Show all the images before and after filtering
    _show_images(orig, images)

    #Close all windows and end the program
    cv2.destroyAllWindows()