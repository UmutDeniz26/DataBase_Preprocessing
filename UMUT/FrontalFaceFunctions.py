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


#This function will write the landmarks of the frontal face to the txt file
#It will also return the modified confidenceArray
def writeRetinaFaceLandmarks(image_cv2, img_path, txt_path, txt_name, logFolderPath,inter,intra,imgCounter):
    txt_path = txt_path+txt_name
    txt_path = os.path.splitext(txt_path)[0]# it gives extensionless path
    txt_path = txt_path + '.txt'

    if os.path.exists(txt_path):
        resp = txtFileOperations.readJsonDictFromFile(txt_path)
        txtFileOperations.writeFileMainTxt(txt_path, resp,inter,intra)
        #This part is for testing the face alignment
        imgCounter = plot_aligned_faces(image_cv2, resp,intra,imgCounter)
        return "Txt already exists!", imgCounter
    
    #insert resp from extract faces
    #resp = detect_distences_of_sides.detect_best_frontal_face(img_path)

    print(txtFileOperations.writeFileMainTxt(txt_path, resp,inter,intra))
    print(txtFileOperations.run(txt_path, resp))
    return "Added txt: " + txt_path + " successfully!", imgCounter

def plot_aligned_faces(image_cv2, resp,intra,imgCounter):
    if intra%5 == 0 and 0<=imgCounter<21:    
        imgCounter+=1
        # Don't use last element of the landmarks which is 'facial_area'
        # Convert dictionary values to np.array
        landmarks = list(resp.values());landmarks = landmarks[0:-1];landmarks = np.array(landmarks)

        # Test face alignment
        image = face_align_landmark(image_cv2, landmarks)
        plt.subplot(4,5, imgCounter);plt.imshow(image);plt.title(imgCounter)
        plt.axis('off')
    
    if imgCounter == 20:
        imgCounter = -1
        plt.show()

    return imgCounter

