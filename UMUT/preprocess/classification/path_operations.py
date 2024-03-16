import os
import cv2

def get_path_slices(path: str) -> list:
    """
        Splits the path into slices.

        Args:
            path (str): Path to be split

        Returns:
            list: List of the slices
    """
    slices = os.path.normpath(path).split(os.sep)    
    for index, elem in enumerate(slices):
        if "." in elem:
            slices[index] = elem.split(".")[0]
            slices.append(elem.split(".")[1])
    return slices

def get_path_features(slices: list) -> dict:
    """
        Extracts the features from the path.

        Args:
            slices (list): List of the slices

        Returns:
            dict: Dictionary of the features
    """
    features = {}
    features["extension"] = slices[-1]
    features["id"] = slices[-2]
    features["inter"] = slices[-3]
    return features