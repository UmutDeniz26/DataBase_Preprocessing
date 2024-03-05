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
    print("Landmarks are written to the txt file successfully! : " + txt_path)


def initMainTxtFile(output_path,log_path ,columns, full_path="", full_path_flag = False):
    
    txt_path = os.path.join(output_path, "informations.txt")
    # Column names written to the txt file
    if not os.path.exists(txt_path):
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    with open(txt_path , 'w') as file:
        for column in columns:
            space_count = np.floor(abs_space/len(columns)).astype(int)
            file.write(f"{column:^{space_count}},")
    Common.writeLog(os.path.join(log_path, "logMainTxtFile.txt"), "Initialized txt: " + txt_path + " successfully!")

def writeFileMainTxt(txt_path, landmarks, inter, intra, destination="", full_path_flag = False):
    if landmarks == False:
        landmarks = {"Response": False}

    file_path = txt_path
    output_path = txt_path.split(os.sep)[-4]
    txt_path = os.path.join(output_path, "informations.txt")
    #   prepare a string with columns, all colum should be seperated with "|" and should be in the middle of the string and taking 6 space from the left and right
    columns = [ file_path ] + [inter] + [intra]# + list(landmarks.values())

    space_count = np.floor(abs_space/len(columns)).astype(int)
    with open(txt_path , 'a') as file:
        file.write("\n")
        for column in columns:
            file.write(f"{str(column):^{space_count}}, ")

    #Common.writeLog(f'./{upperFolderName}/LOG/{dbName}/logMainTxtFile.txt', "Text line successfully added to main text! : " + file_path)
    return "Text line successfully added to main text! : " + file_path

import json
def readJsonDictFromFile(fileToRead):
    try:
        with open(fileToRead, "r") as fileToRead:
            try:
                content = json.loads( fileToRead.read() )
                return content
            except:
                #print("Error: " + fileToRead + " is not a valid json file!")
                return {"Response":False}
    except:
        #print("Error: " + fileToRead.name + " is not a json file!")
        return {"Response":False}
