"""
cv_test
Author: Neil Balaskandarajah
Created on: 21/06/2020
Test for opencv
"""
import cv2
import numpy as np
from game import Game

#load the image in
img = cv2.imread('lvl58.png', cv2.IMREAD_COLOR)
cv2.imshow('regular', img)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert regular BRG img to gray
cv2.imshow('grayscale', img_gray)

#Drawing on images
# cv2.line(img, (0,0), (100,100), (0, 0, 255), 5)  #line
roi_1 = (90, 50); roi_2 = (160,140)
# cv2.rectangle(img, roi_1, roi_2, (0,0,0), 1)  #rectangle
# cv2.circle(img, (200, 200), 30, (0, 255, 0), 2)  #circle; -1 is filled in
# cv2.polylines(img, [np.array([[10, 10], [20, 20], [10, 30]], np.int32)], True, (255,0,0), 2)  #draw points
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img, 'yihay!', (20, 150), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

# px = img[22, 22]  #get pixel
# print(px)
# px = [0,0,0]
# print(px)

#ROI: Region of Image
roi = img[100:150, 100:150]
# img[roi_1[1]:roi_2[1], roi_1[0]:roi_2[0]] = [255, 255,255]

# stack_A = img[roi_1[1]:roi_2[1], roi_1[0]:roi_2[0]]  #get region of image
# img[0:roi_2[1]-roi_1[1], 0:roi_2[0]-roi_1[0]] = stack_A  #paste region of image to another section

#Thresholding
rows, cols, channels = img.shape
roi = img[0:rows, 0:cols]
ret, mask = cv2.threshold(img_gray, 140, 255, cv2.THRESH_BINARY_INV)  #if pixel value above 220, conv to 0, below to 255
# cv2.imshow('invbin', mask)

gaus = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 115, 1)
# cv2.imshow('gaus', gaus)

#Color filtering
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #Convert BGR to HSV
lower_clr = np.array([50, 0, 190]); upper_clr = np.array([255, 255, 255])  #Top and bottom bounds in HSV

mask = cv2.inRange(hsv, lower_clr, upper_clr)  #pixels in the range of lower and upper
res = cv2.bitwise_not(img, img_gray, mask=mask)
cv2.imshow('filtered', res)

cv2.waitKey(0); cv2.destroyAllWindows()