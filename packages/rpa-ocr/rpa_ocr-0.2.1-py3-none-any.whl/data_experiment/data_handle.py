# -*- coding:utf-8 -*-
# @author :adolf
import os
import cv2

image_file_path = "/home/shizai/adolf/data/1862/"
img_list = os.listdir(image_file_path)

image_save_path = "/home/shizai/adolf/data/"

for img_name in img_list:
    # print(img_name)
    new_img_name = img_name.split('_')[1]
    # print(new_img_name)
    img = cv2.imread(os.path.join(image_file_path, img_name))
    cv2.imwrite(os.path.join(image_save_path, new_img_name), img)
    # break
