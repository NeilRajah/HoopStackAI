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

def game_from_browser(filename):
    """
    Create the game from an image from the browser
    """
    #Get the image and scale it
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    img = scale_image(img, 0.5)
    orig = img

    #Image to filter to remove the background
    stack_bg = img
    win_name = 'filtering'
    # contours, hierarchy = cv2.findContours(stack_bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours = np.array(contours).reshape((-1,1,2)).astype(np.int32)
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

    cv2.imshow('original', orig); cv2.imshow('stack_bg', stack_bg)
    cv2.waitKey(0); cv2.destroyAllWindows()

if __name__ == '__main__':
    game_from_browser('lvl2.png')