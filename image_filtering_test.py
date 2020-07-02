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

        # mask = cv2.erode(mask, np.ones((values[6], values[6]), np.uint8))
        # mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, np.ones((values[6], values[6]), np.uint8))
        mask = cv2.erode(mask, np.ones((values[6], values[6]), np.uint8))

        img = cv2.bitwise_and(orig, orig, mask=mask)

        cv2.imshow('filtered', img)

def color_window():
    """
    Window for tuning colors out in images
    """
    # Create the image and convert it to HSV
    img = cv2.imread('tests//lvl5.png', cv2.IMREAD_COLOR)
    img = scale_image(img, 0.5)
    orig = deepcopy(img)
    cv2.imshow('orig', orig)

    # Set up the window
    win_name = 'color_gui'
    cv2.namedWindow(win_name)

    # Trackbars (name, min, max, [start value])
    trackbars = [
        ['H Value', 0, 255, 95],
        ['Tolerance (+/-)', 0, 10, 5],
        ['Open', 1, 15, 2],
        ['Canny Low', 0, 500, 0],
        ['Canny High', 0, 500, 0],
        ['Blur', 1, 100, 1],
        ['Alpha', 0, 1000],
        ['Beta', 0, 1000]
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

        # Print the HSV boundaries as python variables if p is pressed
        elif k == ord('p'):
            s1 = 'lower_HSV = np.array([{}, {}, {}])'.format(*values[:3])
            s2 = 'upper_HSV = np.array([{}, {}, {}])'.format(*values[3:6])
            print("{}\n{}\n".format(s1, s2))

        # Print the HSV boundaries as arguments
        elif k == ord('a'):
            print("{}, {}".format(values[:3], values[3:]))

        #Filter out the background
        mask = filter_bg(orig)
        img = cv2.bitwise_and(orig, orig, mask=mask)

        #Threshold out the colors
        values = [cv2.getTrackbarPos(name, win_name) for name in trackbar_names]
        hue_thresh = values[0]
        tol = values[1]
        lower_h = max(hue_thresh - tol, 0)
        upper_h = min(hue_thresh + tol, 255)

        mask2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask2 = cv2.inRange(mask2, (lower_h, 0, 0), (upper_h, 255, 255))
        img = cv2.bitwise_and(img, img, mask=mask2)

        #Morphological transformation
        m = values[2]
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((m,m), np.uint8))

        #Blurring
        b = values[5]
        if b > 0:
            img = cv2.blur(img, (b, b))

        #Change brightness and contrast
        # alpha = values[6] / 1000; beta = values[7] / 1000
        # img = contrast_brightness(img, alpha, beta)

        #Canny edge detection
        low_canny = values[3]; high_canny = values[4]
        if low_canny != 0 and high_canny != 0:
            img = cv2.Canny(img, low_canny, high_canny, L2gradient=True)

        cv2.imshow('filtered', img)

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

