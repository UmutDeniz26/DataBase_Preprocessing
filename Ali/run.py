from detect_frontal_face import copy_max_abs_image_to_folder
import os


import sys
sys.path.insert(0, "./UMUT")
import writeToTxt


source_folder = "./Ali/CASIA-FaceV5(BMP)/Face/"
destination_folder = "./Ali/CASIA-FaceV5(BMP)/Face"

for filename in os.listdir(source_folder):

    # Dosyanın tam yolu
    image_path = os.path.join(source_folder, filename)

    # copy_max_abs_image_to_folder fonksiyonunu çağır
    copy_max_abs_image_to_folder(image_path, destination_folder)