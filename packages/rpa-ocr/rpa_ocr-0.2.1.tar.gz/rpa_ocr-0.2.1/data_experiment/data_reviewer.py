# -*- coding:utf-8 -*-
# @author :adolf
import cv2
import os

import matplotlib.pyplot as plt
from PIL import Image

image_file_path = "/home/shizai/adolf/data/xiaozhang/"
img_list = os.listdir(image_file_path)
img_list = list(sorted(img_list))
img_name = img_list[int(1651 * 2 + 1)]
# print(img_name)
img = cv2.imread(os.path.join(image_file_path, img_name))
img2 = Image.open(os.path.join(image_file_path, img_name))
plt.imshow(img)
plt.show()

plt.imshow(img2)
plt.show()
# print(img.shape)
# for img_name in img_list:
#     img = cv2.imread(os.path.join(image_file_path,img_name))
#     if img.shape != (90, 200, 3):
#         print(img_name)
#         print(img.shape)

# print(img.shape)
# print(img_list[int(1651*2)])
for image_name in img_list:
    img_n = image_name.split('.')[0]
    if len(img_n) != 4:
        img_n = img_n.replace(' (2)', '')
        if len(img_n) != 4:
            print(img_n)
            print(len(img_n))
