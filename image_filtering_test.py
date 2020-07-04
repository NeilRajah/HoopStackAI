"""
image_filtering_test
Author: Neil Balaskandarajah
Created on: 26/06/2020
Test filters and functions from image_filtering
"""
import cv2
import numpy as np
from image_filtering import *
from os import listdir
import logging
import matplotlib.pyplot as plt

def thresholding_window():
    #Create the image and convert it to HSV
    img = cv2.imread('tests//lvl4.png', cv2.IMREAD_COLOR)
    img = scale_image(img, 0.5)
    orig = deepcopy(img)

    #Set up the window
    win_name = 'filtering_gui'
    cv2.namedWindow(win_name)

    # Trackbars (name, min, max, [start value])
    trackbars = [
        ['Bottom H', 0, 255, 0],
        ['Bottom S', 0, 255, 0],
        ['Bottom V', 0, 255, 251],
        ['Top H', 0, 255, 255],
        ['Top S', 0, 255, 255],
        ['Top V', 0, 255, 255],
        ['Erosion', 1, 20]
    ]
    trackbar_names = [trackbar[0] for trackbar in trackbars]  #Just the names

    #Add the trackbars to the window
    for trackbar in trackbars:
        def nothing(x): pass
        cv2.createTrackbar(trackbar[0], win_name, trackbar[1], trackbar[2], nothing)
        if len(trackbar) > 3: cv2.setTrackbarPos(trackbar[0], win_name, trackbar[3])

    values = "don\'t press p when window starts".split()
    while 1:
        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            break

        #Print the HSV boundaries as python variables if p is pressed
        elif k == ord('p'):
            s1 = 'lower_HSV = np.array([{}, {}, {}])'.format(*values[:3])
            s2 = 'upper_HSV = np.array([{}, {}, {}])'.format(*values[3:6])
            print("{}\n{}\n".format(s1, s2))

        #Print the HSV boundaries as arguments
        elif k == ord('a'):
            print("{}, {}".format(values[:3], values[3:]))

        #Move one image up in list
        elif k == ord('+'):
            pass
        #Move one image back in list
        elif k == ord('-'):
            pass

        #Set the threshold boundaries to the trackbar positions
        values = [cv2.getTrackbarPos(name, win_name) for name in trackbar_names]
        mask = filter_bg(orig, lower=values[:3], upper=values[3:6], e=0)

        mask = cv2.erode(mask, np.ones((values[6], values[6]), np.uint8))

        img = cv2.bitwise_and(orig, orig, mask=mask)

        cv2.imshow('filtered', img)

