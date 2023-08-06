#!/usr/bin/env python

import cv2
import os 
from typing import List 
import pathlib


IMG_PATH = os.path.join(pathlib.Path(__file__).parent, "img.jpg")


class Processor:
    def __init__(self, image):
        self.image = cv2.imread(image)
        
    def extract(self, start_y, end_y, start_x, end_x, name):
        """
        extract pixel for size, ROI (region of interest)

        Args:
            start_y (int): pos_y_start
            end_y (int): pos_y_end
            start_x (int): pos_x_start
            end_x (int): pos_x_end
            name (str): extracted image file name
        """
        (height, width, dims) = self.image.shape
        print(height, width, dims)
        roi = self.image[start_y: end_y, start_x: end_x]
        cv2.imshow(name, roi)
        return cv2.waitKey(0)
    
    
    def resize(self, expected_width, name):
        """
        based on aspect ratio, change the height based on the weight we define, so image won't squished.

        Args:
            expected_width (int): expected resized width
            name (str): resized image file name
        """
        (height, width, dims) = self.image.shape
        # print(height, width, dims)
        ratio = expected_width/ width
        dim = (expected_width, int(height * ratio))
        # interpolation=cv2.INTER_AREA
        resized = cv2.resize(self.image, dim)
        cv2.imshow(name, resized)
        return cv2.waitKey(0)
    
    
    def rotate(self, angle, name, scale = 1.0):
        """
        change image display degree. 

        Args:
            angle (int): rotate angle in degrees, such as 45, 60, 90 ...
            name (str): rotated image file name
        """
        
        (height, width, dims) = self.image.shape
        center = (width // 2, height // 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(self.image, M, (width, height))
        cv2.imshow(name, rotated)
        return cv2.waitKey(0)
    
    
    # TODO
    def draw_boundingbox(self):
        pass 
    


if __name__ == "__main__":
    
    IMG_PATH = os.path.join(pathlib.Path(__file__).parent, "img.jpg")
    img = Processor(IMG_PATH)
    img.resize(1000, "roi.jpg")
    img.extract(1800, 2800, 2000, 3000, "extracted.jpg")
    img.rotate(60, "rotated.jpg")
    