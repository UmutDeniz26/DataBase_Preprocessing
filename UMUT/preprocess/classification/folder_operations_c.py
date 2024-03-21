import os
import shutil


def delete_old_group_folders(folder_path: str) -> None:
    """
        Delete the old group folders.

        Args:
            src_path (str): Path to the dataset

        Returns:
            None
    """
    for folder_name in os.listdir(folder_path):
        if "group" in folder_name:
            shutil.rmtree(os.path.join(folder_path, folder_name))

      
def get_img_file_count(files: list) -> int:
    count = 0
    for file in files:
        count = count+1 if file.endswith(".jpg") else count 
    return count


def build_group_folders(groups: list, print_flag: bool = False) -> None:
    """
        Build the group folders.

        Args:
            groups (list): List of groups

        Returns:
            None
    """
    for group_index,group in enumerate(groups):
        for obj in group:
            # Create the folder path
            group_slices = obj.path.split(os.sep)
            group_slices[-1] = f"group_{group_index}/{group_slices[-1]}"
            group_folder_path = os.path.normpath('/'.join(group_slices))
            
            if not os.path.exists(group_folder_path):
                os.makedirs(os.path.dirname(group_folder_path), exist_ok=True)
            else:
                shutil.rmtree( os.path.dirname(group_folder_path) )
                os.makedirs(os.path.dirname(group_folder_path), exist_ok=True)
            shutil.copy(obj.path, group_folder_path)
            
            print(obj.path) if print_flag else None
        print("\n") if print_flag else None
