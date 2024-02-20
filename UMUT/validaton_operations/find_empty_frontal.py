import os


def main(folder_path):
    frontal_faces = []
    src_paths = []
    for root_path, dir_names, file_names in os.walk(folder_path):
        if "frontal" in os.path.join(root_path).lower():
            number_of_files = len(file_names)
            if number_of_files != 1:
                print(f"Number of files in {root_path}: {number_of_files}")
        else:
            continue

if __name__ == "__main__":
    main(folder_path="UMUT/database/HELEN")
