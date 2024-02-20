import os
import shutil

def replaceEntersAndTabs(array):
    newArray = []
    for element in array:
        element = element.replace('\n', '');element = element.replace('\t', '');element = element.replace(' ', '')
        newArray.append(element)
    return newArray


def writeLog(log_file_path, log):
    with open(log_file_path, 'a') as log_file:
        log_file.write(log + '\n')


def clearLogs(logFolderPath):
    if os.path.exists(logFolderPath):
        shutil.rmtree(logFolderPath)
        os.makedirs(logFolderPath, exist_ok=True)

def copyFile(input_file_path, output_file_path):
    print("Copying: " + input_file_path + " to " + output_file_path)
    shutil.copy(input_file_path, output_file_path)

def clearFolder(folderPath):
    if os.path.exists(folderPath):
        shutil.rmtree(folderPath)
        os.makedirs(folderPath, exist_ok=True)
    else:
        os.makedirs(folderPath, exist_ok=True)
