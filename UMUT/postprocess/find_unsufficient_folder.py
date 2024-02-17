import os 

def count_path_slices(path):
    # Normalize the path to handle both forward and backward slashes
    path = os.path.normpath(path)
    # Split the path into directory slices
    slices = path.split(os.sep)
    # Count the number of slices
    return len(slices)

def main(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if len(files) < 100:
            if count_path_slices(root) > 4:
                print(root, len(files),count_path_slices(root))

if __name__ == "__main__":
    main("UMUT/Two_Face_Handle/Output_copy")