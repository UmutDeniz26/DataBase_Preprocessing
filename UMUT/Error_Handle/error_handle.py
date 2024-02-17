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

    for root, dirs, files in os.walk(folder_path):
        if len(files) < 100:
            large_folder_flag = True
        else:
            large_folder_flag = False

        print("Root: ", root)
        if count_path_slices(root) > 4:
            for file in files:
                if file.endswith(".txt"):
                    content = open(os.path.join(root, file)).read()
                    if delete_all_errors:
                        print("File path: ", os.path.join(root, file))
                        print("Content: ", content)
    

if __name__ == "__main__":
    main(folder_path="UMUT\Two_Face_Handle\HELEN_FOLDERED_copy", delete_all_errors=True)