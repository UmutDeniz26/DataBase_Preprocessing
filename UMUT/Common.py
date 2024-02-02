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