import sys
sys.path.insert(0, './Ali')
sys.path.insert(0, './UMUT')
import cv2
import os
import shutil
import Common
import writeToTxt
import matplotlib.pyplot as plt
import detect_distences_of_sides
import writeToTxt


def FaceRecogFrontalHandle(image_cv2_yunet, img_path, confidenceArray, txt_path, txt_name):
    txt_path = txt_path+txt_name
    txt_path = os.path.splitext(txt_path)[0]# it gives extensionless path
    txt_path = txt_path + '.txt'

    if os.path.exists(txt_path):
        return confidenceArray
    
    resp = detect_distences_of_sides.detect_best_frontal_face(img_path)
    if resp == False:   # IF face is not detected
        return confidenceArray
    confidence = resp["difference_between_le_re"]
    confidenceArray.append({'confidence': confidence, 'img': image_cv2_yunet})

    writeToTxt.run(txt_path, resp)

    return confidenceArray

def showFrontalFaces(image, confidence, frontalCount,showFrontalFaceExamples):
    if frontalCount<40 and showFrontalFaceExamples:
        plt.subplot(4,10,frontalCount)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(str(round(float(confidence),2)))
        plt.axis('off')
    elif frontalCount == 40 and showFrontalFaceExamples:
        plt.show()    

#This function will write the frontal face to the folder
def writeFrontalFaceToFolder(confidence, frontalCount, destination, file_name_withoutExtension, extension, file_id, logFolderPath, out_file_name, imgTxtDBs, dbName, file):    
    os.makedirs( destination + 'frontal/', exist_ok=True)
    output_file_path_frontal = destination + 'frontal/' + file_name_withoutExtension + '.' + extension
    
    if imgTxtDBs == True:
        input_file_path_frontal = file
    else:
        input_file_path_frontal = './' + dbName + '/' + out_file_name

    #print("Frontal input file path: " + input_file_path_frontal)
    shutil.copy(input_file_path_frontal, output_file_path_frontal)

    logString = "Added Frontal Image Count: " + str(frontalCount) + " - " + str(file_id)+ " - " + str(confidence) + " - " + out_file_name
    
    Common.writeLog( logFolderPath+'/logFrontalFaceAdded.txt', logString)
