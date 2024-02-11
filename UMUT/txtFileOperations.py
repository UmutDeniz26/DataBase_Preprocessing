import os
import numpy as np

import Common

abs_space = 1 # This is the absolute space for each column in the main txt file
def writeLandmarksTxtFile(txt_path, landmarks):
    if type(landmarks) is not dict:
        txt_path = txt_path.replace(".txt", "_FaceNotFound.txt")
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        with open(txt_path , 'w') as file:
            file.write("FaceNotFound")
        return "FaceNotFound"

    keys = list(landmarks.keys())

    # Make sure that the txt_path is a file
    if os.path.isdir(txt_path):
        print("Error: " + txt_path + " is a directory!")
        exit()

    # Output file path should be a txt file, this line will change the extension to txt
    txt_path = os.path.splitext(txt_path)[0] + '.txt'

    #txt file operations
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    with open(txt_path , 'w') as file:
        file.write("{\n")
        for key, value in landmarks.items():
            if key == keys[-1]:
                file.write(f" \"{key}\" : {value}\n")
            else:
                file.write(f" \"{key}\" : {value},\n")
        file.write("}")
    return "Txt file successfully written! : " + txt_path


def initMainTxtFile(dbName,upperFolderName,columns):
    txt_path = os.path.join(upperFolderName, dbName + "_FOLDERED", dbName + "_Info.txt")
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)

    # Column names written to the txt file
    with open(txt_path , 'w') as file:
        for column in columns:
            space_count = np.floor(abs_space/len(columns)).astype(int)
            file.write(f"{column:^{space_count}},")

    os.makedirs(f'./{upperFolderName}/LOG/{dbName}', exist_ok=True)
    Common.writeLog(f'./{upperFolderName}/LOG/{dbName}/logMainTxtFile.txt', "Initialized txt: " + txt_path + " successfully!")
    return "Initialized txt: " + txt_path + " successfully!"

def writeFileMainTxt(txt_path, landmarks, inter, intra):
    if landmarks == False:
        landmarks = {"Response": False}

    # in elements, is there _FOLDERED, if there is, then split it with "_" then take the first element
    # This part is weaking, it should be changed, because it is connected to the folder name notation (_FOLDERED)
    # os.path.normpath(txt_path).split(os.sep) => It splits the path with the os.sep, which is the seperator of the path ( "/" )
    for index,element in enumerate(os.path.normpath(txt_path).split(os.sep)):
        if "_FOLDERED" in element:
            dbName = element.split("_")[0]
            upperFolderName = os.path.normpath(txt_path).split(os.sep)[index-1]
            break

    file_path = txt_path.replace(".txt", "")

    #txt_path = f'./{upperFolderName}/{dbName}_FOLDERED/{dbName}_Info.txt'
    txt_path = os.path.join(upperFolderName, dbName + "_FOLDERED", dbName + "_Info.txt")

    #   prepare a string with columns, all colum should be seperated with "|" and should be in the middle of the string and taking 6 space from the left and right
    columns = [ file_path + ".jpg" ] + [inter] + [intra] + list(landmarks.values())

    space_count = np.floor(abs_space/len(columns)).astype(int)
    with open(txt_path , 'a') as file:
        file.write("\n")
        for column in columns:
            file.write(f"{str(column):^{space_count}}, ")

    Common.writeLog(f'./{upperFolderName}/LOG/{dbName}/logMainTxtFile.txt', "Text line successfully added to main text! : " + file_path)
    return "Text line successfully added to main text! : " + file_path

import json
def readJsonDictFromFile(fileToRead):
    try:
        with open(fileToRead, 'r') as file:
            json_dict = json.load(file)
            return json_dict
    except:
        print("Error: " + fileToRead + " is not a json file!")
        return {"Response":False}
