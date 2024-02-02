import os
import re
import cv2
import shutil
import matplotlib.pyplot as plt


import sys

sys.path.insert(0, './Ali')
import detect_distences_of_sides

sys.path.insert(0, './UMUT')
import writeToTxt
import Common
import NameFeatureExtractor
import DBsWithTxtInfo
import FrontalFaceFunctions


def main(dbName='YoutubeFace', logFolderPath='./UMUT/LOG/YoutubeFace', txtInfoPath='./UMUT/youtubeFaceDB.txt', showFrontalFaceExamples=False, isThereTrainTest=False, inputOrAutoMod=False, upperFolderName='UMUT'):
    
    dbName = './'+upperFolderName+'/'+dbName
    print("DB Name: " + dbName)
    print("Log Folder Path: " + logFolderPath)
    print("Txt Info Path: " + txtInfoPath)
    print("Show Frontal Face Examples: " + str(showFrontalFaceExamples))
    print("Is There Train Test: " + str(isThereTrainTest))
    print("Input Or Auto Mod: " + str(inputOrAutoMod))
    print("Upper Folder Name: " + upperFolderName)
    

    """
    #Change these
    dbName = 'YoutubeFace' #IBUG, LFPW, HELEN, AFW, IBUG, YoutubeFace, LFW
    logFolderPath = './UMUT/LOG/'+ dbName
    txtInfoPath = './UMUT/youtubeFaceDB.txt' #only for imgTxtDBs
    showFrontalFaceExamples = False #True for show, False for not show
    isThereTrainTest = False #True for LFPW Dataset, False for anothers
    #It doesnt work properly right now!!!
    inputOrAutoMod = False #True for auto, False for input, auto mod is only for IBUG Dataset. If you want to use auto mod, you should change the function autoDetermineAccordingToFeatureCount
    """

    #Global Variables for decideWhichElementsWhichFeatures
    file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index= 0, 0, 0, 0 

    #This variable will be automatically changed according to the number of features
    copyFlag = False

    print("DB Name: " + dbName)
    if dbName == './'+upperFolderName+'/YoutubeFace' or dbName == './'+upperFolderName+'/LFW':
        imgTxtDBs = True
    else:
        imgTxtDBs = False

    ##########################   MAIN   #############################
    plt.figure(figsize=(20,10))
    files = os.scandir('./'+dbName)
    confidenceArray = []
    firstFlag = True;makeDeceisonFlag = True
    imageCounter = 0 # only for imgTxtDBs
    holdID = 0;holdFeaturesLen = 0;frontalCount = 0

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

        file_name_withoutExtension = features["file_name_withoutExtension"]
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


            #print("Output File Path: " + output_file_path)
            #copy input filepath to output filepath
            #print("Copying: " + input_file_path + " to " + output_file_path)
            shutil.copy(input_file_path, output_file_path)

            logString = "Added Image: " + out_file_name
            Common.writeLog(logFolderPath+'/logAddedImage.txt', logString)
        
        #Frontal detection
        if extension == 'jpg':
            if holdID != file_id and firstFlag == False:
                image_cv2, confidence = FrontalFaceFunctions.findMaxFrontalFace(confidenceArray,logFolderPath,out_file_name)
                confidenceArray.clear()
                frontalCount += 1

                if  confidence != False:    
                    FrontalFaceFunctions.showFrontalFaces(image_cv2, confidence, frontalCount,showFrontalFaceExamples)
                    #Our frontal image is ready
                    #create a folder that named frontal, and copy this into
                    FrontalFaceFunctions.writeFrontalFaceToFolder(confidence, frontalCount, output_folder, 
                                                                file_name_withoutExtension, extension, file_id, logFolderPath, 
                                                                out_file_name, imgTxtDBs, dbName, file)
            firstFlag = False
            holdID = file_id
            
            if imgTxtDBs == True:
                input_file_path = file    
            else:
                input_file_path = './' + dbName + '/' + out_file_name
            
            image_cv2 = cv2.imread(input_file_path)
            
            confidenceArray = FrontalFaceFunctions.FaceRecogFrontalHandle(image_cv2,input_file_path,confidenceArray,output_folder,out_file_name)#remove output_folder 
            #print("Length of confidence array: " + str(len(confidenceArray)))
            #_, faces = yunetDetectionDNN(image_cv2,input_file_path,confidenceArray,output_folder,out_file_name) #remove output_folder
            #DNNFrontalHandle(faces, image_cv2)


if __name__ == "__main__":
    main()