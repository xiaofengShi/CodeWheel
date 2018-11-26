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

""" convert paints to sketch
    PaintsToSketchV4 is now the best

"""

import cv2
import numpy as np
import imageio
import scipy.ndimage
import os
np.seterr(divide='ignore', invalid='ignore')


def PaintsToSketch(img_path):
    image = cv2.imread(img_path)
    # Convert image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Clean up image using Guassian Blur
    img_gray_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    # Extract edges
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    # Do an invert binarize the image
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask


"""
The Dodge blend function divides the bottom layer by the inverted top layer.
This lightens the bottom layer depending on the value of the top layer.
We have the blurred image, which highlights the boldest edges.
"""


def PaintsToSketchV2(img_path):
    # reading the image
    img = cv2.imread(img_path, 1)
    # converting the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # inverting the image
    img_invert = cv2.bitwise_not(img_gray)
    # bluring or smoothing the inverted image with the kernel size (10,10)
    img_blur = cv2.blur(img_invert, (10, 10))

    return cv2.divide(img_gray, 255 - img_blur, scale=256)

def PaintsToSketchV3(img_path):
    img = cv2.imread(img_path)
    # 1
    blur = cv2.GaussianBlur(img, (0, 0), 3)
    image = cv2.addWeighted(img, 1.5, blur, -0.5, 0)
    # 2
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(img, -1, kernel)
    # 3
    image = cv2.bilateralFilter(img, 9, 75, 75)
    # 4
    sigma = 1
    threshold = 5
    amount = 1
    blurred = cv2.GaussianBlur(img, (0, 0), 1, None, 1)
    lowContrastMask = abs(img - blurred) < threshold
    sharpened = img*(1+amount) + blurred*(-amount)
    image = cv2.bitwise_or(sharpened.astype(np.uint8), lowContrastMask.astype(np.uint8))

    return image


def PaintsToSketchV4(img_path):
    img = cv2.imread(img_path)

    gray_img = np.dot(img[..., :3], [0.299, 0.587, 0.114])
    gray_inv_img = 255 - gray_img
    blur_img = cv2.GaussianBlur(gray_inv_img, (5, 5), 0)
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Clean up image using Guassian Blur
    img_gray_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    # Extract edges
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    # blur_img = scipy.ndimage.filters.gaussian_filter(gray_inv_img, sigma=2)
    # Do an invert binarize the image
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)

    def dodge(front, back):
        result = front*255/(255-back)
        result[np.logical_or(result > 255, back == 255)] = 255
        return result.astype('uint8')

    final_img = dodge(blur_img, gray_img)

    # h, w = final_img.shape
    # src2 = 255*np.ones([h, w], img.dtype)
    contrast = 0.6
    brightenss = 0
    img_contrast_brightness = cv2.addWeighted(final_img, contrast, mask, 1-contrast, brightenss)

    # gauss
    # img_gray_blur = cv2.GaussianBlur(final_img, (5, 5), 0)
    # cv2.imwrite('gauss.jpg',img_gray_blur)
    # canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    # ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)

    return img_contrast_brightness






# img_path = './img/3_PaintsToSketch_in2.jpg'

# sketch = PaintsToSketch(img_path)
# cv2.imwrite('./img/3_PaintsToSketch_done_V1.jpg', sketch)

# sketchV2 = PaintsToSketchV2(img_path)
# cv2.imwrite('./img/3_PaintsToSketch_done_v2.jpg', sketchV2)

# sketchV3 = PaintsToSketchV3(img_path)
# cv2.imwrite('./img/3_PaintsToSketch_done_v3.jpg', sketchV3)

def main():
    img_dir = '/Users/xiaofeng/Desktop/0002_c'
    save_dir = '/Users/xiaofeng/Desktop/0003_c'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_list = [os.path.join(img_dir,i) for i in os.listdir(img_dir)]
    for img_path in file_list:
        file_name = os.path.basename(img_path)
        save = os.path.join(save_dir, file_name)
        print('save: ',save)
        sketchV4 = PaintsToSketchV4(img_path)
        cv2.imwrite(save, sketchV4)


if __name__ == '__main__':
    main()
