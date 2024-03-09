import os 
import sys
import json
sys.path.insert(0, './UMUT')

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

def main(folder_path, delete_all_errors=False):
    large_folder_flag = False

    total_folder_count = 0;index = 0;error_count = 0
    paths_of_correct_files_smaller_than_5 = [];info_of_correct_files_smaller_than_5 = []
    files_to_delete = []

    for root, dirs, files in os.walk(folder_path):
        total_folder_count += 1

    for root, dirs, files in os.walk(folder_path):
        print(f"\n\n\nProgress: {(index/total_folder_count)*100:.2f}%", end="\r")
        os.system('clear')
        index+=1

        # if frontal folder pass
        if "frontal" in root:
            continue   

        error_count = 0
        if count_path_slices(root,folder_path) == 2:
            temp_error_files = []
            for file in files:
                if file.endswith(".txt"):
                    txt_path = os.path.join(root, file)
                    img_path = txt_path.replace(".txt", ".jpg")
                    with open(txt_path, "r") as f:
                        content = f.read()
                        
                    if "pass_exception" in content:
                        continue

                    if "Error" in content or "Stack Overflow" in content or "too small"\
                        in content or "LandmarkError" in content or "Response" in content:
                        if delete_all_errors:
                            temp_error_files.append(img_path)
                            temp_error_files.append(txt_path)
                            error_count += 1
                    
            correct_files = len(files)/2 - error_count

            ##########################################################################3
            string = (f"Error count: {error_count}  "
                          f"Total files: {len(files)}  "
                          f"Correct files: {int(correct_files)}  "
                          f"Folder path: {root}")
            
            if correct_files < 5:
                info_of_correct_files_smaller_than_5.append(string)
                for file in temp_error_files:
                    paths_of_correct_files_smaller_than_5.append(file)       
            else:
                with open(os.path.join("UMUT","Error_Handle", "error_greater_than_5.txt"), "a") as f:
                    f.write(f"{string}\n")
        
                for file in temp_error_files:
                    if delete_all_errors:
                        
                        img_path = file.replace(".txt", ".jpg")
                        txt_path = file

                        if os.path.exists(img_path) and os.path.exists(txt_path):
                            #os.remove(img_path)
                            files_to_delete.append(img_path)
                            #os.remove(txt_path)
                            files_to_delete.append(txt_path)
                        else:
                            print(f"Files does not exist: {img_path}")
                            exit()

    with open(os.path.join("UMUT","Error_Handle", "files_to_delete.txt"), "a") as f:
        for item in files_to_delete:
            f.write("%s\n" % item)
    
    write_txt_path = os.path.join("UMUT","Error_Handle", "error.txt")
    with open(write_txt_path, "w") as f:
        for item in info_of_correct_files_smaller_than_5:
            f.write("%s\n" % item)
    
    write_txt_path = os.path.join("UMUT","Error_Handle", "error_paths.txt")
    with open(write_txt_path, "w") as f:
        for item in paths_of_correct_files_smaller_than_5:
            f.write("%s\n" % item)
            

if __name__ == "__main__":
    main(folder_path="casia-webface_FOLDERED", delete_all_errors=False)