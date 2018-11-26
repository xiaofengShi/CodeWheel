'''
File: 2_PaintToSketch.py
Project: image_related
File Created: Saturday, 20th October 2018 3:12:22 pm
Author: xiaofeng (sxf1052566766@163.com)
-----
Last Modified: Saturday, 20th October 2018 3:12:55 pm
Modified By: xiaofeng (sxf1052566766@163.com>)
-----
Copyright 2018.06 - 2018 onion Math, onion Math
'''

""" Get img from camera and convert it to sketch """

import cv2
import numpy as np



def CameraToSketch(image):
    # Convert image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Clean up image using Guassian Blur
    img_gray_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    # Extract edges
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    # Do an invert binarize the image
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask

# Initialize webcam, cap is the object provided by VideoCapture
# It contains a boolean indicating if it was sucessful (ret)
# It also contains the images collected from the webcam (frame)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('Our Live Sketcher', CameraToSketch(frame))
    if cv2.waitKey(1) == 13:  # 13 is the Enter Key
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
