import os
import sys
import cv2
import numpy as np
import shutil
import tensorflow

sys.path.insert(0,"UMUT/")

from media_pipe_operations import mediapipe_API
import path_operations
import image_operations_c
folder_cnt = 0
# böyle bir aşkı bitirebilir mi ne sanıyorsun

class Image:
    def __init__(self, path: str, image: np.ndarray =None, features: dict = {}):
        """
            Image object for the classification process.

            Args:
                path (str): Path to the image
                image (np.ndarray): Image object
                features (dict): Features of the image

            Returns:
                None
        """

        # Set the path, it is essential
        self.path = path

        # If the image is not provided, read it from the path
        self.image = cv2.imread(path) if image is None else image

        self.image_shape = self.image.shape
        
        for key, value in mediapipe_API.get_evaluated_features(self.image).items():
            self.add_attribute(key, value)
        
        for key, value in features.items():
            self.add_attribute(key, value)
    
    def __str__(self):
        return f"Summary of the image:\nPath: {self.path}\nID: {self.id}\nInter: {self.inter}\
            \nExtension: {self.extension}\nImage Shape: {self.image_shape}\n\nTo see all the attributes, use print_attributes() method."
    # add .self attribute
    def add_attribute(self, attribute: str, value: any) -> None:
        self.__setattr__(attribute, value)
    def print_attributes(self) -> None:
        for key, value in self.__dict__.items():
            print(f"{key}: {str(value)[:100]}{'...' if  len(str(value)) > 100 else ''}")

    def get_frontal_score(self) -> float:
        """
            Get the frontal score of the image.

            Args:
                None

            Returns:
                float: Frontal score of the image
        """
        score = {}        
        # It should be close to 0
        score["headpose_avg"] = self.head_pose_angles["average_abs_angle"]
        # They should be close to 90
        score["nose_angle_min"] = self.nose_angle_arr["min_abs_angle"]
        score["nose_angle_max"] = self.nose_angle_arr["max_abs_angle"]

        return score

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
        if "4295" in root:
            print("Here")
        img_count = get_img_file_count(files)

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
                
                img_buffer.add_attribute(
                    "avg_image_colors",
                    image_operations_c.calculate_avg_color_of_slices(img_buffer.image, 5, 5)
                )

                image_objects.append(img_buffer)

                if last_file_flag:
                    print(f"\nProcessing {root} \nImage Count: {len(image_objects)}")
                    difference_vector = image_operations_c.get_difference_of_avg_colors(image_objects)
                    difference_vector.sort(key=lambda x: x["Result"])
                    avg_diff = get_avg_difference(difference_vector)
                    threshold = avg_diff//3

                    print(f"Average difference: {avg_diff}")
                    print(f"Threshold: {threshold}")
                    
                    groups = create_groups(
                        result_sorted=difference_vector,
                        min_group_limit=3,
                        threshold=threshold,
                        print_flag=True
                    )

                    #result_sorted = sorted( image_operations_c.get_similarity(image_objects) , key=lambda x: x["Result"]["distance"] )
                    #groups = create_groups(result_sorted=result_sorted, min_group_limit=5, threshold=0.7)

                    delete_group_folders(root)

                    build_group_folders(groups, print_flag=False)

                    image_objects = []

def get_avg_difference(difference_vector: list) -> float:
    """
        Get the average difference from the difference vector.

        Returns:
            float: Average difference
    """
    total = 0
    for elem in difference_vector:
        total += elem["Result"]
    return total / len(difference_vector)
def build_group_folders(groups: list, print_flag: bool = False, min_group_limit:int= 4) -> None:
    """
        Build the group folders.

        Args:
            groups (list): List of groups

        Returns:
            None
    """
    for group_index,group in enumerate(groups):
        if len(group) < min_group_limit-1:
            print(f"{group_index}. group has {len(group)} element!")
            input("Press enter to continue ...")

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

def delete_group_folders(folder_path: str) -> None:
    """
        Delete the old group folders.

        Returns:
            None
    """
    for folder_name in os.listdir(folder_path):
        if "group" in folder_name:
            shutil.rmtree(os.path.join(folder_path, folder_name))

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
    while i<len(result_sorted): #len( [ True for group in groups if len(group) > min_group_limit] ) < min_group_count:
        if i == len(result_sorted):
            break
        elem = result_sorted[i]
        i+=1
        
        all_objects = []
        for group in groups:
            for obj in group:
                all_objects.append(obj)

        obj1_exists = elem["Obj1"] in all_objects
        obj2_exists = elem["Obj2"] in all_objects

        if elem["Result"] > threshold:
            continue_count += 1
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
    
    # Limit gropus
    groups = [group for group in groups if len(group) >= min_group_limit]

    print(f"Group Count (Filtered): {len(groups)}") if print_flag else None
    print(f"Continue Count: {continue_count}") if print_flag else None

    return groups
                
def get_img_file_count(files: list) -> int:
    count = 0
    for file in files:
        count = count+1 if file.endswith(".jpg") else count 
    return count


if __name__ == "__main__":
    main(src_path    = "src/dataset-casia-webface" ,
         target_path = "src/dataset-casia-webface-classified" )