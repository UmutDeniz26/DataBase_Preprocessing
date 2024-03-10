import os 
import sys
import json
sys.path.insert(0, './UMUT')

# Count the number of slices in a path
def count_path_slices(path, database_root_path):

    # Remove the database root path from the path
    split_path = path.split(database_root_path)
    purified_path = split_path[1]

    # Normalize the path to handle both forward and backward slashes
    path = os.path.normpath(purified_path)
    # Split the path into directory slices
    slices = path.split(os.sep)
    slices = [slice for slice in slices if slice!=""]

    # Count the number of slices
    return len(slices)

# Get the number of correct files and the files with errors in a folder
def get_correct_file_count_and_error_files(root):
    # Initialize variables
    temp_error_files = []

    # Get the files in the folder
    files = os.listdir(root)

    for file in files:
        if file.endswith(".txt") and "_Info" not in file:
            txt_path = os.path.join(root, file)
            img_path = txt_path.replace(".txt", ".jpg")
            with open(txt_path, "r") as f:
                content = f.read()

            if "Error" in content or "Stack Overflow" in content or "too small"\
                in content or "LandmarkError" in content or "Response" in content\
                and "pass_exception" not in content:

                temp_error_files.append(img_path);temp_error_files.append(txt_path)
    
    error_count = len(temp_error_files)//2
    correct_files = len(files)//2 - error_count
    return correct_files, temp_error_files, error_count

# Write the content of an array to a txt file
def write_array_to_txt_file(file_path, content_arr):
    with open(file_path, "a") as f:
        for item in content_arr:
            f.write(f"{item}\n")

# Main function
def main(folder_path):

    # Initialize variables
    index = 0;error_count = 0
    paths_of_correct_files_smaller_than_5 = [];info_of_correct_files_smaller_than_5 = []
    files_to_delete = []
    folder_count = len(os.listdir(folder_path))

    for root, dirs, files in os.walk(folder_path):
        print(f"\n\n\nProgress: {(index/folder_count)*100:.2f}%", end="\r")
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

        # if frontal folder pass
        if "frontal" in root:
            index += 1
            continue   

        # Only process the folders with 2 slices ( Which means the folder is a person folder )
        if count_path_slices(root,folder_path) == 2:
            correct_file_count, files_with_error,error_count = get_correct_file_count_and_error_files(root)
            string = (f"Error count: {error_count}  "
                        f"Total files: {len(files)}  "
                        f"Correct files: {int(correct_file_count)}  "
                        f"Folder path: {root}")

            # If the number of correct files is smaller than 5, add the info to the array
            if correct_file_count < 5:
                info_of_correct_files_smaller_than_5.append(string)
                for file in files_with_error:
                    paths_of_correct_files_smaller_than_5.append(file)       
            else:
                write_txt_path = os.path.join("UMUT","Error_Handle", "error_greater_than_5.txt")
                write_array_to_txt_file(write_txt_path, [string])

                for file in files_with_error:
                    txt_path = file
                    img_path = file.replace(".txt", ".jpg")

                    if os.path.exists(img_path) and os.path.exists(txt_path):
                        #os.remove(img_path)
                        files_to_delete.append(img_path)
                        #os.remove(txt_path)
                        files_to_delete.append(txt_path)
                    else:
                        print(f"Files does not exist: {img_path}")
                        exit()

    # # # # # # # # # # # # # # # #  WRITE TO TXT FILES # # # # # # # # # # # # # # # # # # # # # # # # 

    # Write the paths of the files to delete to a txt file
    write_txt_path = os.path.join("UMUT","Error_Handle", "files_to_delete.txt")
    write_array_to_txt_file(write_txt_path, files_to_delete)

    # Write the info of the correct files smaller than 5 to a txt file
    write_txt_path = os.path.join("UMUT","Error_Handle", "error_info_smaller_than_5.txt")
    write_array_to_txt_file(write_txt_path, info_of_correct_files_smaller_than_5)

    # Write the paths of the correct files smaller than 5 to a txt file
    write_txt_path = os.path.join("UMUT","Error_Handle", "error_path_smaller_than_5.txt")
    write_array_to_txt_file(write_txt_path, paths_of_correct_files_smaller_than_5)

if __name__ == "__main__":
    main(folder_path="UMUT/casia-webface_FOLDERED")