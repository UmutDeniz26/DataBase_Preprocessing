import os
import re
import cv2
import sys
import shutil
import matplotlib.pyplot as plt
from retinaface import RetinaFace

# Custom scripts
import Common
import DBsWithTxtInfo
import txtFileOperations
import NameFeatureExtractor
import FrontalFaceFunctions

sys.path.insert(0, './Ali')
import DetectUpperCase
import detectFrontelImageFromTxt
import detect_distences_of_sides


intra = 0
inter = 0

def main(
        data_base_name, upper_folder_name, align_images_flag, reset_images_flag,
        auto_feature_select=False, print_features_flag=True,
        select_first_image_as_frontal=False,show_aligned_images=False
    ):

    #------------------------------------------------------- Initialization -------------------------------------------------------#
    #This is the folder path of the logs
    log_folder_path = f'./{upper_folder_name}/LOG/{data_base_name}'
    os.makedirs(log_folder_path, exist_ok=True)
    Common.clearLogs(log_folder_path)

    # This is very important for the txt operations.
    #The txt file should be in the same folder with the images and the name of the txt file should be the same with the name of the folder
    txtInfoPath = f'./{upper_folder_name}/{data_base_name}.txt'

    print(txtFileOperations.initMainTxtFile(data_base_name,upper_folder_name,
                                            ["file_path","inter","intra","left_eye","right_eye","nose","mouth_left","mouth_right","facial_area"]))

    #These variables will be automatically changed according to the number of features
    file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index = 0, 0, 0, 0
    resp = []

    imgTxtDBs = False
    if data_base_name == 'YoutubeFace' or data_base_name == 'LFW' or 'CASIA-FaceV5(BMP)':
        imgTxtDBs = True

    if show_aligned_images == True:
        plotimageCounter=0
    else:
        plotimageCounter=-1
    #------------------------------------------------------- Main Part -------------------------------------------------------#
    data_base_folder_path = './'+ upper_folder_name +'/'+ data_base_name

    files = os.scandir(data_base_folder_path)

    if DetectUpperCase.save_second_letter_upper(data_base_folder_path,"uppercase_files.txt") >0:
        print("There are some folders that has two upper case.")
        DetectUpperCase.rename_second_letter_lowercase(data_base_folder_path)
        exit()

    first_iteration = True;make_deceison_flag = True

    hold_id = 0;hold_left_inner_id = 0;holdFeaturesLen = 0;frontalCount = 0

    plt.figure(figsize=(20,10))

    #Txt operations for YoutubeFace and LFW
    if imgTxtDBs ==True:
        imageInformationsTxt = open(txtInfoPath, 'r') # change this
        imageInformations = imageInformationsTxt.readlines()
        imageInformations = Common.replaceEntersAndTabs(imageInformations)
        files = DBsWithTxtInfo.imgTxtDBsFilesConcat(files)

    index_dictionary = {
        "file_id_index": file_id_index,
        "inner_id_right_side_index": inner_id_right_side_index,
        "inner_id_left_side_index": inner_id_left_side_index,
        "learnType_index": learnType_index
    }
    files.sort()

    #Iterate through the files
    for index,file in enumerate(files):
        if imgTxtDBs == True:
            output_file_name = imageInformations[index]+'.jpg'
            input_file_path = file
        else:
            output_file_name = file.name
            input_file_path = './' + upper_folder_name + '/' + data_base_name + '/' + output_file_name


        #Extract features from file name
        features,index_dictionary,make_deceison_flag = NameFeatureExtractor.extractFeaturesFromFileName(output_file_name, index_dictionary, auto_feature_select, make_deceison_flag, print_features_flag)
        numberOfSlices = features["numberOfSlices"]
        #When number of slices changed, we should extract features again
        if numberOfSlices != holdFeaturesLen and first_iteration == False:
            print("Number of features changed! Please check the features!")
            if auto_feature_select == False:
                input("Press Enter to continue...")
            make_deceison_flag = True
            features,index_dictionary,make_deceison_flag = NameFeatureExtractor.extractFeaturesFromFileName(output_file_name, index_dictionary, auto_feature_select, make_deceison_flag, print_features_flag)
        holdFeaturesLen = numberOfSlices

        inner_id_right_side = features["inner_id_right_side"]
        inner_id_left_side = features["inner_id_left_side"]
        extension = features["extension"]
        learnType = features["learnType"]
        file_id = features["file_id"]

        #If the fileID or inner_id_left_side is different than the previous one, we should detect the frontal face of the previous folder
        if ( hold_id != file_id or hold_left_inner_id != inner_id_left_side ) and first_iteration == False:
            global inter
            inter+=1
            os.makedirs(output_folder + "frontal/", exist_ok=True);os.makedirs(output_folder, exist_ok=True)

            confidence_score,image_cv2 = detectFrontelImageFromTxt.run(output_folder)

            # If select_first_image_as_frontal is True, then the first image will be selected as the frontal image
            if select_first_image_as_frontal == True:
                image_cv2_split = image_cv2.split("_")
                image_cv2_split[-1] = "0"
                image_cv2 = "_".join(image_cv2_split)


            if image_cv2 == False:
                Common.writeLog( log_folder_path +'/logNoFrontalFace.txt', output_file_name)
            else:
                if len(os.listdir(output_folder+'frontal/')) > 0:
                    print("Frontal Image Already Exists!")
                    #clear all files in output_folder+frontal/
                    Common.clearFolder(output_folder + "frontal/")

                frontal_image_path = output_folder + image_cv2 + ".jpg"
                frontalCount += 1
                Common.copyFile(frontal_image_path, output_folder + "frontal/" + image_cv2 + ".jpg")
                os.makedirs('./' + upper_folder_name + '/' + data_base_name + '_FOLDERED/Frontal_Faces/', exist_ok=True)
                Common.copyFile( frontal_image_path, "./" + upper_folder_name + "/" + data_base_name + "_FOLDERED/Frontal_Faces/" + image_cv2 + ".jpg")
                Common.writeLog( log_folder_path +'/logAddedFrontalImage.txt', frontal_image_path)

        first_iteration = False
        hold_id = file_id
        hold_left_inner_id = inner_id_left_side


        # In this part, you can change the output folder structure according to your needs
        # If learnType is True-> output_folder = f'./{upper_folder_name}/{data_base_name}_FOLDERED/{learnType}/{file_id}/'
        output_folder = f'./{upper_folder_name}/{data_base_name}_FOLDERED/{learnType + "/" if learnType else ""}{file_id}/'


        # Add inner folder when inner_id_left_side is different than False and inner_id_left_side is a number
        if inner_id_left_side != False and inner_id_left_side.isdigit() == True:
            output_folder = output_folder + inner_id_left_side + '/'
        else:
            output_folder = output_folder + '0' + '/'

        # Create folders if they don't exist / COPY PROCESS
        # Replace the images with same name
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = output_folder + output_file_name

        print(output_file_path)
        #Here we copy the jpg file to the output folder
        if extension != 'mat':
            #aligned_file_path = input_file_path.replace("UMUT", "UMUT/"+data_base_name+"_aligned")
            if reset_images_flag == True or not os.path.exists(output_file_path):
                #Expand face area is a parameter for the retinaface, it is used to expand the face area
                #It is used to include the hair and the ears in the face area !!!
                if align_images_flag == True:
                    try:
                        faces = RetinaFace.extract_faces(input_file_path,align=True,align_first=True)
                    except:
                        faces = [];resp = {}

                    if len(faces) ==0:
                        Common.writeLog(log_folder_path+'/logNoFace.txt', output_file_name)
                        Common.copyFile(input_file_path, output_file_path)
                    else:
                        print("Copying " + input_file_path + " to " + output_file_path)
                        cv2.imwrite(output_file_path, cv2.cvtColor(faces[0], cv2.COLOR_BGR2RGB))
                        #Common.copyFile(aligned_file_path, output_file_path)
                else:
                    resp = {}
                    Common.copyFile(input_file_path, output_file_path)
            else:
                Common.writeLog(log_folder_path+'/logExists.txt', output_file_path)
                if extension == 'jpg':
                    resp = txtFileOperations.readJsonDictFromFile(output_file_path.replace('jpg','txt'))
                if len(resp) == 0:
                    Common.writeLog(log_folder_path+'/logNoFace.txt', output_file_path)

        logString = "Added Image: " + output_file_name
        Common.writeLog(log_folder_path+'/logAddedImage.txt', logString)

        #Frontal detection
        if extension == 'jpg':
            # If all of the images was processed, in a folder:

            if imgTxtDBs == True:
                input_file_path = file
            else:
                input_file_path = './' + upper_folder_name + '/' + data_base_name + '/' + output_file_name

            #Read the image
            image_cv2 = cv2.imread(input_file_path)

            global intra
            #Calculate the landmarks of the frontal face and write them to the txt file
            response = FrontalFaceFunctions.writeRetinaFaceLandmarks(
                                            image_cv2, output_file_path,
                                            inter, intra
                                        )
            intra+=1

            if response != "Txt already exists!":
                Common.writeLog(log_folder_path+'/logAddedTxt.txt', response)
            else:
                Common.writeLog(log_folder_path+'/logTxtExists.txt', output_folder)

if __name__ == "__main__":
    main(
        data_base_name='YoutubeFace', upper_folder_name='UMUT',
        align_images_flag=True, reset_images_flag=True,
        auto_feature_select=False, print_features_flag=True,
        select_first_image_as_frontal=False, show_aligned_images=False
    )
