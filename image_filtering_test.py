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

def window():
    #Create the image and convert it to HSV
    img = cv2.imread('tests//lvl7.png', cv2.IMREAD_COLOR)
    img = scale_image(img, 0.5)
    orig = deepcopy(img)

    #Set up the window
    win_name = 'filtering_gui'
    cv2.namedWindow(win_name)

    # Trackbars (name, min, max, [start value])
    trackbars = [
        ['Bottom H', 0, 255],
        ['Bottom S', 0, 255],
        ['Bottom V', 0, 255, 248],
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

        # mask = cv2.erode(mask, np.ones((values[6], values[6]), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, np.ones((values[6], values[6]), np.uint8))

        img = cv2.bitwise_and(orig, orig, mask=mask)

        cv2.imshow('filtered', img)

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
def get_game_stack(stack_image):
    """
    Get the game version of a stack from an image of one
    """
    orig = deepcopy(stack_image)
    filtered = stack_image
    for i in range(5):
        a = 9; b = 75
        filtered = cv2.bilateralFilter(filtered, a, b, b)

    cv2.imshow('hoops', filtered)
    cv2.imshow('orig', orig)
    cv2.waitKey(0); cv2.destroyAllWindows()

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

def _test_game_stacks(images):
    """
    Create the model game stacks and print them
    """
    for image in images:
        cv2.imshow('image', image)

        #Get the images of each stack
        stack_images = get_stack_images(image)

        #Print the game's version of the stack given the image
        for stack_image in stack_images:
            stack_image = scale_image(stack_image, 3)
            get_game_stack(stack_image)

"""
Findings
16,0,0 - 255,255,239 filters out to get individual stacks
18,0,0 - 255,137,235 gets rid of holders
[0, 0, 0], [255, 255, 219] gets rid of shadow and bg, keeps colors (morph transformation after to solidify)
16,0,0 - 255,255,255 gets rid of bg
"""

#Get the images
DIR = 'tests//'
images = [scale_image(cv2.imread(DIR+file, cv2.IMREAD_COLOR), 0.5) for file in listdir(DIR)]

# window()
# _test_background_filtering(deepcopy(images))
# _test_find_stacks(deepcopy(images))
# _test_click_locations(deepcopy(images))
# _test_stack_images(deepcopy(images))
_test_game_stacks(deepcopy(images))
