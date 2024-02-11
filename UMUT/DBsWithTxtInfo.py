import os
#This function will find jpg files in the folders
def imgTxtDBsFilesConcat(inFiles):
    inFilesPaths = []

    def traverse_directory(root_dir):
        for file in os.scandir(root_dir):
            if file.is_dir():
                traverse_directory(file.path)
            elif file.name.endswith(".jpg") or file.name.endswith(".bmp"):#değişen
                inFilesPaths.append(file.path)

    for file in inFiles:
        if file.is_dir():
            traverse_directory(file.path)
        elif file.name.endswith(".jpg") or file.name.endswith(".bmp"):#değişen
            inFilesPaths.append(file.path)

    return inFilesPaths
