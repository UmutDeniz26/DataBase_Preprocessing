import cv2
import numpy as np
import common
import mediapipe as mp

from media_pipe import face_mesh

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_nose_landmarks(results):
    nose_landmarks = [ 
                results.multi_face_landmarks[0].landmark[1],
                results.multi_face_landmarks[0].landmark[4],
                results.multi_face_landmarks[0].landmark[5],
                results.multi_face_landmarks[0].landmark[195],
                results.multi_face_landmarks[0].landmark[197],
                results.multi_face_landmarks[0].landmark[6] 
        ]
    return nose_landmarks

def get_center_of_eyes(landmarks):
    center_of_right_eye = (landmarks[33].x + landmarks[133].x) / 2, (landmarks[33].y + landmarks[133].y) / 2
    center_of_left_eye = (landmarks[362].x + landmarks[263].x) / 2, (landmarks[362].y + landmarks[263].y) / 2
    return center_of_left_eye, center_of_right_eye


import mediapipe as mp
def head_pose_estimation(results: object, image: np.ndarray) -> tuple:
    """
        Estimates the head pose of the person in the image and returns the result as a tuple.

        Args:
            results (object): Results of the face mesh
            image (np.ndarray): Image of the person

        Returns:
            tuple: Tuple of the head pose angles
    """
    if not results.multi_face_landmarks:
        return None
    
    landmarks = results.multi_face_landmarks[0]  # Assuming there's only one face in the image

    face_2d = []
    face_3d = []

    for idx, lm in enumerate(landmarks.landmark):
        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291:
            if idx == 1:
                nose_2d = (lm.x * image.shape[1], lm.y * image.shape[0])
                nose_3d = (lm.x * image.shape[1], lm.y * image.shape[0], lm.z * 3000)
            x, y = int(lm.x * image.shape[1]), int(lm.y * image.shape[0])

            face_2d.append([x, y])
            face_3d.append(([x, y, lm.z]))

    # Get 2d Coord
    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)

    focal_length = 1 * image.shape[1]

    cam_matrix = np.array([[focal_length, 0, image.shape[0] / 2],
                           [0, focal_length, image.shape[1] / 2],
                           [0, 0, 1]])
    distortion_matrix = np.zeros((4, 1), dtype=np.float64)

    success, rotation_vec, translation_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, distortion_matrix)

    # Getting rotational of face
    rmat, jac = cv2.Rodrigues(rotation_vec)

    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

    x = angles[0] * 360
    y = angles[1] * 360
    z = angles[2] * 360

    return x, y, z


def calculate_nose_perpendicular_angle(nose_landmarks: list):
    """
        Calculates the angles between the nose landmarks and returns the result as a list.

        Args:
            nose_landmarks (list): List of nose landmarks
    
        Returns:
            list: List of angles between the nose landmarks
    """

    result_angles = []
    for index, landmark in enumerate(nose_landmarks):
        if index == 0:
            continue        
        line_first_point = (nose_landmarks[index-1].x, nose_landmarks[index-1].y)
        line_second_point = (landmark.x, landmark.y)
        angle_betwee_points = common.calculate_angle_between_2_points(line_first_point, line_second_point)
        result_angles.append(angle_betwee_points)
    return result_angles

def get_results(image: np.ndarray) -> object:
    """
        Returns the results of the face mesh.

        Args:
            image (np.ndarray): Image to be processed

        Returns:
            object: Results of the face mesh
    """
    return face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )