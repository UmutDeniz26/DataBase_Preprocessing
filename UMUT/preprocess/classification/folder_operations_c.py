import os
import shutil
import headpose_operations_c

def delete_groups_in_folder(folder_path: str) -> None:
    """
        Delete the old group folders.

        Args:
            src_path (str): Path to the dataset

        Returns:
            None
    """
    if not os.path.exists(folder_path):
        return
    for folder_name in os.listdir(folder_path):
        if "group" in folder_name:
            shutil.rmtree(os.path.join(folder_path, folder_name))
      
def get_img_file_count(files: list) -> int:
    count = 0
    for file in files:
        if "group" in file or "frontal" in file:
            continue
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
        
        print("Group: ",group_index)
        headpose_response = headpose_operations_c.get_most_frontal_face(group)

        for obj in group:
            # Create the folder path
            group_slices = obj.path.split(os.sep)
            group_slices[-1] = f"group_{group_index}/{group_slices[-1]}"
            #group_slices.pop(-2)
            group_folder_path = os.path.normpath('/'.join(group_slices))
            group_folder_path = group_folder_path.replace(obj.source_path, obj.target_path)
            
            if False:#not headpose_response["valid_data"]:
                continue

            frontal_img = headpose_response["frontal_img"]
            
            if os.path.exists(group_folder_path):
                shutil.rmtree( os.path.dirname(group_folder_path) )
            
            os.makedirs(os.path.dirname(group_folder_path), exist_ok=True)
            shutil.copy(obj.path, group_folder_path)
            os.makedirs(os.path.join(os.path.dirname(group_folder_path), "frontal"), exist_ok=True)
            shutil.copy(frontal_img.path, os.path.join(os.path.dirname(group_folder_path), "frontal", os.path.basename(frontal_img.path)) )
            
            print(obj.path,"to",group_folder_path) if print_flag else None
        print("\n") if print_flag else None
