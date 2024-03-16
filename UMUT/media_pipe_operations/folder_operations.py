import os

import txt_operations

def delete_files_by_txt_path(txt_path: str, delete_count: int) -> None:
    """
        Deletes the first delete_count lines from the txt file and the corresponding images.
    
        Args:
            txt_path (str): Path of the txt file
            delete_count (int): Number of lines to be deleted from the txt file

        Returns:
            None
    """

    # Read the lines of the txt file
    lines = txt_operations.read_lines(txt_path)
    validation = "n"

    # Delete the first delete_count lines
    for i in range(delete_count):
        # Replace Frontal_faces part
        img_path_slices = lines[i].split(" ")[0].split(".")[0].split("\\")[-1].split("_")
        path = lines[i].split(" ")[0]
        img_path = path.replace("Frontal_faces", f"{img_path_slices[0]}\\{img_path_slices[1]}")
        txt_path = img_path.replace(".jpg", ".txt")

        if validation =="n":
            validation = input(f"Are you sure you want to delete\n{img_path} and {txt_path}? (y/n): ")
        elif validation == "y":
            os.remove(img_path)
            os.remove(txt_path)
        else:
            print("Invalid input. Exiting...")
            return