def thresh_blue(img):
    """
    Threshold out all colors but blue
    """
    #Make copy of image for later viewing
    s = 1
    img = scale_image(img, s)
    orig = deepcopy(img)

    #Define blue
    blue_h = 95
    blue_tol = 5
    blue_close = int(3 * s)
    blue_lower = (blue_h - blue_tol, 0, 250)
    blue_upper = (blue_h + blue_tol, 255, 255)

    #Filter out blue
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, blue_lower, blue_upper) #Filter out just blue
    img = cv2.bitwise_and(img, img, mask=mask)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((blue_close, blue_close), np.uint8))
    # img = k_means(img, 1)  #Don't need to isolate colors

    #Find the contours
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cont_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    contours, _ = cv2.findContours(cont_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    logging.debug('There are {} contours before filtering'.format(len(contours)))

    #Filter out bad contours
    contours = filter_out_contours(contours)
    logging.debug('There are {} contours after filtering'.format(len(contours)))

    if len(contours) > 0:
        # Sort the contours based on their y values
        def cont_sort_key(c):
            return cv2.boundingRect(c)[1]
        contours = sorted(contours, key=cont_sort_key)
        y = [cv2.boundingRect(c)[1] for c in contours]
        logging.debug('y values are {}'.format(y))

        #Show each individual contour
        for i, c in enumerate(contours):
            cont_img = cv2.drawContours(deepcopy(orig), [c], -1, (0, 0, 255), 2)
            cv2.imshow('contour{}'.format(i), scale_image(cont_img, 2))
            cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        logging.debug('no contours\n')

    #Show before and after
    cv2.imshow('original', orig)
    cv2.imshow('filtered', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def thresh_red(img):
    """
    Threshold red hoops out
    """
    # Make copy of image for later viewing
    s = 1
    img = scale_image(img, s)
    orig = deepcopy(img)

    #Define red
    red_h = 176
    red_tol = 3
    red_close = int(3 * s)
    red_lower = (red_h - red_tol, 0, 250)
    red_upper = (red_h + red_tol, 255, 255)

    #Filter out red
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #Could pass this into the function
    mask = cv2.inRange(hsv, red_lower, red_upper)  # Filter out just blue
    img = cv2.bitwise_and(img, img, mask=mask)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((red_close, red_close), np.uint8))

    #Find contours
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cont_mask = cv2.inRange(hsv, red_lower, red_upper)
    contours, _ = cv2.findContours(cont_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    logging.debug('There are {} contours before filtering'.format(len(contours)))

    #Filter out bad contours
    contours = filter_out_contours(contours)
    logging.debug('There are {} contours after filtering'.format(len(contours)))

    if len(contours) > 0:
        # Sort the contours based on their y values
        def cont_sort_key(c):
            return cv2.boundingRect(c)[1]

        contours = sorted(contours, key=cont_sort_key)
        y = [cv2.boundingRect(c)[1] for c in contours]
        logging.debug('y values are {}'.format(y))

        # Show each individual contour
        for i, c in enumerate(contours):
            cont_img = cv2.drawContours(deepcopy(orig), [c], -1, (0, 255, 0), 2)
            cv2.imshow('contour{}'.format(i), scale_image(cont_img, 2))
            cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        logging.debug('no contours\n')

    # Show before and after
    cv2.imshow('original', orig)
    cv2.imshow('filtered', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #Sort the contours


def filter_out_contours(contours):
    """
    Filter out bad contours that are not hoops
    """
    i = 0
    while i < len(contours):
        area = -cv2.contourArea(contours[i], True)
        logging.debug('area is {}\n'.format(area))

        if abs(area) < 100:  # Small area
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
    image = images[6]  #[5] has orange
    #3 has pink and blue
    cv2.imshow('full', image)
    stacks = get_stack_images(image)
    print('There are {} stacks'.format(len(stacks)))
    for i,stack in enumerate(stacks):
        get_game_stack(stack)

def _test_unique_colors(images):
    """
    Test the functionality of unique_colors
    """
    image = images[6]
    stacks = get_stack_images(image)
    for i,stack in enumerate(stacks):
        unique_colors(stack)

def _test_thresh_blue(images):
    """
    Test the functionality of thresholding blue out
    """
    for image in images:
        stacks = get_stack_images(image)
        for i, stack in enumerate(stacks):
            thresh_blue(stack)

def _test_thresh_red(images):
    """
    Test the functionality of thresholding red out
    """
    # image = cv2.imread('tests//lvl5.png', cv2.IMREAD_COLOR)
    # stacks = get_stack_images(image)
    # for i, stack in enumerate(stacks):
    #     thresh_red(stack)
    for image in images:
        stacks = get_stack_images(image)
        for i, stack in enumerate(stacks):
            thresh_red(stack)

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
logging.basicConfig(level=logging.DEBUG)

# thresholding_window()
# color_window()
# _test_background_filtering(deepcopy(images))
# _test_find_stacks(deepcopy(images))
# _test_click_locations(deepcopy(images))
# _test_stack_images(deepcopy(images))
# _test_game_stacks(deepcopy(images))
# _test_unique_colors(deepcopy(images))
# _test_thresh_blue(deepcopy(images))
_test_thresh_red(deepcopy(images))