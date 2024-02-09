import os
import json
import math
import sys

def run(folder_path):
    max_abs_image= ""
    max_abs_value = sys.maxsize
    for filename in os.listdir(folder_path):
        image_path = folder_path + "/" + filename
        if filename.endswith(('.txt')):
            try:
                with open(image_path, "r") as file:
                    content = file.read()
                    content = json.loads(content)
            except:
                print("Error: " + image_path + " is not a valid json file!")
                continue
            try:
                distance_nose_left_eye = math.sqrt((content["left_eye"][0] - content["nose"][0])**2 + (content["left_eye"][1] - content["nose"][1])**2)
                distance_nose_right_eye = math.sqrt((content["right_eye"][0] - content["nose"][0])**2 + (content["right_eye"][1] - content["nose"][1])**2)
                difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)
                if difference_between_le_re < max_abs_value:
                    max_abs_value = difference_between_le_re
                    max_abs_image = filename.replace(".txt","")
            except:
                difference_between_le_re = 1000.0
    #print(max_abs_value,max_abs_image)
    if max_abs_value == -1 or max_abs_image == "":
        return False, False
    return max_abs_value,max_abs_image
