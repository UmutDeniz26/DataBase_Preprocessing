# from detect_frontal_face import copy_max_abs_image_to_folder
# import os

# source_folder = "./Ali/CASIA-FaceV5(BMP)/Face/"
# destination_folder = "./Ali/CASIA-FaceV5(BMP)/Face"

# for filename in os.listdir(source_folder):

#     image_path = os.path.join(source_folder, filename)
#     copy_max_abs_image_to_folder(image_path, image_path)

import sys
sys.path.insert(0, "./UMUT")

import main as DB_Folder_Manipulator

DB_Folder_Manipulator.main(
        data_base_name='YoutubeFace', upper_folder_name='Ali',
        align_images_flag=True, reset_images_flag=True,
        auto_feature_select=False, print_features_flag=False,
        select_first_image_as_frontal=False, show_aligned_images=False
    )
