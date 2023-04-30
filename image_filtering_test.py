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

def thresholding_window(filename):
    #Create the image and convert it to HSV
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
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
    img = cv2.imread('game.png', cv2.IMREAD_COLOR)
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

def hstack_images(original, processed, cvt_to_bgr=True):
    """Stack two images horizontally

    @param original: Original pre-processed image (appears on left)
    @param processed: Post-processed image to be filtered(appears on right)
    @param cvt_to_bgr: Whether to convert the processed image back to BGR or not
    @return: Image containing img1 and img2
    """
    if cvt_to_bgr:
        return np.hstack((original, cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)))
    return np.hstack((original, processed))

def _test_background_filtering(images):
    """Apply the background filter on each image and display it

    @param images: Images to apply the background filter onto
    """
    print('STARTING BACKGROUND FILTERING TEST')

    for i, image in enumerate(images):
        bg_filtered_image = filter_bg(image)
        original_and_filtered = hstack_images(image, bg_filtered_image)

        cv2.imshow('original & background filtered image ({})'.format(i), original_and_filtered)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    print('FINISHED BACKGROUND FILTERING TEST\n')

def _test_find_stacks(images):
    """Find the stacks in each image and display them

    @param images: Images to find the stacks in
    """
    print('STARTING STACK LOCATION TEST')

    # Show the stack bounds for all images
    for i, image in enumerate(images):
        stacks = get_stack_bounds(image)

        # Draw the bounds of each stack and the number of stacks
        stack_image = cv2.putText(np.copy(image),
                                  'num_stacks: {}'.format(len(stacks)),
                                  (10,30),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.75, (0,0,0), 1, cv2.LINE_AA)
        for stack in stacks:
            stack_image = draw_rect(stack_image, stack, [0, 0, 0])

        original_and_stacks = hstack_images(image, stack_image, cvt_to_bgr=False)
        cv2.imshow('original & stack-identified image ({})'.format(i), original_and_stacks)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

    print('ENDING STACK LOCATION TEST\n')

def _test_click_locations(images):
    """Find the click locations in each image and display them

    @param images: Images to find the click locations in
    """
    #Show the click locations for all images
    for i, image in enumerate(images):
        stack_bounds = get_stack_bounds(image)
        clicks = get_click_locations(stack_bounds)

        #Draw the number of points and the points at the center of their stacks
        clicks_image = cv2.putText(np.copy(image),
                                   'num_stacks: {}'.format(len(clicks)),
                                   (10, 30),
                                   cv2.FONT_HERSHEY_DUPLEX,
                                   0.75, (0, 0, 0), 1, cv2.LINE_AA)
        for click in clicks.values():
            clicks_image = cv2.circle(clicks_image, click, 5, (0,0,0), -1)

        original_and_clicks = hstack_images(image, clicks_image, False)
        cv2.imshow('original and clicks_image {}'.format(i), original_and_clicks)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def _test_stack_images(images):
    """Create all the sub-images for each stack and display them

    @param images: Images to find the stack images in
    """
    SIZE = (100, 150)
    for i, image in enumerate(images):
        # for idx,stack_image in enumerate(get_stack_images(image)):
        #     cv2.imshow('stack{}'.format(i), scale_image(stack_image, 1))
        stack_images = get_stack_images(image)
        combined_stack_images = cv2.resize(stack_images[0], SIZE)
        for stack_img in stack_images:
            combined_stack_images = np.hstack((combined_stack_images, cv2.resize(stack_img, SIZE)))
        cv2.imshow('all stack images from image {}'.format(i), combined_stack_images)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def _test_thresh_color(images):
    """Test thresholding out a specified color

    @param images: Images to apply a specific color threshold filter on
    """
    for img in images:
        # Get the stack bounds to draw onto the main image
        stack_bounds = get_stack_bounds(img)

        # Get all the sub-images for each stack
        stack_images = get_stack_images(img)

        SIZE = (200, 300)
        filtered_imgs = []

        # Loop through all the stacks
        for stack_bound, stack_img in zip(stack_bounds, stack_images):
            #Draw the rectangle for the current stack
            disp = deepcopy(img)
            located_stacks_img = draw_rect(np.copy(disp), stack_bound, [0,0,0])
            cv2.imshow('Filtering stack', located_stacks_img)

            # Convert the current stack image into hsv
            stack_img_hsv = cv2.cvtColor(stack_img, cv2.COLOR_BGR2HSV)
            for i, color in enumerate(COLORS):
                contours = thresh_color(stack_img, stack_img_hsv, COLORS[color])

                # Draw the contours
                stack2 = deepcopy(stack_img)
                cont_img = cv2.drawContours(stack2, contours, -1, (255,255,255), 2)
                # cont_img = cv2.resize(cont_img, SIZE)

                # Put the number of contours as text
                txt = '{}:{}'.format(color, len(contours))
                print(txt)

                # Display the contour information to the screen
                cv2.imshow(txt, scale_image(cont_img, 9))
                filtered_imgs.append(cont_img)
                cv2.moveWindow(txt, 180*i, 600)
            # cv2.imshow('filtered_images', np.hstack(filtered_imgs))
            print()
            # Skip to the next image
            if cv2.waitKey(0) == ord('1'):
                break
        cv2.destroyAllWindows()

def _test_get_game_stack(images):
    """
    Test creating Game instances from images
    """
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

def _test_game_from_image():
    """
    Test creating a game from an image
    """
    img = cv2.imread('game.png', cv2.IMREAD_COLOR)
    img = scale_image(img, 0.5)
    game, _ = game_from_image(img)
    game.display()
    [print('{},'.format(x)) for x in game.stacks.values()]
    # game.solve()
    # game.display()

#Get the images
DIR = 'tests//'
# images = [scale_image(cv2.imread(DIR+file, cv2.IMREAD_COLOR), 0.5) for file in listdir(DIR)]
# logging.basicConfig(level=logging.DEBUG)
images = [scale_image(cv2.imread('tests//lvl2.png', cv2.IMREAD_COLOR), 0.5)]

# thresholding_window('game.png')
_test_background_filtering(deepcopy(images))
_test_find_stacks(deepcopy(images))
_test_click_locations(deepcopy(images))
_test_stack_images(deepcopy(images))
# color_window()
_test_thresh_color(deepcopy(images))
# _test_get_game_stack(deepcopy(images))
# _test_game_from_image()