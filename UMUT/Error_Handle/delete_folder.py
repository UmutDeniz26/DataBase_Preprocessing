import os 
import sys
import shutil
def main(file_paths_txt):

    with open(file_paths_txt, "r") as f:
        file_paths = f.readlines()
    
    for file_path in file_paths:
        file_path = file_path.split(" ")[0]
        file_path = file_path.strip()
        file_path = os.path.normpath(file_path)
        txt_path = file_path.replace(".jpg", ".txt")
        
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path} and its txt file")
        except FileNotFoundError:
            pass
        
        try:
            os.remove(txt_path)
            print(f"Deleted: {txt_path}")
        except FileNotFoundError:
            pass

            
    """
    db_folder_path = os.sep.join(os.path.normpath(file_paths[0].strip()).split("\\")[:-3])
    print(f"db_folder_path: {db_folder_path}")

    for file_path in file_paths:
        file_path = file_path.strip()
        file_path = os.path.normpath(file_path)
        folder_path = os.path.dirname(file_path)
        try:
            shutil.rmtree(folder_path)
            with open(log, "a") as f:
                f.write(f"Deleted: {folder_path}\n")
        except FileNotFoundError:
            with open(error_log, "a") as f:
                f.write(f"Error: {folder_path}\n")


    for folder in os.listdir(db_folder_path):
        folder_path = os.path.join(db_folder_path, folder)
        if os.path.isfile(folder_path):
            continue
        
        file_count = len(os.listdir(folder_path))
        print(f"Deleting: {folder_path}")
        print(f"File count: {file_count}")
        if file_count == 0:
            shutil.rmtree(folder_path)
            with open(upper_log, "a") as f:
                f.write(f"Deleted: {folder_path}\n")
    """

if __name__ == "__main__":
    main("UMUT/Error_Handle/too_small_files.txt")



"""
example of error_paths.txt:
UMUT/database/HELEN_FOLDERED\00000027\00000030\00000027_00000030_00000498.jpg
UMUT/database/HELEN_FOLDERED\00000027\00000030\00000027_00000030_00000498.txt
"""
