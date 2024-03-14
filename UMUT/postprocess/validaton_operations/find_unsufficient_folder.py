import os 

def count_path_slices(path,folder_path):
    # Normalize the path to handle both forward and backward slashes
    path = os.path.normpath(path)
    path = path.replace(folder_path,"")

    # Split the path into directory slices
    slices = path.split(os.sep)
    # Count the number of slices
    return len(slices)

def main(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if count_path_slices(root,folder_path) > 4:
            print(root, len(files),count_path_slices(root))

if __name__ == "__main__":
    main("UMUT\casia-webface_FOLDERED")