import os
import sys
import cv2
import numpy as np
import shutil

sys.path.insert(0,"UMUT/")

from media_pipe_operations import mediapipe_API
import path_operations
import image_operations_c
import Common_c
import folder_operations_c


class Image:
    def __init__(self, path: str, image: np.ndarray =None, features: dict = {}):
        """
            Image object for the classification process.

            Args:
                path (str): Path to the image
                image (np.ndarray): Image object
                features (dict): Features of the image

        """

        # Set the path, it is essential
        self.path = path

        # If the image is not provided, read it from the path
        self.image = cv2.imread(path) if image is None else image

        self.image_shape = self.image.shape
        
        for key, value in mediapipe_API.get_evaluated_features(self.image).items():
            self.__setattr__(key, value)
        
        for key, value in features.items():
            self.__setattr__(key, value)
    
    def __str__(self):
        return f"Summary of the image:\nPath: {self.path}\nID: {self.id}\nInter: {self.inter}\
            \nExtension: {self.extension}\nImage Shape: {self.image_shape}\n\nTo see all the attributes, use print_attributes() method."
    
    def print_attributes(self) -> None:
        for key, value in self.__dict__.items():
            print(f"{key}: {str(value)[:100]}{'...' if  len(str(value)) > 100 else ''}")

    def get_frontal_score(self) -> float:
        return {
            "headpose_avg": self.head_pose_angles["average_abs_angle"],
            "nose_angle_min": self.nose_angle_arr["min_abs_angle"],
            "nose_angle_max": self.nose_angle_arr["max_abs_angle"]
            }

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
        img_count = folder_operations_c.get_img_file_count(files)

        for index, file in enumerate(files):
            last_file_flag = True if index == img_count - 1 else False

            if file.endswith(".jpg") and "group" not in root and "frontal" not in root:
                img_path = os.path.join(root, file)
                
                
                slices = path_operations.get_path_slices(img_path)
                features = path_operations.get_path_features(slices)

                img_buffer = Image(
                    path=img_path,
                    features=features
                )
                
                img_buffer.__setattr__(
                    "avg_image_colors",
                    image_operations_c.calculate_avg_color_of_slices(img_buffer.image, 5, 5)
                )

                image_objects.append(img_buffer)

                if last_file_flag:
                    print(f"\nProcessing {root} \nImage Count: {len(image_objects)}")
                    difference_vector = image_operations_c.get_difference_of_avg_colors(image_objects)
                    difference_vector.sort(key=lambda x: x["Result"])
                    avg_diff = Common_c.get_avg_difference(difference_vector)
                    threshold = avg_diff//2

                    print(f"Average difference: {avg_diff}")
                    print(f"Threshold: {threshold}")
                    groups = create_groups(result_sorted=difference_vector, min_group_limit=5, threshold=threshold, print_flag=True)

                    #result_sorted = sorted( image_operations_c.get_similarity(image_objects) , key=lambda x: x["Result"]["distance"] )
                    
                    #groups = create_groups(result_sorted=result_sorted, min_group_limit=5, threshold=0.7)
                    
                    folder_operations_c.delete_old_group_folders(root)

                    folder_operations_c.build_group_folders(groups, print_flag=False)

                    image_objects = []


def create_groups(result_sorted: list, min_group_limit: int, threshold: float, print_flag: bool = False) -> list:
    """
        Create groups from the sorted result list.

        Args:
            result_sorted (list): Sorted result list
            min_group_limit (int): Minimum number of elements in a group
            threshold (float): Threshold for the distance, if smaller than this, the elements are in the same group

        Returns:
            list: List of groups
    """
    # Initialize the groups list
    groups = [];i=0
    continue_count = 0

    # Number of groups that have more than 5 elements. If there are more than 2 groups like that, continue.    
    all_objects = []
    while i<len(result_sorted): #len( [ True for group in groups if len(group) > min_group_limit] ) < min_group_count:
        if i == len(result_sorted):
            break
        elem = result_sorted[i]
        i+=1
        
        obj1_exists = elem["Obj1"] in all_objects
        obj2_exists = elem["Obj2"] in all_objects

        if elem["Result"] > threshold:
            continue_count += 1
            continue

        if not obj1_exists and not obj2_exists: #and len(groups) < max_group_count:
            groups.append([elem["Obj1"], elem["Obj2"]])
            all_objects.append(elem["Obj1"]);all_objects.append(elem["Obj2"])
        
        elif obj1_exists and elem["Obj2"] not in all_objects:
            for group in groups:
                if elem["Obj1"] in group:
                    group.append(elem["Obj2"]);all_objects.append(elem["Obj2"])
                    break
        
        elif obj2_exists and elem["Obj1"] not in all_objects:
            for group in groups:
                if elem["Obj2"] in group:
                    group.append(elem["Obj1"]);all_objects.append(elem["Obj1"])
                    break

    # Remove the groups that have less than 5 elements
    for group in groups:
        if len(group) < min_group_limit:
            groups.remove(group)

    print(f"Group Count (Filtered): {len(groups)}") if print_flag else None
    print(f"Continue Count: {continue_count}") if print_flag else None

    return groups
          
if __name__ == "__main__":
    main("src/foldered", "src/foldered")