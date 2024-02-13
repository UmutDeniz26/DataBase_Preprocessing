import os
import re
import cv2
import sys
import shutil

# Custom scripts
import Common
import DBsWithTxtInfo
import txtFileOperations
import NameFeatureExtractor
import FrontalFaceFunctions

root_dir_path = os.path.dirname(os.path.abspath(__file__))
root_dir_without_current_folder_name = root_dir_path.split('\\')[:-1]
root_dir_without_current_folder_name = '\\'.join(root_dir_without_current_folder_name)

os.chdir(root_dir_without_current_folder_name)

sys.path.insert(0, './UMUT')
sys.path.insert(0, './Ali')


import DetectUpperCase
import detectFrontelImageFromTxt


sys.path.insert(0, './retinaface_custom/main')

import RetinaFace
#from retinaface import RetinaFace

print("RetinaFace imported from", RetinaFace.__file__)

intra = 0
inter = 0

def main(
        data_base_name: str, upper_folder_name: str,
        align_images_flag: bool, reset_images_flag: bool,
        auto_feature_select: bool = False, print_features_flag: bool = True,
        select_first_image_as_frontal: bool = False, show_aligned_images: bool = False
    )->list:
    """
    This function will create a new folder structure for the dataset.
    Args:
        data_base_name (str): The name of the dataset.
        upper_folder_name (str): The name of the upper folder.
        align_images_flag (bool): If True, the images will be aligned.
        reset_images_flag (bool): If True, the images will be reset.
        auto_feature_select (bool): If True, the features will be selected automatically.
        print_features_flag (bool): If True, the features will be printed.
        select_first_image_as_frontal (bool): If True, the first image will be selected as the frontal image.
        show_aligned_images (bool): If True, the aligned images will be shown.
    """

    #------------------------------------------------------- Initialization -------------------------------------------------------#
    #This is the folder path of the logs
    log_folder_path = os.path.join(upper_folder_name, 'LOG', data_base_name)

    os.makedirs(log_folder_path, exist_ok=True)
    Common.clearLogs(log_folder_path)

    # This is very important for the txt operations.
    #The txt file should be in the same folder with the images and the name of the txt file should be the same with the name of the folder
    txt_info_path = os.path.join(upper_folder_name, data_base_name + '.txt')

    print(txtFileOperations.initMainTxtFile(data_base_name,upper_folder_name,
        ["file_path","inter","intra","right_eye","left_eye","nose","mouth_right","mouth_left"]))

    #These variables will be automatically changed according to the number of features
    hold_id, hold_left_inner_id, hold_features_count, frontal_count = 0, 0, 0, 0

    if data_base_name == 'YoutubeFace' or 'LFW' or 'CASIA-FaceV5(BMP)':
        images_with_txt_file_format = True
    else:
        images_with_txt_file_format = False

    #------------------------------------------------------- Main Part -------------------------------------------------------#

    data_base_folder_path = os.path.join(upper_folder_name, data_base_name)
    """
    data_base_folder_path = os.path.join(root_dir_without_current_folder_name, data_base_folder_path)
    txt_info_path = os.path.join(root_dir_without_current_folder_name, txt_info_path)
    log_folder_path = os.path.join(root_dir_without_current_folder_name, log_folder_path)
    """

    files = os.scandir(data_base_folder_path)

    if DetectUpperCase.save_second_letter_upper(data_base_folder_path,"uppercase_files.txt") >0:
        print("There are some folders that has two upper case.")
        DetectUpperCase.rename_second_letter_lowercase(data_base_folder_path)
        exit()

    first_iteration = True;make_deceison_flag = True

    #Txt operations for YoutubeFace and LFW
    if images_with_txt_file_format ==True:
        image_informations_txt = open(txt_info_path, 'r') # change this
        image_informations = image_informations_txt.readlines()
        image_informations = Common.replaceEntersAndTabs(image_informations)
        files = DBsWithTxtInfo.imgTxtDBsFilesConcat(files)

    files.sort()

    #Iterate through the files
    for index,file in enumerate(files):
        if images_with_txt_file_format == True:
            # Warning about the number of txt file lines and the number of images
            if len(image_informations) != len(files) and index == 0:
                print("The number of txt file lines and the number of images are not equal!",
                    "\nThe number of txt file lines: " + str(len(image_informations)) +
                    "\nThe number of images: " + str(len(files)),
                    "\nThis can cause a problem!")

                input("Press Enter to continue...")

            output_file_name = image_informations[index]+'.jpg'
            input_file_path = file
        else:
            output_file_name = file.name
            input_file_path = './' + upper_folder_name + '/' + data_base_name + '/' + output_file_name


        #Extract features from file name
        features,make_deceison_flag = NameFeatureExtractor.extractFeaturesFromFileName(output_file_name, auto_feature_select, make_deceison_flag, print_features_flag)
        numberOfSlices = features["numberOfSlices"]
        #When number of slices changed, we should extract features again
        if numberOfSlices != hold_features_count and first_iteration == False:
            print("Number of features changed! Please check the features!")
            if auto_feature_select == False:
                input("Press Enter to continue...")
            make_deceison_flag = True
            features,make_deceison_flag = NameFeatureExtractor.extractFeaturesFromFileName(output_file_name, auto_feature_select, make_deceison_flag, print_features_flag)
        hold_features_count = numberOfSlices

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

            confidence_score, most_frontal_face_name = detectFrontelImageFromTxt.run(output_folder)

            if select_first_image_as_frontal:
                most_frontal_face_name = most_frontal_face_name.split("_")
                most_frontal_face_name[-1] = "0"
                most_frontal_face_name = "_".join(most_frontal_face_name)

            if not most_frontal_face_name:
                #If there is no frontal face, the last image is selected as frontal face
                Common.writeLog(
                    os.path.join(log_folder_path, 'logNoFrontalFace.txt'),
                    output_file_name + ", the first image is selected as frontal face!"
                )
            #If there is a frontal face, the image is selected as frontal face
            frontal_image_folder = os.path.join(output_folder, "frontal")
            if os.listdir(frontal_image_folder):
                print("Frontal Image Already Exists!")
                Common.clearFolder(frontal_image_folder)

            frontal_image_path = os.path.join(output_folder, most_frontal_face_name + ".jpg")
            frontal_count += 1

            # Copy the frontal image to the frontal folder
            Common.copyFile(
                frontal_image_path, # from
                os.path.join(frontal_image_folder, most_frontal_face_name + ".jpg") # to
            )
            os.makedirs(
                os.path.join('./', upper_folder_name, data_base_name + '_FOLDERED', 'Frontal_Faces'), exist_ok=True
            )

            # Copy the frontal image to the frontal faces folder
            Common.copyFile(
                frontal_image_path, # from
                os.path.join(
                    "./", upper_folder_name, data_base_name + "_FOLDERED", "Frontal_Faces", most_frontal_face_name + ".jpg") # to
            )

            # Write the frontal image to the log file
            Common.writeLog(
                os.path.join(log_folder_path, 'logAddedFrontalImage.txt'), frontal_image_path
            )


        first_iteration = False
        hold_id = file_id
        hold_left_inner_id = inner_id_left_side


        # In this part, you can change the output folder structure according to your needs
        # If learnType is True-> output_folder = f'./{upper_folder_name}/{data_base_name}_FOLDERED/{learnType}/{file_id}/'
        output_folder = os.path.join(upper_folder_name, data_base_name + "_FOLDERED", learnType + "/" if learnType else "", file_id + "/")

        # Add inner folder when inner_id_left_side is different than False and inner_id_left_side is a number
        if inner_id_left_side != False and inner_id_left_side.isdigit() == True:
            output_folder = os.path.join(output_folder, inner_id_left_side + "/")
        else:
            output_folder = os.path.join(output_folder, "0" + "/")

        # Create folders if they don't exist / COPY PROCESS
        # Replace the images with same name
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, output_file_name)

        #Here we copy the jpg file to the output folder
        if extension != 'mat':
            #aligned_file_path = input_file_path.replace("UMUT", "UMUT/"+data_base_name+"_aligned")
            if reset_images_flag == True or not os.path.exists(output_file_path):
                #Expand face area is a parameter for the retinaface, it is used to expand the face area
                #It is used to include the hair and the ears in the face area !!!
                if align_images_flag == True:
                    try:
                        response_dictionary = RetinaFace.extract_faces(input_file_path,align=True,align_first=True)
                        cropped_aligned_face = response_dictionary["face_1"]["face"]
                        landmarks = response_dictionary["face_1"]["landmarks"]
                    except:
                        cropped_aligned_face = [];landmarks = {}

                    try:
                        if response_dictionary["TwoPeopleDetected"] == True:
                            Common.writeLog( log_folder_path+"/logTwoFace", output_file_path)
                    except:
                        True

                    if len(cropped_aligned_face) ==0:
                        Common.writeLog(log_folder_path+'/logNoFace.txt', output_file_name)
                        Common.copyFile(input_file_path, output_file_path)
                    else:
                        print("Copying " + input_file_path + " to " + output_file_path)
                        cv2.imwrite(output_file_path, cropped_aligned_face)
                        #Common.copyFile(aligned_file_path, output_file_path)
                else:
                    landmarks = RetinaFace.detect_faces(input_file_path)['face_1']['landmarks']
                    Common.copyFile(input_file_path, output_file_path)
            else:
                Common.writeLog(log_folder_path+'/logExists.txt', output_file_path)
                if extension == 'jpg':
                    landmarks = txtFileOperations.readJsonDictFromFile(output_file_path.replace('jpg','txt'))
                if len(landmarks) == 0:
                    Common.writeLog(log_folder_path+'/logNoFace.txt', output_file_path)

        logString = "Added Image: " + output_file_name
        Common.writeLog(log_folder_path+'/logAddedImage.txt', logString)

        #Frontal detection
        if extension == 'jpg':
            # If all of the images was processed, in a folder:

            if images_with_txt_file_format == True:
                input_file_path = file
            else:
                input_file_path = './' + upper_folder_name + '/' + data_base_name + '/' + output_file_name

            #Read the image
            image_cv2 = cv2.imread(input_file_path)

            global intra
            #Calculate the landmarks of the frontal face and write them to the txt file
            response = FrontalFaceFunctions.writeRetinaFaceLandmarks(
                                            image_cv2, output_file_path,
                                            inter, intra,show_aligned_images, landmarks
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
        auto_feature_select=False, print_features_flag=False,
        select_first_image_as_frontal=False, show_aligned_images=False
    )
