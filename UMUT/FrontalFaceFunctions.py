import sys
sys.path.insert(0, './Ali')
sys.path.insert(0, './UMUT')


import cv2
import os
import Common
import txtFileOperations
import matplotlib.pyplot as plt
import detect_distences_of_sides
from retinaface import RetinaFace

from skimage import transform as tform
from skimage import transform
import numpy as np

number_of_plot_images = 20
plt.figure(figsize=(20, 20))

#This function will write the landmarks of the frontal face to the txt file
#It will also return the modified confidenceArray
def writeRetinaFaceLandmarks(image_cv2, output_file_path ,inter ,intra):

    # Output file path should be a txt file, this line will change the extension to txt
    output_file_path = os.path.splitext(output_file_path)[0] + '.txt'

    if os.path.exists(output_file_path):
        landmarks = txtFileOperations.readJsonDictFromFile(output_file_path)
        txtFileOperations.writeFileMainTxt(output_file_path, landmarks, inter, intra)
        #This part is for testing the face alignment
        plot_aligned_faces(image_cv2, intra)
        return "Txt already exists!"
    else:
        #insert resp from extract faces
        #resp = detect_distences_of_sides.detect_best_frontal_face(img_path)
        txtFileOperations.writeFileMainTxt(output_file_path, {"Response": False},inter,intra)
        txtFileOperations.writeLandmarksTxtFile(output_file_path, {"Response": False})

        return "Txt file successfully written! : " + output_file_path


def plot_aligned_faces(image_cv2 ,intra):
    global number_of_plot_images
    if intra%5 == 0 and 0 < number_of_plot_images:
        number_of_plot_images-=1
        plt.subplot( 5, 4, number_of_plot_images )
        plt.imshow(image_cv2)
        plt.title('intra: ' + str(intra))
        plt.axis('off')
    if number_of_plot_images == 0:
        number_of_plot_images -= 1
        plt.show()
