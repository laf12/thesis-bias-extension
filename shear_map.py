# Goal of this script: create a shear map from a set of pictures and shear values

import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def get_contour_image(path):

    # Load the pictures in the folder
    img1 = cv2.imread(path,0)

    # show the pictures
    # plt.imshow(img1, cmap = 'gray')
    # plt.show()

    # invert the pictures
    img1 = 255 - img1

    # get a contour of the picture
    ret, cnt = cv2.threshold(img1, 200, 230, 0)
    # show the thresholded image
    # plt.imshow(cnt, cmap = 'gray')
    # plt.show()

    cnt, contours = cv2.findContours(cnt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # create an empty image with the same dimensions as the original image
    cnt_img = np.zeros_like(img1)

    # draw the contour onto the image
    if len(contours) > 0:
        cv2.drawContours(cnt_img, cnt, contourIdx=-1, color=255, thickness=1)

    return cnt_img


def main():
    # for each picture in the folder, get the contour image and save it in a new folder
    input_folder_path = "modified"
    output_folder_path = "contour"

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".tif"):
            path = os.path.join(input_folder_path, filename)
            cnt_img = get_contour_image(path)
            cv2.imwrite(os.path.join(output_folder_path, filename), cnt_img)

def view_contour_image(path):
    # Load the pictures in the folder
    img1 = cv2.imread(path,0)

    # show the pictures
    plt.imshow(img1, cmap = 'gray')
    plt.show()
    

if __name__ == "__main__":
    # main()
    for filename in os.listdir("contour"):
        if filename.endswith(".tif"):
            path = os.path.join("contour", filename)
            view_contour_image(path)
    