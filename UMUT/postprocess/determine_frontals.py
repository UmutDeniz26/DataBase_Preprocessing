import os
import cv2
import sys

sys.path.insert(0,'./Ali')
import json
import math
import shutil
#import detectFrontelImageFromTxt as detect

def run(folder_path):
    max_abs_image= ""
    max_abs_value = sys.maxsize

    for filename in os.listdir(folder_path):
        image_path = folder_path + "/" + filename
        if filename.endswith(('.txt')):
            with open(image_path, "r") as file:
                content = file.read()
                content = content.replace(')',']').replace('(','[')
                if "Low Confidence" in content:
                    content = content.replace(",\"[Low Confidence]\"", '')
            try:
                    content = json.loads(content)
            except:
                print("Json Error: " + image_path + " is not a valid json file!")
                content = {"Response":False}
            try:
                distance_nose_left_eye = math.sqrt((content["left_eye"][0] - content["nose"][0])**2 + (content["left_eye"][1] - content["nose"][1])**2)
                distance_nose_right_eye = math.sqrt((content["right_eye"][0] - content["nose"][0])**2 + (content["right_eye"][1] - content["nose"][1])**2)
                difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)
                if difference_between_le_re < max_abs_value:
                    max_abs_value = difference_between_le_re
                    max_abs_image = filename.replace(".txt","")
            except:
                difference_between_le_re = 1000.0

    # Split the name with "." then join all the elements except the last one that is the extension, than return the name
    if max_abs_value == -1 or max_abs_image == "":
        return 0,  '.'.join( os.listdir(folder_path)[0].split('.')[:-1] )
    return max_abs_value,max_abs_image

def main(folder_path, select_first_as_frontal = False):

    # Frontal folders
    frontal_faces = []
    src_paths = []
    for root_path, dir_names, file_names in os.walk(folder_path):
        if "Frontal" in root_path or "frontal" in root_path:
            continue
        if len(file_names)>4:
            max_abs_value,max_abs_image = run(root_path)
            if select_first_as_frontal:
                max_abs_image = file_names[0].replace(".jpg", "")

            frontal_path = os.path.join(root_path, "frontal")
            if os.path.exists(frontal_path):
                shutil.rmtree(frontal_path)
                os.makedirs(frontal_path)
                shutil.copy(os.path.join(root_path, max_abs_image+".jpg"), os.path.join(frontal_path, max_abs_image+".jpg"))
                frontal_faces.append(max_abs_image)
                src_paths.append(os.path.join(root_path, max_abs_image+".jpg"))

            #print(f"Max Abs Value: {max_abs_value}, Max Abs Image: {max_abs_image}")

    # Frontal faces folder
    frontal_faces_folder = os.path.join(folder_path, "Frontal_faces")
    if os.path.exists(frontal_faces_folder):
        shutil.rmtree(frontal_faces_folder)
    os.makedirs(frontal_faces_folder)
    for frontal_face, src_path in zip(frontal_faces, src_paths):
        shutil.copy(src_path, os.path.join(frontal_faces_folder, frontal_face+".jpg"))

    # Frontal images paths txt
    txt_path = os.path.join(folder_path, "Frontal_faces.txt")
    with open(txt_path, "w") as file:
        for path in src_paths:
            file.write(path + "\n")

    print("Frontal faces txt is saved at: ", txt_path)



if __name__ == '__main__':
    main("UMUT/database/LFPW_FOLDERED_without_errors", select_first_as_frontal = True)
    main("UMUT/database/HELEN_FOLDERED_without_errors", select_first_as_frontal = True)
    main("UMUT/database/AFW_FOLDERED_without_errors", select_first_as_frontal = True)
