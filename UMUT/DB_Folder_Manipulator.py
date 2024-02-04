import os
import re
import cv2
import shutil
import matplotlib.pyplot as plt
import sys

sys.path.insert(0, './Ali')
import detect_distences_of_sides
import detectFrontelImageFromTxt

sys.path.insert(0, './UMUT')
import Common
import NameFeatureExtractor
import DBsWithTxtInfo
import FrontalFaceFunctions
import txtFileOperations

def main(dbName, upperFolderName, showFrontalFaceExamples, inputOrAutoMod, printFeaturesFlag):    
    #This is the folder path of the logs
    logFolderPath = f'./{upperFolderName}/LOG/{dbName}'
    os.makedirs(logFolderPath, exist_ok=True)
    Common.clearLogs(logFolderPath)

    # This is very important for the txt operations. 
    #The txt file should be in the same folder with the images and the name of the txt file should be the same with the name of the folder
    txtInfoPath = f'./{upperFolderName}/{dbName}.txt' 
    
    print(txtFileOperations.initMainTxtFile(dbName,upperFolderName,
                                            ["file_path","left_eye","right_eye","nose","mouth_left","mouth_right","facial_area"]))
    
    #These variables will be automatically changed according to the number of features
    file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index = 0, 0, 0, 0 

    imgTxtDBs = False
    if dbName == 'YoutubeFace' or dbName == 'LFW':
        imgTxtDBs = True
    #------------------------------------------------------- Main Part -------------------------------------------------------#
    
    files = os.scandir('./'+ upperFolderName +'/'+ dbName)
    firstFlag = True;makeDeceisonFlag = True

    holdID = 0;holdLeftInnerID = 0;holdFeaturesLen = 0;frontalCount = 0;
    
    plt.figure(figsize=(20,10))

    #Txt operations for YoutubeFace and LFW
    if imgTxtDBs ==True:
        imageInformationsTxt = open(txtInfoPath, 'r') # change this
        imageInformations = imageInformationsTxt.readlines()
        imageInformations = Common.replaceEntersAndTabs(imageInformations)
        files = DBsWithTxtInfo.imgTxtDBsFilesConcat(files)

    indexDict = {
        "file_id_index": file_id_index,
        "inner_id_right_side_index": inner_id_right_side_index,
        "inner_id_left_side_index": inner_id_left_side_index,
        "learnType_index": learnType_index
    }

    #Iterate through the files
    for index,file in enumerate(files):
        if imgTxtDBs == True:
            output_file_name = imageInformations[index]+'.jpg'
            if index%1000 == 0:
                print("Image Counter: " + str(index))
        else:
            output_file_name = file.name
        
        #Extract features from file name
        features,indexDict,makeDeceisonFlag = NameFeatureExtractor.extractFeaturesFromFileName(output_file_name, indexDict, inputOrAutoMod, makeDeceisonFlag, printFeaturesFlag)    
        numberOfSlices = features["numberOfSlices"]
        #When number of slices changed, we should extract features again
        if numberOfSlices != holdFeaturesLen and firstFlag == False:
            print("Number of features changed! Please check the features!")
            if inputOrAutoMod == False:
                input("Press Enter to continue...")
            makeDeceisonFlag = True
            features,indexDict,makeDeceisonFlag = NameFeatureExtractor.extractFeaturesFromFileName(output_file_name, indexDict, inputOrAutoMod, makeDeceisonFlag, printFeaturesFlag)
        holdFeaturesLen = numberOfSlices
        
        inner_id_right_side = features["inner_id_right_side"]
        inner_id_left_side = features["inner_id_left_side"]
        extension = features["extension"]
        learnType = features["learnType"]
        file_id = features["file_id"]

        #If the fileID or inner_id_left_side is different than the previous one, we should detect the frontal face of the previous folder
        if ( holdID != file_id or holdLeftInnerID != inner_id_left_side ) and firstFlag == False:
            os.makedirs(output_folder + "frontal/", exist_ok=True);os.makedirs(output_folder, exist_ok=True)
            
            confidence,image_cv2 = detectFrontelImageFromTxt.run(output_folder)
            FrontalFaceFunctions.showFrontalFaces(image_cv2, confidence, frontalCount,showFrontalFaceExamples)
            
            if image_cv2 == False:
                Common.writeLog( logFolderPath +'/logNoFrontalFace.txt', output_file_name)
            else:
                if len(os.listdir(output_folder+'frontal/')) > 0:
                    print("Frontal Image Already Exists!")
                else:
                    bestImageFilePath = output_folder + image_cv2 + ".jpg"
                    frontalCount += 1
                    Common.copyFile(bestImageFilePath, output_folder + "frontal/" + image_cv2 + ".jpg")
                    os.makedirs('./' + upperFolderName + '/' + dbName + '_FOLDERED/Frontal_Faces/', exist_ok=True)
                    Common.copyFile( bestImageFilePath, "./" + upperFolderName + "/" + dbName + "_FOLDERED/Frontal_Faces/" + image_cv2 + ".jpg")
                    Common.writeLog( logFolderPath +'/logAddedFrontalImage.txt', bestImageFilePath)
                         
        firstFlag = False
        holdID = file_id
        holdLeftInnerID = inner_id_left_side
            
        
        # In this part, you can change the output folder structure according to your needs
        # If learnType is True-> output_folder = f'./{upperFolderName}/{dbName}_FOLDERED/{learnType}/{file_id}/'
        output_folder = f'./{upperFolderName}/{dbName}_FOLDERED/{learnType + "/" if learnType else ""}{file_id}/'


        # Add inner folder when inner_id_left_side is different than False and inner_id_left_side is a number
        if inner_id_left_side != False and inner_id_left_side.isdigit() == True:
            output_folder = output_folder + inner_id_left_side + '/'
        else:
            output_folder = output_folder + '0' + '/'

        # Create folders if they don't exist / COPY PROCESS
        # Replace the images with same name
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = output_folder + output_file_name

        if imgTxtDBs == True:
            input_file_path = file
        else:
            input_file_path = './' + upperFolderName + '/' + dbName + '/' + output_file_name

        #Here we copy the jpg file to the output folder
        Common.copyFile(input_file_path, output_file_path)

        logString = "Added Image: " + output_file_name
        Common.writeLog(logFolderPath+'/logAddedImage.txt', logString)
        
        #Frontal detection
        if extension == 'jpg':
            # If all of the images was processed, in a folder:
            
            if imgTxtDBs == True:
                input_file_path = file    
            else:
                input_file_path = './' + upperFolderName + '/' + dbName + '/' + output_file_name
            
            #Read the image
            image_cv2 = cv2.imread(input_file_path)
        
            #Calculate the landmarks of the frontal face and write them to the txt file
            response = FrontalFaceFunctions.writeRetinaFaceLandmarks(image_cv2,input_file_path,output_folder,output_file_name,  logFolderPath)#remove output_folder 
            if response != "Txt already exists!":
                Common.writeLog(logFolderPath+'/logAddedTxt.txt', response)
            else:
                Common.writeLog(logFolderPath+'/logTxtExists.txt', output_folder)

if __name__ == "__main__":
    main('YoutubeFace', 'UMUT', False, False, False)