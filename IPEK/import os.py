import os
import shutil

def count_images_in_folder(folder_path):
    """
    Counts the number of images (files with .jpg extension) in the given folder.
    """
    image_count = sum(1 for file in os.listdir(folder_path) if file.lower().endswith('.jpg'))
    return image_count

def process_folders(folder_path, output_file):
    """
    Deletes folders with less than four images and records the names of the remaining folders in another file.
    """
    # Open the output file to record folder names
    with open(output_file, 'w') as output:
        # Iterate over folders in the specified path
        for folder_name in os.listdir(folder_path):
            folder_full_path = os.path.join(folder_path, folder_name)
            # Check if the path is a directory
            if os.path.isdir(folder_full_path):
                image_count = count_images_in_folder(folder_full_path)
                # If there are four or more images, record the folder name
                if image_count >= 4:
                    output.write(folder_name + '\n')
                else:
                    # If there are fewer than four images, delete the folder
                    print(f"Deleting folder: {folder_full_path}")
                    try:
                        shutil.rmtree(folder_full_path)
                        print(f"Folder deleted: {folder_full_path}")
                    except Exception as e:
                        print(f"Error deleting folder {folder_full_path}: {str(e)}")

# Define your folder path and the path to the text file to record folder names
folder_path = r"C:\Users\ipekb\Desktop\file detect\lfw-deepfunneled"
output_file = "selected_folders.txt"

# Process the folders
process_folders(folder_path, output_file)
