import os
import numpy as np

import Common

abs_space = 1 # This is the absolute space for each column in the main txt file
def run(txt_path, resp):
    if type(resp) is not dict:
        txt_path = txt_path.replace(".txt", "_FaceNotFound.txt")
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        with open(txt_path , 'w') as file:
            file.write("FaceNotFound")
        return "FaceNotFound"

    new_dict = {key: value for key, value in resp.items() if key not in ['distance_nose_left_eye', 'distance_nose_right_eye', 'difference_between_le_re']}
    keys = list(new_dict.keys())

    if txt_path.endswith(".bmp"):
        txt_path = txt_path.replace(".bmp", ".txt")
    if txt_path.endswith(".jpg"):
        txt_path = txt_path.replace(".jpg", ".txt")
    if os.path.isdir(txt_path):
        print("Error: " + txt_path + " is a directory!")
        exit()

    #txt file operations
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    with open(txt_path , 'w') as file:
        file.write("{\n")
        for key, value in new_dict.items():
            if key == keys[-1]:
                file.write(f" \"{key}\" : {value}\n")
            else:
                file.write(f" \"{key}\" : {value},\n")
        file.write("}")
    return "Added txt: " + txt_path + " successfully!"


def initMainTxtFile(dbName,upperFolderName,columns):
    txt_path = f'./{upperFolderName}/{dbName}_FOLDERED/{dbName}_Info.txt'
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    #prepare a string with colums, all colum should be seperated with "|" and should be in the middle of the string and taking 6 space from the left and right
    with open(txt_path , 'w') as file:
        for column in columns:
            space_count = np.floor(abs_space/len(columns)).astype(int)
            if column == columns[-1]:
                file.write(f"{column:^{space_count}}")
            else:
                file.write(f"{column:^{space_count}},")

    os.makedirs(f'./{upperFolderName}/LOG/{dbName}', exist_ok=True)
    Common.writeLog(f'./{upperFolderName}/LOG/{dbName}/logMainTxtFile.txt', "Initialized txt: " + txt_path + " successfully!")
    return "Initialized txt: " + txt_path + " successfully!"

def writeFileMainTxt(txt_path, resp, inter, intra):
    if resp == False:
        resp = {"left_eye": "FaceNotFound"}

    # in elements, is there _FOLDERED, if there is, then split it with "_" then take the first element
    # This part is weaking, it should be changed, because it is connected to the folder name notation (_FOLDERED)
    for index,element in enumerate(txt_path.split("/")):
        if "_FOLDERED" in element:
            dbName = element.split("_")[0]
            upperFolderName = txt_path.split("/")[index-1]
            break

    # This part is also weaking, because it needs a dictionary with exact keys
    featureSelectFlag = False
    resp_holder = resp.copy()
    resp.clear()
    #print(resp_holder)
    for key, value in resp_holder.items():
        if key == "left_eye" or key == "right_eye" or key == "nose" or key == "mouth" or key == "face":
            featureSelectFlag = True
        if featureSelectFlag:
            resp.update({key: value})

    file_path = txt_path.replace(".txt", "")
    txt_path = f'./{upperFolderName}/{dbName}_FOLDERED/{dbName}_Info.txt'
    colums = [ file_path + ".jpg" ] + [inter] + [intra] + list(resp.values())

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

    Common.writeLog(f'./{upperFolderName}/LOG/{dbName}/logMainTxtFile.txt', "Added txt line to main Txt: " + file_path + " successfully!")
    return "Added txt line to main Txt: " + file_path + " successfully!"

import json
def readJsonDictFromFile(fileToRead):
    with open(fileToRead, 'r') as file:
        json_dict = json.load(file)
        return json_dict
