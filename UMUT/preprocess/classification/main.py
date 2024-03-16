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
    def __init__(self, path: str, features: dict, image: np.ndarray = None):
        self.path = path
        if image is None:
            self.image = cv2.imread(path)
        else:
            self.image = image

        self.features = features
        for key, value in mediapipe_API.get_evaluated_features(self.image).items():
            self.features[key] = value

    
    def __str__(self):
        return f"Path: {self.path} \nFeatures: {self.features} \nEvaluated Features: {self.evaluated_features} \n\n"
    

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

    hold_inter = "";hold_id = "";image_objects = []
    for root, dirs, files in os.walk(src_path):
        img_count = get_img_file_count(files)

        for index, file in enumerate(files):
            last_file_flag = True if index == img_count - 1 else False

            if file.endswith(".jpg") and "group" not in root:
                img_path = os.path.join(root, file)
                image = cv2.imread(img_path)
                slices = path_operations.get_path_slices(img_path)
                features = path_operations.get_path_features(slices)
                #avg_image_colors = image_operations_c.calculate_avg_color_of_slices(image, 15, 15)    
                #features["avg_image_colors"] = avg_image_colors

                image_objects.append(Image(img_path, features, image))

                if last_file_flag:
                    print(f"\nProcessing {root} \nImage Count: {len(image_objects)}")
                    #difference_vector = image_operations_c.get_difference_of_avg_colors([image.features["avg_image_colors"] for image in image_objects])
                    #difference_vector.sort(key=lambda x: x["diff"])

                    result = image_operations_c.get_similarity(image_objects)
                    result_sorted = sorted(result, key=lambda x: x["Result"]["distance"])

                    groups = [];i=0

                    min_group_limit = 3 # Minimum number of elements in a group
                    max_group_count = 2 # Number of groups that have more than 5 elements. If there are more than 2 groups like that, continue.
                    min_group_count = 2 # Number of groups that have more than 5 elements. If there are more than 2 groups like that, continue.

                    # Number of groups that have more than 5 elements. If there are more than 2 groups like that, continue.
                    while len( [ True for group in groups if len(group) > min_group_limit] ) < min_group_count:
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

                        if not obj1_exists and not obj2_exists and len(groups) < max_group_count:
                            groups.append([elem["Obj1"], elem["Obj2"]])
                        elif obj1_exists:
                            for group in groups:
                                if elem["Obj1"] in group and elem["Obj2"] not in all_objects:
                                    group.append(elem["Obj2"])
                                    break
                        elif obj2_exists:
                            for group in groups:
                                if elem["Obj2"] in group and elem["Obj1"] not in all_objects:
                                    group.append(elem["Obj1"])
                                    break

                    # Remove the groups that have less than 3 elements
                    groups = [group for group in groups if len(group) > min_group_limit]

                    # Create the folders and copy the files
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
                            
                            print(obj.path)
                        print("\n")
                    print("Processed file count: ", i)
                    image_objects = []

                
def get_img_file_count(files: list) -> int:
    count = 0
    for file in files:
        count = count+1 if file.endswith(".jpg") else count 
    return count


if __name__ == "__main__":
    main("src/casia-raw", "src/casia-classified")