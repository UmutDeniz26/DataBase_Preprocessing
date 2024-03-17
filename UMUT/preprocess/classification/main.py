import os
import sys
import cv2
import numpy as np
import shutil

sys.path.insert(0,"UMUT/")

from media_pipe_operations import mediapipe_API
import path_operations
import image_operations_c


class Image:
    def __init__(self, path: str, image: np.ndarray =None, features: dict = {}):
        self.path = path
        if image is None:
            self.image = cv2.imread(path)
        else:
            self.image = image
        
        for key, value in mediapipe_API.get_evaluated_features(self.image).items():
            self.add_attribute(key, value)
        
        for key, value in features.items():
            self.add_attribute(key, value)
    
    def __str__(self):
        return f"Path: {self.path} \nFeatures: {self.features} \nEvaluated Features: {self.evaluated_features} \n\n"

    # add .self attribute
    def add_attribute(self, attribute: str, value: any) -> None:
        self.__setattr__(attribute, value)
    
    def print_attributes(self) -> None:
        for key, value in self.__dict__.items():
            print(f"{key}: {str(value)[:100]}{'...' if  len(str(value)) > 100 else ''}")
            
def main(src_path: str, target_path: str)-> None:
    """
        Main function for the classification process.

        Args:
            src_path (str): Path to the dataset
            target_path (str): Path to the target folder

        Returns:
            None
    """
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    image_objects = []
    for root, _, files in os.walk(src_path):
        img_count = get_img_file_count(files)

        for index, file in enumerate(files):
            last_file_flag = True if index == img_count - 1 else False

            if file.endswith(".jpg") and "group" not in root:
                img_path = os.path.join(root, file)
                
                img_buffer = Image(
                    path=img_path,
                )
                
                slices = path_operations.get_path_slices(img_path)
                features = path_operations.get_path_features(slices)

                for key, value in features.items():
                    img_buffer.add_attribute(key, value)

                img_buffer.add_attribute(
                    "avg_image_colors",
                    image_operations_c.calculate_avg_color_of_slices(img_buffer.image, 15, 15)
                )

                image_objects.append(img_buffer)

                if last_file_flag:
                    print(f"\nProcessing {root} \nImage Count: {len(image_objects)}")
                    #difference_vector = image_operations_c.get_difference_of_avg_colors([image.features["avg_image_colors"] for image in image_objects])
                    #difference_vector.sort(key=lambda x: x["diff"])

                    result_sorted = sorted( image_operations_c.get_similarity(image_objects) , key=lambda x: x["Result"]["distance"] )
                    
                    groups = create_groups(result_sorted=result_sorted, min_group_limit=5, threshold=0.7)
                    
                    build_group_folders(groups, print_flag=True)

                    image_objects = []

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


def create_groups(result_sorted: list, min_group_limit: int, threshold: float) -> list:
    """
        Create groups from the sorted result list.

        Args:
            result_sorted (list): Sorted result list
            min_group_limit (int): Minimum number of elements in a group
            threshold (float): Threshold for the distance

        Returns:
            list: List of groups
    """
    # Initialize the groups list
    groups = [];i=0

    # Number of groups that have more than 5 elements. If there are more than 2 groups like that, continue.
    while i<len(result_sorted): #len( [ True for group in groups if len(group) > min_group_limit] ) < min_group_count:
        i+=1
        if i == len(result_sorted):
            break
        elem = result_sorted[i]
        
        all_objects = []
        for group in groups:
            for obj in group:
                all_objects.append(obj)

        obj1_exists = elem["Obj1"] in all_objects
        obj2_exists = elem["Obj2"] in all_objects

        if elem["Result"]["distance"] < threshold:
            continue

        if not obj1_exists and not obj2_exists: #and len(groups) < max_group_count:
            groups.append([elem["Obj1"], elem["Obj2"]])
        elif obj1_exists and elem["Obj2"] not in all_objects:
            for group in groups:
                if elem["Obj1"] in group:
                    group.append(elem["Obj2"])
                    break
        elif obj2_exists and elem["Obj1"] not in all_objects:
            for group in groups:
                if elem["Obj2"] in group:
                    group.append(elem["Obj1"])
                    break
        
    groups = [group for group in groups if len(group) >= min_group_limit]
    return groups
                
def get_img_file_count(files: list) -> int:
    count = 0
    for file in files:
        count = count+1 if file.endswith(".jpg") else count 
    return count


if __name__ == "__main__":
    main("src/casia-raw", "src/casia-classified")