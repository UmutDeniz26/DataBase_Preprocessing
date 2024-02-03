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
import writeToTxt
import Common
import NameFeatureExtractor
import DBsWithTxtInfo
import FrontalFaceFunctions
logFolderPath = ""

def main(dbName, upperFolderName, showFrontalFaceExamples, isThereTrainTest, inputOrAutoMod):
    global logFolderPath
    logFolderPath = f'./{upperFolderName}/LOG/{dbName}'
    txtInfoPath = f'./{upperFolderName}/{dbName}DB.txt'
    dbName = './'+upperFolderName+'/'+dbName
     
    #These variables will be automatically changed according to the number of features
    file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index= 0, 0, 0, 0 

    #This variable will be automatically changed according to the number of features
    copyFlag = False

    print("DB Name: " + dbName)
    if dbName == './'+upperFolderName+'/YoutubeFace' or dbName == './'+upperFolderName+'/LFW':
        imgTxtDBs = True
    else:
        imgTxtDBs = False

    ##########################   MAIN   #############################
    files = os.scandir('./'+dbName)
    firstFlag = True;makeDeceisonFlag = True
    imageCounter = 0 # only for imgTxtDBs
    holdID = 0;holdFeaturesLen = 0;frontalCount = 0;holdLeftInnerID = 0;
    plt.figure(figsize=(20,10))

    Common.clearLogs(logFolderPath)
    os.makedirs(logFolderPath, exist_ok=True)

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

    #example ->AFW_815038_1_12.jpg
    for file in files:
        if imgTxtDBs == True:
            out_file_name = imageInformations[imageCounter]+'.jpg'
            imageCounter += 1
            if imageCounter%1000 == 0:
                print("Image Counter: " + str(imageCounter))
        else:
            out_file_name = file.name
        
        features,indexDict,makeDeceisonFlag = NameFeatureExtractor.extractFeaturesFromFileName(out_file_name, indexDict, inputOrAutoMod, makeDeceisonFlag)    
        numberOfSlices = features["numberOfSlices"]

        #When number of slices changed, we should extract features again
        if numberOfSlices != holdFeaturesLen and firstFlag == False:
            print("Number of features changed! Please check the features!")
            if inputOrAutoMod == False:
                input("Press Enter to continue...")
            makeDeceisonFlag = True
            features,indexDict,makeDeceisonFlag = NameFeatureExtractor.extractFeaturesFromFileName(out_file_name, indexDict, inputOrAutoMod, makeDeceisonFlag)
        
        
        file_id_index = indexDict["file_id_index"]
        inner_id_right_side_index = indexDict["inner_id_right_side_index"]
        inner_id_left_side_index = indexDict["inner_id_left_side_index"]
        learnType_index = indexDict["learnType_index"]

        inner_id_right_side = features["inner_id_right_side"]
        inner_id_left_side = features["inner_id_left_side"]
        extension = features["extension"]
        learnType = features["learnType"]
        file_id = features["file_id"]

        holdFeaturesLen = numberOfSlices
        
        # This part is important for the output folder structure
        # In this part, you can change the output folder structure according to your needs
        if learnType == False:
            output_folder = './' + dbName + '_FOLDERED/' + file_id + '/'
        else:
            output_folder = './' + dbName + '_FOLDERED/' + learnType + '/' + file_id + '/'
        
        
        if inner_id_left_side != False and inner_id_left_side.isdigit() == True:
            output_folder = output_folder + inner_id_left_side + '/'

        # Create folders if they don't exist / COPY PROCESS
        # If len of files in output folder is less than 10, copy the file
        if copyFlag == False:
            try:
                if len(os.listdir(output_folder)) < 10 or copyFlag == True:
                    copyFlag = True
            # If folder does not exist, create folder and copy the file
            except:
                copyFlag = True
                print("Folder does not exist, creating folder: " + output_folder)     
        else:
            os.makedirs(output_folder, exist_ok=True)
            output_file_path = output_folder + out_file_name

            if imgTxtDBs == True:
                input_file_path = file
                #print("Input File Path: " + input_file_path)
            else:
                input_file_path = './' + dbName + '/' + out_file_name


            #copy input filepath to output filepath
            #print("Copying: " + input_file_path + " to " + output_file_path)

            #Here we copy the jpg file to the output folder
            shutil.copy(input_file_path, output_file_path)

            logString = "Added Image: " + out_file_name
            Common.writeLog(logFolderPath+'/logAddedImage.txt', logString)
        
        #Frontal detection
        if extension == 'jpg':
            # If all of the images was processed, in a folder:
            
            if ( holdID != file_id or holdLeftInnerID != inner_id_left_side ) and firstFlag == False:
                os.makedirs(output_folder + "frontal/", exist_ok=True)
                os.makedirs(output_folder, exist_ok=True)
                confidence,image_cv2 = detectFrontelImageFromTxt.run(output_folder)
                FrontalFaceFunctions.showFrontalFaces(image_cv2, confidence, frontalCount,showFrontalFaceExamples)
                if image_cv2 == False:
                    Common.writeLog( logFolderPath +'/logNoFrontalFace.txt', out_file_name)
                else:
                    if len(os.listdir(output_folder+'frontal/')) > 0:
                        print("Frontal Image Already Exists!")
                        Common.writeLog( logFolderPath +'/logFrontalExists.txt', out_file_name)
                    else:
                        bestImageFilePath = output_folder + image_cv2 + ".jpg"
                        print("Best Image File Path: " + bestImageFilePath)
                        frontalCount += 1
                        shutil.copy(bestImageFilePath, output_folder + "frontal/" + image_cv2 + ".jpg")
                        print(len(os.listdir(output_folder+'frontal/')))
                                      
            firstFlag = False
            holdID = file_id
            holdLeftInnerID = inner_id_left_side
            
            if imgTxtDBs == True:
                input_file_path = file    
            else:
                input_file_path = './' + dbName + '/' + out_file_name
            
            #Read the image
            image_cv2 = cv2.imread(input_file_path)
        
            #Calculate the landmarks of the frontal face and write them to the txt file
            response = FrontalFaceFunctions.writeRetinaFaceLandmarks(image_cv2,input_file_path,output_folder,out_file_name)#remove output_folder 
            if response != "Txt already exists!":
                Common.writeLog(logFolderPath+'/logAddedTxt.txt', response)
            else:
                Common.writeLog(logFolderPath+'/logTxtExists.txt', response)

if __name__ == "__main__":
    main('YoutubeFace', 'UMUT', False, False, False)