import os
import re
import cv2
import sys
import shutil
import time

# Custom scripts
import Common
import DBsWithTxtInfo
import txtFileOperations
import NameFeatureExtractor
import FrontalFaceFunctions

sys.path.insert(0, './UMUT')
sys.path.insert(0, './Ali')

import DetectUpperCase
import detectFrontelImageFromTxt

print("Operating System: ", os.name)

from retinaface import RetinaFace
print("RetinaFace imported from", RetinaFace.__file__, "\n")

person_cnt = 0
intra = 0
inter = 0

def main(
        align_images_flag: bool, reset_images_flag: bool,
        auto_feature_select: bool = False, print_features_flag: bool = True,
        select_first_image_as_frontal: bool = False, show_aligned_images: bool = False,
        txt_info_file_format: bool = False
    )->list:
    """
    This function will create a new folder structure for the dataset.
    Args:
        align_images_flag (bool): If True, the images will be aligned.
        reset_images_flag (bool): If True, the images will be reset.
        auto_feature_select (bool): If True, the features will be selected automatically.
        print_features_flag (bool): If True, the features will be printed.
        select_first_image_as_frontal (bool): If True, the first image will be selected as the frontal image.
        show_aligned_images (bool): If True, the aligned images will be shown.
        txt_info_file_format (bool): If True, the images will be in txt file format.
    """
    
    # Constants
    data_base_folder_path = "./src/dataset/"
    txt_info_path = "./src/text/dataset.txt"
    log_folder_path = "./log/"
    output_folder_path = "./casia-webface/"
    
    # Relative paths
    frontal_faces_dir_path = os.path.join(output_folder_path,'Frontal_Faces')
    

    #------------------------------------------------------- Initialization -------------------------------------------------------#
    global person_cnt,intra,inter

    Common.clearLogs(log_folder_path)    
    if reset_images_flag:
        shutil.rmtree(output_folder_path, ignore_errors=True)

    # Create the directories
    Common.init_dirs([data_base_folder_path, output_folder_path, log_folder_path, frontal_faces_dir_path])

    txtFileOperations.initMainTxtFile(output_folder_path,log_folder_path,
        ["file_path","inter","intra","right_eye","left_eye","nose","mouth_right","mouth_left"])

    #These variables will be automatically changed according to the number of features
    hold_id, hold_left_inner_id, hold_features_count, frontal_count = 0, 0, 0, 0

    #------------------------------------------------------- Main Part -------------------------------------------------------#
    
    # Get the files in the folder then sort them
    files = os.scandir(data_base_folder_path)

    if DetectUpperCase.detect_upper_second_letter(data_base_folder_path,"uppercase_files.txt") >0:
        print("There are some folders that has two upper case.")
        DetectUpperCase.rename_second_letter_lowercase(data_base_folder_path)
        exit()

    first_iteration = True;make_deceison_flag = True

    #Txt operations for the databases with txt info file
    if txt_info_file_format ==True:
        image_informations_txt = open(txt_info_path, 'r') # change this
        image_informations = image_informations_txt.readlines()
        image_informations = Common.replaceEntersAndTabs(image_informations)
        files = DBsWithTxtInfo.imgTxtDBsFilesConcat(files)

    #Iterate through the files
    for index,file in enumerate(files):
        if txt_info_file_format == True:
            # Warning about the number of txt file lines and the number of images
            if len(image_informations) != len(files) and index == 0:
                print("The number of txt file lines and the number of images are not equal!",
                    "\nThe number of txt file lines: " + str(len(image_informations)) +
                    "\nThe number of images: " + str(len(files)),
                    "\nThis can cause a problem!")
                input("Press Enter to continue...")

            output_file_name = image_informations[index] + '.jpg'
            input_file_path = file
        else:
            output_file_name = file.name
            input_file_path = os.path.join(data_base_folder_path, output_file_name)

        #Extract features from file name
        features,make_deceison_flag = NameFeatureExtractor.extractFeaturesFromFileName(output_file_name, auto_feature_select, make_deceison_flag, print_features_flag)
        
        # Check if the number of features changed
        numberOfSlices = features["numberOfSlices"]
        if numberOfSlices != hold_features_count and hold_features_count != 0:
            print("Number of features changed! Please check the features!")
            print("The previous number of slices: " + str(hold_features_count))
            print("The current number of slices: " + str(numberOfSlices))
            print("The current features: " + str(features))
            input("Press Enter to continue...")
        hold_features_count = numberOfSlices

        #Get the features
        inner_id_right_side = features["inner_id_right_side"]
        inner_id_left_side = features["inner_id_left_side"]
        extension = features["extension"]
        learnType = features["learnType"]
        file_id = features["file_id"]

        if first_iteration == True:
            start = time.time()
        #If the fileID or inner_id_left_side is different than the previous one, we should detect the frontal face of the previous folder
        if ( hold_id != file_id or hold_left_inner_id != inner_id_left_side ) and first_iteration == False:
            inter+=1
            if hold_id != file_id:
                person_cnt+=1

            _, most_frontal_face_name = detectFrontelImageFromTxt.run(output_folder)

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
                most_frontal_face_name = output_file_name
                
            #If there is a frontal face, the image is selected as frontal face
            frontal_image_folder = os.path.join(output_folder, "frontal")

            # Create the frontal folder if it doesn't exist
            if not os.path.exists(frontal_image_folder):
                os.makedirs(frontal_image_folder, exist_ok=True)

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

            # Copy the frontal image to the frontal faces folder
            Common.copyFile(
                frontal_image_path, # from
                os.path.join(
                    output_folder_path, "Frontal_Faces", most_frontal_face_name + ".jpg") # to
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
        output_folder = os.path.join(
            output_folder_path, learnType + "/" if learnType else "", file_id + "/"
        )

        # Add inner folder when inner_id_left_side is different than False and inner_id_left_side is a number
        if inner_id_left_side != False and inner_id_left_side.isdigit() == True:
            if txt_info_file_format:
                output_folder = os.path.join(output_folder, inner_id_left_side + "/")
        else:
            output_folder = os.path.join(output_folder, "0/")

        if txt_info_file_format==False:
            string_person_cnt = f'{person_cnt:08d}'
            string_inter = f'{intra:08d}'
            string_intra = f'{inter:08d}'

            if len(output_folder)>30:
                print()

            output_folder = os.path.join(os.path.join(
                output_folder.split('\\')[:-1]),string_person_cnt,string_intra) + "\\"

        # Create folders if they don't exist / COPY PROCESS
        # Replace the images with same name
        os.makedirs(output_folder, exist_ok=True)
        if txt_info_file_format:
            output_file_path = os.path.join(output_folder, output_file_name)
        else:
            output_file_path = os.path.join(
                output_folder, '_'.join([string_person_cnt,string_intra,string_inter])
                +'.'+output_file_name.split('_')[-1].split('.')[-1])

        #Here we copy the jpg file to the output folder
        if extension != 'mat':
            #aligned_file_path = input_file_path.replace("UMUT", "UMUT/"+data_base_name+"_aligned")
            if reset_images_flag == True or not os.path.exists(output_file_path):
                #Expand face area is a parameter for the retinaface, it is used to expand the face area
                #It is used to include the hair and the ears in the face area !!!
                if align_images_flag == True:
                    log_message = "Extracting is successful!"
                    try:
                        response_dictionary = RetinaFace.extract_faces(input_file_path,align=True,align_first=True)
                        cropped_aligned_face = response_dictionary["face_1"]["face"]
                        landmarks = response_dictionary["face_1"]["landmarks"]
                    except:
                        response_dictionary = {};landmarks = {};cropped_aligned_face = []

                    if "TwoPeopleDetected" in response_dictionary.keys():
                        if response_dictionary["TwoPeopleDetected"] == True:
                            log_message = "Error: Two people detected!"
                            Common.writeLog( log_folder_path+"/logTwoFace", output_file_path)
                

                    if len(cropped_aligned_face) ==0:
                        log_message = "Error: No face detected!"
                        Common.writeLog(log_folder_path+'/logNoFace.txt', output_file_name)
                        Common.copyFile(input_file_path, output_file_path)
                    else:
                        cv2.imwrite(output_file_path, cropped_aligned_face)
                        #Common.copyFile(aligned_file_path, output_file_path)
                    
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Processed: {index+1:08d} / {len(files):08d} ({(index+1)/len(files)*100:3.3f}%)")
                    print(f"Elapsed time (hh:mm:ss): {time.strftime('%H:%M:%S', time.gmtime(time.time()-start))}")
                    print(f"Remaining time (hh:mm:ss): {time.strftime('%H:%M:%S', time.gmtime((time.time()-start)*(len(files)-index)/(index+1)))}")
                    print(f"Copying: \n", input_file_path + " to ", output_file_path)
                    print(f"Log Message: {log_message}")
                else:
                    landmarks = RetinaFace.detect_faces(input_file_path)['face_1']['landmarks']
                    Common.copyFile(input_file_path, output_file_path)
            else:
                Common.writeLog(log_folder_path+'/logExists.txt', output_file_path)
                if extension == 'jpg':
                    landmarks = txtFileOperations.readJsonDictFromFile(output_file_path.replace('jpg','txt'))
                if len(landmarks) == 0:
                    Common.writeLog(log_folder_path+'/logNoFace.txt', output_file_path)

        Common.writeLog(log_folder_path+'/logAddedImage.txt', output_file_path)

        #Frontal detection
        if extension == 'jpg':
            # If all of the images was processed, in a folder:

            if txt_info_file_format == True:
                input_file_path = file
            else:
                input_file_path = os.path.join(data_base_folder_path, output_file_name)

            #Read the image
            image_cv2 = cv2.imread(input_file_path)

            #Calculate the landmarks of the frontal face and write them to the txt file
            response = FrontalFaceFunctions.writeRetinaFaceLandmarks(
                                            image_cv2, output_file_path,
                                            inter, intra,show_aligned_images, landmarks
                        )
            if response != "Txt already exists!":
                Common.writeLog(log_folder_path+'/logAddedTxt.txt', response)
            else:
                Common.writeLog(log_folder_path+'/logTxtExists.txt', output_folder)
            intra+=1
    return start

if __name__ == "__main__":
    start = main(
        align_images_flag=True, reset_images_flag=True,
        auto_feature_select=False, print_features_flag=False,
        select_first_image_as_frontal=False, show_aligned_images=False,
        txt_info_file_format=True
    )

    summary = \
    """
    -------------------------------------------------------
    Main process is completed!
    -------------------------------------------------------
          Person Count: {}
            Intra: {}
            Inter: {}
          
          Total Elapsed Time: {}
    -------------------------------------------------------
    """\
    .format(person_cnt,intra,inter,time.strftime('%H:%M:%S', time.gmtime(time.time()-start)))

    print(summary)
