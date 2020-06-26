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
img = cv2.imread('tests/lvl58.png', cv2.IMREAD_COLOR)
# cv2.imshow('regular', img)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert regular BRG img to gray
# cv2.imshow('grayscale', img_gray)

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
ret, mask = cv2.threshold(img_gray, 140, 255, cv2.THRESH_BINARY_INV)  #if pixel value above a, conv to 0, below to 255
# cv2.imshow('invbin', mask)

gaus = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 115, 1)
# cv2.imshow('gaus', gaus)

#Color filtering
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #Convert BGR to HSV
lower_clr = np.array([60, 30, 20]); upper_clr = np.array([255, 255, 255])  #Top and bottom bounds in HSV
#tune H for specific color
#tune S for how vibrant/faded it is
#tune V for how light/dark color is

mask = cv2.inRange(hsv, lower_clr, upper_clr)  #pixels in the range of lower and upper
filtered = cv2.bitwise_and(img, img, mask=mask)
cv2.imshow('filtered', filtered)

#Blurring and Smoothing
kx = ky = 8 #reduces spots
kernel = np.ones((kx, ky), np.float32) / (kx * ky)  #array of ones
# smoothed = cv2.filter2D(filtered, -1, kernel)
# cv2.imshow('smoothed', smoothed)

bx = by = 5  #doesn't work with even numbers
# blur = cv2.GaussianBlur(filtered, (bx, by), 0)
# cv2.imshow('blur', blur)

m = 7  #doesn't work with even numbers, seems like good choice
median = cv2.medianBlur(filtered, m)
cv2.imshow('median', median)  #solid color

b1 = 75; b2 = b3 = 100  #decent image quality but slow
# bilat = cv2.bilateralFilter(filtered, b1, b2, b2)
# cv2.imshow('bilat', bilat)

#Morphological Transformations
morph_kernel = np.ones((3,3), np.uint8)  #larger the tuple, larger the area for erosion check

# dilation = cv2.dilate(filtered, morph_kernel, iterations=1)  #makes colored parts bigger
# cv2.imshow('dilation', dilation)

# ero_dilat = cv2.erode(dilation, morph_kernel, iterations=1)  #compound (get rid of edges, make insides bigger)
# cv2.imshow('ero_dilat', ero_dilat)

# opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel); cv2.imshow('opening', opening)
# closing = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel); cv2.imshow('closing', closing)

#Edge Detection and Gradients
# lap_dilat = cv2.Laplacian(dilation, cv2.CV_64F); cv2.imshow('Laplacian_dilation', lap_dilat)
# cv2.imshow('sobelx', cv2.Sobel(filtered, cv2.CV_64F, 1, 0, ksize=5))
# cv2.imshow('sobely', cv2.Sobel(filtered, cv2.CV_64F, 0, 1, ksize=5))
edge = 100; edge_img = cv2.Canny(median, edge, edge)
# cv2.imshow('edges', edge_img)

#contours
cont_img, contours = cv2.findContours(edge_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = np.array(contours).reshape((-1,1,2)).astype(np.int32)
cv2.drawContours(img, [contours], -1, (0, 55, 0), 3)
# cv2.imshow('contours', img)

# imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)

contours, hierarchy = cv2.findContours(edge_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('contours', img)

cv2.waitKey(0); cv2.destroyAllWindows()