def color_window():
    """
    Window for tuning colors out in images
    """
    # Create the image and convert it to HSV
    img = cv2.imread('tests//lvl11.png', cv2.IMREAD_COLOR)
    img = scale_image(img, 0.5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    orig = deepcopy(img)
    cv2.imshow('orig', orig)

    # Set up the window
    win_name = 'color_gui'
    cv2.namedWindow(win_name)

    # Trackbars (name, min, max, [start value])
    trackbars = [
        ['H', 0, 255, 63],
        ['Tol', 0, 10, 5],
        ['Open', 1, 15, 1],
        ['S Low', 0, 255],
        ['S High', 0, 255, 255],
        ['V Low', 0, 255],
        ['V High', 0, 255, 255]
    ]
    trackbar_names = [trackbar[0] for trackbar in trackbars]  # Just the names

    # Add the trackbars to the window
    for trackbar in trackbars:
        def nothing(x): pass
        cv2.createTrackbar(trackbar[0], win_name, trackbar[1], trackbar[2], nothing)
        if len(trackbar) > 3: cv2.setTrackbarPos(trackbar[0], win_name, trackbar[3])  #Set an initial value

    values = "don\'t press p when window starts".split()
    while 1:
        k = cv2.waitKey(50) & 0xFF
        if k == 27:
            break

        #Get the values
        values = {}
        slider_vals = [cv2.getTrackbarPos(name, win_name) for name in trackbar_names]
        for name, value in zip(trackbar_names, slider_vals):
            values[name] = value

        #Threshold out the colors
        hue_thresh = values['H']
        tol = values['Tol']
        lower_h = max(hue_thresh - tol, 0)
        upper_h = min(hue_thresh + tol, 255)
        lowerb = (lower_h, values['S Low'], values['V Low'])
        upperb = (upper_h, values['S High'], values['V High'])

        #Filter out the color
        mask = cv2.inRange(hsv, lowerb, upperb)
        img = cv2.bitwise_and(orig, orig, mask=mask)

        #Morphological transformation
        m = values['Open']
        # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((m,m), np.uint8))

        #Draw number of contours onto the screen
        hsv2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        cont_mask = cv2.inRange(hsv2, lowerb, upperb)
        contours, _ = cv2.findContours(cont_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = filter_out_contours(contours)
        img = cv2.drawContours(img, contours, -1, 255, 2)
        img = cv2.putText(img, str(len(contours)), (10,30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 255, 2, cv2.LINE_AA)

        cv2.imshow('filtered', img)

#--------------Tests--------------#

def _test_background_filtering(images):
    """
    Apply the background filter on each image and display it
    """
    for image in images:
        cv2.imshow('original', image)
        image = filter_bg(image)

        cv2.imshow('filter_bg', image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def _test_find_stacks(images):
    """
    Find the stacks in each image and display them
    """
    #Show the stack bounds for all images
    for image in images:
        cv2.imshow('original', image)
        stacks = get_stack_bounds(image)

        #Draw the bounds of each stack and the number of stacks
        image = cv2.putText(image, str(len(stacks)), (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        for stack in stacks:
            image = draw_rect(image, stack)
        cv2.imshow('stacks', image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def _test_click_locations(images):
    """
    Find the click locations in each image and display them
    """
    #Show the click locations for all images
    for image in images:
        cv2.imshow('original', image)
        stack_bounds = get_stack_bounds(image)
        clicks = get_click_locations(stack_bounds)

        #Draw the points at the center of their stacks and the number of points
        image = cv2.putText(image, str(len(clicks)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        for click in clicks.values():
            image = cv2.circle(image, click, 5, (0,0,0), -1)
        cv2.imshow('clicks', image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def _test_stack_images(images):
    """
    Create all the sub-images for each stack and display them
    """
    for image in images:
        cv2.imshow('original', image)
        for i,stack_image in enumerate(get_stack_images(image)):
            cv2.imshow('stack{}'.format(i), scale_image(stack_image, 1))
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def _test_thresh_color(images, files):
    """
    Test thresholding out a specified color
    """
    images = [scale_image(cv2.imread('game.png', cv2.IMREAD_COLOR), 0.5)]
    colors = Colors

    for img, file in zip(images, files):
        #Show the image
        disp = deepcopy(img)
        cv2.imshow(file, disp)

        #Get the stack bounds to draw onto the main image
        stack_bounds = get_stack_bounds(img)

        #Get all the sub-images for each stack
        stacks = get_stack_images(img)

        #Loop through all the stacks
        for stack_bound, stack in zip(stack_bounds, stacks):
            #Draw the rectangle for the current stack
            disp = deepcopy(img)
            cv2.imshow(file, draw_rect(disp, stack_bound))

            #Convert the current stack image into hsv
            img_hsv = cv2.cvtColor(stack, cv2.COLOR_BGR2HSV)
            for i,color in enumerate(colors):
                contours = thresh_color(stack, img_hsv, colors[color])

                #Draw the contours
                stack2 = deepcopy(stack)
                cont_img = cv2.drawContours(stack2, contours, -1, (255,255,255), 2)

                #Put the number of contours as text
                txt = '{}:{}'.format(color, len(contours))
                cv2.putText(stack2, txt, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

                #Display the contour information to the screen
                name = 'cont_img{}'.format(i)
                cv2.imshow(name, scale_image(cont_img, 2))
                cv2.moveWindow(name, i * 200, 600)  #THE POWER OF MOVE WINDOW

            #Skip to the next image
            if cv2.waitKey(0) == ord('1'): break
        cv2.destroyAllWindows()

def _test_get_game_stack(images):
    """
    Test creating Game instances from images
    """
    images = [scale_image(cv2.imread('game.png', cv2.IMREAD_COLOR), 0.5)]
    for img in images:
        cv2.imshow('img', img)
        cv2.waitKey(0)

        stacks = get_stack_images(img)
        for stack in stacks:
            cv2.imshow('stack', stack)
            print(get_game_stack(stack))
            cv2.waitKey(0)
        print()
        cv2.destroyAllWindows()
    cv2.destroyAllWindows()

#Get the images
DIR = 'tests//'
images = [scale_image(cv2.imread(DIR+file, cv2.IMREAD_COLOR), 0.5) for file in listdir(DIR)]
# logging.basicConfig(level=logging.DEBUG)

# thresholding_window()
# _test_background_filtering(deepcopy(images))
# _test_find_stacks(deepcopy(images))
# _test_click_locations(deepcopy(images))
# _test_stack_images(deepcopy(images))
# _test_game_stacks(deepcopy(images))
# _test_unique_colors(deepcopy(images))
# color_window()
# _test_thresh_color(deepcopy(images), listdir(DIR))
_test_get_game_stack(deepcopy(images))