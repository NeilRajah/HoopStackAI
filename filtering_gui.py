"""
filtering_gui
Author: Neil Balaskandarajah
Created on: 26/06/2020
A GUI for testing different filters
"""
import cv2
import numpy as np
from image_filtering import *

def window():
    img = cv2.imread('tests//lvl0.png', cv2.IMREAD_COLOR)
    img = scale_image(img, 0.5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    win_name = 'filtering_gui'
    cv2.namedWindow(win_name)

    # Trackbars (name, min, max, [start value])
    trackbars = [
        ['Bottom H', 0, 255, 16],
        ['Bottom S', 0, 255],
        ['Bottom V', 0, 255],
        ['Top H', 0, 255, 255],
        ['Top S', 0, 255, 255],
        ['Top V', 0, 255, 239]
    ]
    trackbar_names = [trackbar[0] for trackbar in trackbars]

    #Add the trackbars to the window
    for trackbar in trackbars:
        def nothing(x): pass
        cv2.createTrackbar(trackbar[0], win_name, trackbar[1], trackbar[2], nothing)
        if len(trackbar) > 3: cv2.setTrackbarPos(trackbar[0], win_name, trackbar[3])

    while 1:
        k = cv2.waitKey(1) & 0xFF
        if k == 27: break

        values = [cv2.getTrackbarPos(name, win_name) for name in trackbar_names]
        lower_HSV = np.array([values[0], values[1], values[2]])
        upper_HSV = np.array([values[3], values[4], values[5]])
        img = cv2.inRange(hsv, lower_HSV, upper_HSV)

        cv2.imshow('filtered', img)

"""
Findings
16,0,0 - 255,255,239 filters out to get individual stacks
"""

window()