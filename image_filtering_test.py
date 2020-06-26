"""
image_filtering_test
Author: Neil Balaskandarajah
Created on: 24/06/2020
Test the image filtering capabilities
"""
import cv2
from os import listdir
from copy import deepcopy
import image_filtering
import numpy as np

#Utility functions

def _show_images(images):
    """
    Show all of the images
    """
    for image in images:
        cv2.imshow('img', image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def _show_images_before_after(before, after):
    """
    Show a pair of images to demonstrate the effect of the filter
    """
    for bef, aft in zip(before, after):
        cv2.imshow('before', bef); cv2.imshow('after', aft)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

#Test cases

def _test_filter_bg(images):
    """
    Test filter_bg from image filtering
    """
    return [image_filtering.filter_bg(img) for img in images]

def _test_find_stacks(images):
    """
    Test find_stacks from image filtering
    """
    for image in images:
        rects = image_filtering.find_stacks(image).values()
        for x,y,w,h in rects:
            image = cv2.rectangle(image, (x,y), (x+w,y+h), 255, 3)
    return images

def _test_create_stack(images):
    """
    Test create_stack from image filtering
    """
    for image in images:
        cv2.imshow('img', image); cv2.waitKey(0); cv2.destroyAllWindows()
        stack_bounds = image_filtering.find_stacks(image).values()
        stacks = [image[y:y + h, x:x + w] for x, y, w, h in stack_bounds]
        # Filter the smaller images
        for i, stack in enumerate(stacks):
            # Remove the background
            stack_mask = image_filtering.filter_bg(stack, lower_clr=np.array([18, 0, 0]))
            stacks[i] = cv2.bitwise_and(stack, stack, mask=stack_mask)
        for stack in stacks:
            cv2.imshow('stack', stack); cv2.waitKey(0); cv2.destroyAllWindows()
            if stack.shape[0] * stack.shape[1] > 100:
                image_filtering.get_game_stack(stack)

#Main Program

if __name__ == '__main__':
    # Load all the images and scale them down
    DIR = 'tests//'
    images = [cv2.imread(DIR+file, cv2.IMREAD_COLOR) for file in listdir(DIR)]
    images = [image_filtering.scale_image(image, 0.5) for image in images]

    #Copy of images for displaying after
    orig = deepcopy(images)

    #Run tests
    # _show_images_before_after(orig, _test_filter_bg(images))  #Seems to be filtering red and orange out more
    # _show_images_before_after(orig, _test_find_stacks(images))  #Finds stacks properly
    _show_images_before_after(orig, _test_create_stack(images))  #Find the colors in the stack