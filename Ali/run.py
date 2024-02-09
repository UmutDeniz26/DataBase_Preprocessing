# from detect_frontal_face import copy_max_abs_image_to_folder
# import os

# source_folder = "./Ali/CASIA-FaceV5(BMP)/Face/"
# destination_folder = "./Ali/CASIA-FaceV5(BMP)/Face"

# for filename in os.listdir(source_folder):

#     image_path = os.path.join(source_folder, filename)
#     copy_max_abs_image_to_folder(image_path, image_path)

import sys
sys.path.insert(0, "./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator.main(dbName='CASIA-FaceV5(BMP)', upperFolderName='Ali', 
    inputOrAutoMod=False, printFeaturesFlag=False,
        selectFirstImageAsFrontal=False, showAlignedImages=False, 
        alignImagesFlag=True, resetImagesFlag=False) #if resetImagesFlag is True, then the images will be recreated 