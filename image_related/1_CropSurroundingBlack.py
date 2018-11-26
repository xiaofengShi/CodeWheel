
'''
File: crop_img.py
Project: sketchKeras
File Created: Thursday, 18th October 2018 7:31:16 pm
Author: xiaofeng (sxf1052566766@163.com)
-----
Last Modified: Friday, 19th October 2018 5:32:45 pm
Modified By: xiaofeng (sxf1052566766@163.com>)
-----
Copyright 2018.06 - 2018 onion Math, onion Math
'''

import cv2
import os


file_list = []


def CropSurroundingBlack(read_file):
    image_ori = cv2.imread(read_file)
    # one channel
    image = cv2.imread(read_file, 0)
    # thresh the iamge
    # the pixel higher than the setting threshold it will be the maxval
    ret, thresh_img = cv2.threshold(image, 15, 255, cv2.THRESH_BINARY)  
    del image
    # thresh_img=cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
    input_width, input_height = thresh_img.shape
    edges_x = []
    edges_y = []
    for i in range(input_width):
        for j in range(input_height):
            if thresh_img[i][j] == 255:
                edges_x.append(i)
                edges_y.append(j)
    if edges_x:
        left = min(edges_x)  
        right = max(edges_x)  
    else:
        left = 0
        right = input_width
    width = right - left  

    if edges_y:
        bottom = min(edges_y)  
        top = max(edges_y) 
    else:
        bottom = 0
        top = input_height
    height = top-bottom  

    pre1_picture = image_ori[left:left+width, bottom:bottom+height, :]  
    cropshape = pre1_picture.shape
    return pre1_picture

# Test the function
read_file = './img/1_CropSurroundingBlack.jpg'
croped_img = CropSurroundingBlack(read_file)
cv2.imwrite('./img/1_CropSurroundingBlack_done.jpg',croped_img)
