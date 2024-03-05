import os 
import sys
sys.path.insert(0, './UMUT')

def count_path_slices(path):
    # Normalize the path to handle both forward and backward slashes
    path = os.path.normpath(path)
    # Split the path into directory slices
    slices = path.split(os.sep)
    # Count the number of slices
    return len(slices)

def main(folder_path, delete_all_errors=False):
    large_folder_flag = False

    total_folder_count = 0;index = 0;error_count = 0
    error_info_paths = [];error_info = [];deleted_files = []

    for root, dirs, files in os.walk(folder_path):
        total_folder_count += 1

    for root, dirs, files in os.walk(folder_path):
        percentage = (index/total_folder_count)*100
        print(f"\n\n\nProgress: {percentage:.2f}%", end="\r")
        index+=1

        # if frontal folder pass
        if "frontal" in root:
            continue   

        error_count = 0
        if count_path_slices(root) > 4:
            temp_error_files = []
            for file in files:
                if file.endswith(".txt"):
                    txt_path = os.path.join(root, file)
                    img_path = txt_path.replace(".txt", ".jpg")
                    content = open(os.path.join(root, file)).read()

                    if "pass_exception" in content:
                        continue

                    if "Error" in content or "Stack Overflow" in content or "too small" in content or "LandmarkError" in content:
                        if delete_all_errors:
                            temp_error_files.append(img_path)
                            temp_error_files.append(txt_path)
                            error_count += 1
            try:
                ratio = error_count/ (len(files)/2)
            except ZeroDivisionError:
                print(f"Error: {root}")
                ratio = 0
            correct_files = len(files)/2 - error_count
            
            if correct_files < 5:
                string = (f"Error count: {error_count}  "
                          f"Total files: {len(files)}  "
                          f"Ratio: {ratio}  "
                          f"Correct files: {int(correct_files)}  "
                          f"Folder path: {root}")
                #print(string)
                error_info.append(string)
                for file in temp_error_files:
                    error_info_paths.append(file)       
            else:
                for file in files:
                    if file.endswith(".txt"):
                        txt_path = os.path.join(root, file)
                        img_path = txt_path.replace(".txt", ".jpg")
                        with open(txt_path, "r") as f:
                            content = f.read()

                        if "pass_exception" in content:
                            continue

                        if "Error" in content or "Stack Overflow" in content or "too small" in content or "LandmarkError" in content:
                            if delete_all_errors:
                                if os.path.exists(img_path) and os.path.exists(txt_path):
                                    os.remove(img_path)
                                    deleted_files.append(img_path)
                                    os.remove(txt_path)
                                    deleted_files.append(txt_path)
                                else:
                                    print(f"Files does not exist: {img_path}")
                                    exit()

    with open("deleted_files.txt", "w") as f:
        for item in deleted_files:
            f.write("%s\n" % item)
    
    write_txt_path = os.path.join("UMUT","Error_Handle", "error.txt")
    with open(write_txt_path, "w") as f:
        for item in error_info:
            f.write("%s\n" % item)
    
    write_txt_path = os.path.join("UMUT","Error_Handle", "error_paths.txt")
    with open(write_txt_path, "w") as f:
        for item in error_info_paths:
            f.write("%s\n" % item)
            

if __name__ == "__main__":
    main(folder_path="UMUT/database/HELEN_FOLDERED", delete_all_errors=True)