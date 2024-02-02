from detect_frontal_face import copy_max_abs_image_to_folder
import os

source_folder = "./Ali/CASIA-FaceV5(BMP)/Face/"
destination_folder = "./Ali/CASIA-FaceV5(BMP)/Face"

for filename in os.listdir(source_folder):

    image_path = os.path.join(source_folder, filename)
    copy_max_abs_image_to_folder(image_path, image_path)