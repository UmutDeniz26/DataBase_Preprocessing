import sys
sys.path.insert(0,"UMUT/media_pipe_operations")

import numpy as np
import cv2
import mediapipe as mp
import landmark_operations
import common

def get_evaluated_features(image:np.ndarray) -> dict:
    """
        Evaluates the features of the images with the model.

        Args:
            image (np.ndarray): Image to be evaluated

        Returns:
            dict: Dictionary of the evaluated features
    """
    evaluated_features = {}

    results = landmark_operations.face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )
    if results.multi_face_landmarks is None or image is None:
        return evaluated_features
    
    nose_landmarks = landmark_operations.get_nose_landmarks(results)
    
    head_pose_angles = landmark_operations.head_pose_estimation(results, image)
    average_angle = common.calculate_abs_average(head_pose_angles)
    center_of_eyes = landmark_operations.get_center_of_eyes(results.multi_face_landmarks[0].landmark)
    nose_angle_arr = landmark_operations.calculate_nose_perpendicular_angle(nose_landmarks)
    
    evaluated_features["nose_angle_arr"] = {"angles": nose_angle_arr, "max_abs_angle": max([abs(angle) for angle in nose_angle_arr]),"min_abs_angle": min([abs(angle) for angle in nose_angle_arr])}
    evaluated_features["head_pose_angles"] = {"angles": head_pose_angles, "average_abs_angle": average_angle}
    evaluated_features["center_of_eyes"] = center_of_eyes

        
    return evaluated_features