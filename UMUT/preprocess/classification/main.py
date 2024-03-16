import os
import sys
import cv2

sys.path.insert(0,"UMUT/")

from media_pipe_operations import mediapipe_API
import path_operations

class Image:
    def __init__(self, path: str, features: dict):
        self.path = path
        self.image = cv2.imread(path)
        self.features = features
        self.evaluated_features = mediapipe_API.get_evaluated_features(self.image)
    
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

            if file.endswith(".jpg"):
                img_path = os.path.join(root, file)
                slices = path_operations.get_path_slices(img_path)
                features = path_operations.get_path_features(slices)
                image_objects.append(Image(img_path, features))
                                
                if last_file_flag:
                    print(f"Processing {root} \nLen: {len(image_objects)}")
                    image_objects = []

                
def get_img_file_count(files: list) -> int:
    count = 0
    for file in files:
        count = count+1 if file.endswith(".jpg") else count 
    return count


if __name__ == "__main__":
    main("src/casia-raw", "src/casia-classified")