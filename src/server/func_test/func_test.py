# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : func_test.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""

import cv2
from matplotlib import pyplot as plt
import numpy as np


def show(img):
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.imshow(img)
    fig.show()


def search_rect():
    img = cv2.imread('E:\\test\\5.jpg')
    # img = cv2.imread('E:\\PaulCoding\\1.6-morphology_auth\\test\\qrcode.jpg')
    img_rotate = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_rotate = cv2.threshold(img_rotate, 90, 255, cv2.THRESH_TOZERO_INV)
    img_rotate = cv2.GaussianBlur(img_rotate, (5, 5), 0)
    img_fc, contours, hierarchy = cv2.findContours(img_rotate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        if w < 50 or h < 50:
            continue
        print(x, y, w, h)
        if 600 < w < 1000:
            box = cv2.minAreaRect(contours[i])
            center = (int(box[0][0]), int(box[0][1]))
            matrix = cv2.getRotationMatrix2D(center, box[2], 1.0)
            draw_img = cv2.warpAffine(img, matrix, img.shape[:2], flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            break
    else:
        draw_img = img.copy()
    img_cut = cv2.cvtColor(draw_img, cv2.COLOR_BGR2GRAY)
    _, img_cut = cv2.threshold(img_cut, 90, 255, cv2.THRESH_TOZERO_INV)
    img_cut = cv2.GaussianBlur(img_cut, (5, 5), 0)
    img_fc, contours, hierarchy = cv2.findContours(img_cut, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        if w < 50 or h < 50:
            continue
        # cv2.rectangle(draw_img, (x, y), (x + w, y + h), (255, 0, 0), 5)
        print(x, y, w, h)
        if -20 < w - h < 20 and 600 < w < 1000:
            break
    else:
        show(draw_img)
        print("not fount")
        return
    show(draw_img)
    new_image = draw_img[y - 5: y + h + 5, x - 5: x + w + 5]
    # new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    # _, new_img_br = cv2.threshold(new_image, 90, 255, cv2.THRESH_TOZERO)
    # _, new_img_br = cv2.threshold(new_img_br, 135, 255, cv2.THRESH_TOZERO_INV)
    show(new_image)
    cv2.imwrite("E:\\\\test\\post.jpg", new_image)


# search_rect()

# import tensorflow as tf
#
# gpu_device_name = tf.test.gpu_device_name()
# print(gpu_device_name)

import mysqlx

mysqlx.connection()


if __name__ == '__main__':
    print("func_test start")
