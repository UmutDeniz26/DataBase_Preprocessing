import os
import json
import math
import sys
import numpy as np

y = 0
abs_space = 1
def run(folder_path,i):
    max_abs_image= ""
    max_abs_value = sys.maxsize
    
    global y
    for filename in sorted(os.listdir(folder_path)):
        image_path = folder_path + "/" + filename

        if filename.endswith(('.txt')):

            try:
                with open(image_path, "r") as file:
                    content = file.read()
                    content = json.loads(content)
                    print(content)
            except:
                print("Error: " + image_path + " is not a valid json file!")
                continue
            txt_path = '/home/ali/Desktop/github/DataBase_Preprocessing/Ali/Info.txt'
            
            resp_holder = content.copy()
            for key, value in resp_holder.items():
                if key == "left_eye" or key == "right_eye" or key == "nose" or key == "mouth" or key == "face":
                    featureSelectFlag = True
                if featureSelectFlag:
                    content.update({key: value})

            file_path = image_path.replace(".txt", "")
            file_path = file_path.replace("/home/ali/Desktop/github/DataBase_Preprocessing/Ali","")
            colums = [ file_path + ".jpg" ] + [i] + [y] + list(content.values())

            y += 1
            space_count = np.floor(abs_space/len(colums)).astype(int)
            with open(txt_path , 'a') as file:
                file.write("\n")
                for column in colums:
                    if column == colums[-1]:
                        file.write(f"{str(column):^{space_count}}")
                    elif column == colums[0]:
                        file.write("\"")
                        file.write(f"{str(column):^{space_count}}\",")
                    else:
                        file.write(f"{str(column):^{space_count}},")
            distance_nose_left_eye = math.sqrt((content["left_eye"][0] - content["nose"][0])**2 + (content["left_eye"][1] - content["nose"][1])**2)
            distance_nose_right_eye = math.sqrt((content["right_eye"][0] - content["nose"][0])**2 + (content["right_eye"][1] - content["nose"][1])**2)
            difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)
            if difference_between_le_re < max_abs_value:
                max_abs_value = difference_between_le_re
                max_abs_image = filename.replace(".txt","")
    #print(max_abs_value,max_abs_image)
    if max_abs_value == -1 or max_abs_image == "":
        return False, False
    return max_abs_value,max_abs_image
source_folder = "/home/ali/Desktop/github/DataBase_Preprocessing/Ali/CASIA-FaceV5(BMP)/Face"
i = 0
for filename in os.listdir(source_folder):

    image_path = os.path.join(source_folder, filename)
    run(image_path,filename)



def runn(txt_path):
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    columns = ["file_path","inter","intra","left_eye","right_eye","nose","mouth_left","mouth_right","facial_area"]
    with open(txt_path , 'w') as file:
        for column in columns:
            space_count = np.floor(abs_space/len(columns)).astype(int)
            if column == columns[-1]:
                file.write(f"{column:^{space_count}}")
            else:
                file.write(f"{column:^{space_count}},")

# runn('/home/ali/Desktop/github/DataBase_Preprocessing/Ali/Info.txt')