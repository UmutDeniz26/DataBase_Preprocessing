import sys
sys.path.insert(0, './Ali')
sys.path.insert(0, './UMUT')
import cv2
import os
import Common
import txtFileOperations
import matplotlib.pyplot as plt
import detect_distences_of_sides


#This function will write the landmarks of the frontal face to the txt file
#It will also return the modified confidenceArray
def writeRetinaFaceLandmarks(image_cv2, img_path, txt_path, txt_name, logFolderPath):
    txt_path = txt_path+txt_name
    txt_path = os.path.splitext(txt_path)[0]# it gives extensionless path
    txt_path = txt_path + '.txt'

    if os.path.exists(txt_path):
        resp = txtFileOperations.readJsonDictFromFile(txt_path)
        txtFileOperations.writeFileMainTxt(txt_path, resp)
        return "Txt already exists!"
    
    
    resp = detect_distences_of_sides.detect_best_frontal_face(img_path)
    print(txtFileOperations.writeFileMainTxt(txt_path, resp))
    print(txtFileOperations.run(txt_path, resp))
    return "Added txt: " + txt_path + " successfully!"

def showFrontalFaces(image, confidence, frontalCount,showFrontalFaceExamples):
    if frontalCount<40 and showFrontalFaceExamples:
        plt.subplot(4,10,frontalCount)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(str(round(float(confidence),2)))
        plt.axis('off')
    elif frontalCount == 40 and showFrontalFaceExamples:
        plt.show()    
