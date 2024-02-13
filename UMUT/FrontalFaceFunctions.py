import sys
sys.path.insert(0, './Ali')
sys.path.insert(0, './UMUT')


import cv2
import os
import Common
import txtFileOperations
#import matplotlib.pyplot as plt
import detect_distences_of_sides

from skimage import transform as tform
from skimage import transform
import numpy as np

number_of_plot_images = 20
#plt.figure(figsize=(20, 20))

#This function will write the landmarks of the frontal face to the txt file
#It will also return the modified confidenceArray
def writeRetinaFaceLandmarks(image_cv2, output_file_path ,inter ,intra, show_aligned_images, landmarks_input = {"Response":False}):

    # Output file path should be a txt file, this line will change the extension to txt
    output_file_path = os.path.splitext(output_file_path)[0] + '.txt'
    plot_aligned_faces(image_cv2, intra,show_aligned_images)

    if os.path.exists(output_file_path):
        txtFileOperations.writeFileMainTxt(output_file_path, landmarks_input, inter, intra)
        txtFileOperations.writeLandmarksTxtFile(output_file_path, landmarks_input)
        #This part is for testing the face alignment
        return "Txt already exists!"
    else:
        #insert resp from extract faces
        #resp = detect_distences_of_sides.detect_best_frontal_face(img_path)
        txtFileOperations.writeFileMainTxt(output_file_path, landmarks_input, inter, intra)
        txtFileOperations.writeLandmarksTxtFile(output_file_path, landmarks_input)
        return "Txt file successfully written! : " + output_file_path


def plot_aligned_faces(image_cv2 ,intra, show_aligned_images):
    if show_aligned_images:
        global number_of_plot_images
        print("number_of_plot_images: ", number_of_plot_images)
        if number_of_plot_images == 0:
            number_of_plot_images -= 1
            #plt.show()
        elif intra%20 == 0 and 0 < number_of_plot_images:
            #plt.subplot( 5, 4, number_of_plot_images )
            #plt.imshow(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
            #plt.title('intra: ' + str(intra))
            #plt.axis('off')
            number_of_plot_images-=1
