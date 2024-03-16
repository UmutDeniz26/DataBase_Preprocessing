import os
import numpy as np
import cv2
import mediapipe as mp
import shutil
import matplotlib.pyplot as plt



FACEMESH_TESSELATION = mp.solutions.face_mesh.FACEMESH_TESSELATION
IMG_COUNT = 0
                                       
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    

FRONTAL_FACE_FOLDER_PATH = "src/frontal_faces"
ANGLES_TXT_PATH = "src/mediapipe/angles.txt"
FACE_DRAWINGS_FOLDER = "src/frontal"


# Custom imports
import common
import landmark_operations
import txt_operations
import folder_operations
import image_operations

txt_operations.clear_txt(ANGLES_TXT_PATH)

def main():
    dataset_path = "Esogu-sets/Esogu-sets/"
    target_path = "non-frontal-test"

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    folders = os.listdir(dataset_path)

    for folder in folders:
        files = os.listdir(os.path.join(dataset_path, folder))
        files_size = len(files)

        clip_frontal_faces_limit = files_size//2
       
        if files_size < 80:
            continue
        else:
            files_with_angles = []
            for file_name in files:
                image_path = os.path.join(dataset_path, folder, file_name)
                image = cv2.imread(image_path)
                try:
                    results = face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )
                    head_poses = landmark_operations.head_pose_estimation( results, image)
                    average_angle = common.calculate_abs_average( head_poses )
                    files_with_angles.append( (image_path, average_angle) )
                except Exception as e:
                    print("Error:", e)
                
            files_with_angles =  txt_operations.limit_angles_by_magnitude(files_with_angles, clip_frontal_faces_limit)
            for file_angle in files_with_angles:
                image_path = file_angle[0]
                target = os.path.join(target_path, folder)
                if not os.path.exists(target):
                    os.makedirs(target)
                shutil.copy(image_path, target)

    face_mesh.close()
    return 0

def write_angle(image_path: str) -> None:
    """
        Writes the maximum rotation angle and the maximum nose angle to the txt file.
    
        Args:
            image_path (str): Path of the folder that contains the images

        Returns:
            None
    """

    if image_path.endswith(".jpg") and "frontal" not in image_path.lower():    
        # Get image path and image
        image = cv2.imread(image_path)
        
        # Get results and head poses
        results = face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )

        if results.multi_face_landmarks is None:
            print("No face detected in ", image_path)
            return

        head_poses = landmark_operations.head_pose_estimation( results, image)
        nose_angles = landmark_operations.calculate_nose_perpendicular_angle(landmark_operations.get_nose_landmarks(results))
        
        max_rotation_angle = max( [abs(angle) for angle in head_poses] )
        max_nose_angle = max( [abs(angle) for angle in nose_angles] )
        

        txt_operations.add_to_txt(
            txt_path = ANGLES_TXT_PATH,
            data = f"{image_path:100} {max_rotation_angle:7.2f}  {max_nose_angle:7.2f}\n"
        )
                

def plot_images_with_txt_file(txt_path: str, row: int, col: int) -> None:
    """
        Plot the images with the given paths in the txt file.

        Args:
            txt_path (str): The path of the txt file that contains the image paths.
            row (int): The number of rows in the plot.
            col (int): The number of columns in the plot.

        Returns:
            None
    """
    with open(txt_path, "r") as f:
        lines = f.readlines()
    fig, axes = plt.subplots(row, col)
    for i in range(row):
        for j in range(col):
            img_path = lines[i*col+j].split(" ")[0]
            img = cv2.imread(img_path)
            axes[i,j].imshow(img)
            axes[i,j].axis("off")
    plt.show()

def draw_landmarks(img_path: str, zoom_scale: float = 1) -> None:
    """
        Draws the landmarks on the image and returns the image.

        Args:
            img_path (str): Path of the image
            zoom_scale (float): Scale of the zoom

        Returns:
            image (np.ndarray): Image with the landmarks

    """
    global FACEMESH_TESSELATION, IMG_COUNT
    IMG_COUNT += 1

    image = cv2.imread(img_path)
    results = face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )

    if results.multi_face_landmarks is None or image is None:
        return
    elif zoom_scale != 1:
        image = cv2.resize(image, (0, 0), fx=zoom_scale, fy=zoom_scale)
    
    image_width, image_height, _ = image.shape

    multi_face_landmarks = results.multi_face_landmarks[0]
    nose_landmarks = landmark_operations.get_nose_landmarks(results)
    center_of_eyes = landmark_operations.get_center_of_eyes(multi_face_landmarks.landmark)
    
    rotation_arr = landmark_operations.head_pose_estimation(results, image)
    nose_angle_arr = landmark_operations.calculate_nose_perpendicular_angle(nose_landmarks)
    nose_angle_arr = [abs(angle) for angle in nose_angle_arr]

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(
        image, multi_face_landmarks, FACEMESH_TESSELATION,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0),
        thickness=1, circle_radius=1)
    )

    # Red dots for the center of the eyes and the nose
    for eye in center_of_eyes:
        cv2.circle(image, (int(eye[0] * image.shape[1]), int(eye[1] * image.shape[0])), 5, (0, 0, 255), -1)
    
    # Draw lines between the nose landmarks
    for i,landmark in enumerate(nose_landmarks):
        if i == 0:
            continue
        line_first_point = (int(nose_landmarks[i-1].x * image.shape[1]), int(nose_landmarks[i-1].y * image.shape[0]))
        line_second_point = (int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]))
        cv2.line(image, line_first_point, line_second_point, (0, 0, 255), 2)

    # Determine if the face is frontal or not
    put_text_coordinates = ( int(image_width * 0.1), int(image_height * 0.05) )
    target_score = 90
    offset = 0.05
    if max(nose_angle_arr)<target_score+target_score*offset and min(nose_angle_arr)>target_score-target_score*offset:
        cv2.putText(image, "Frontal", put_text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(image, "Non-frontal", put_text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
    # Put text max nose angle and min nose angle
    put_text_coordinates = ( int(image_width * 0.05), int(image_height * 0.95) )
    cv2.putText(image, f"Max angle: {max(nose_angle_arr):.2f}", put_text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 50), 2, cv2.LINE_AA)
    put_text_coordinates = ( int(image_width * 0.55), int(image_height * 0.95) )
    cv2.putText(image, f"Min angle: {min(nose_angle_arr):.2f}", put_text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 50), 2, cv2.LINE_AA)

    # Center of bottom with larger font
    put_text_coordinates = ( int(image_width * 0.1), int(image_height * 0.15) )
    cv2.putText(image, f"Progress: {IMG_COUNT}", put_text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)

    return image
        
def itarate_over_images(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg"):
                #write_angle(os.path.join(root, file))
                image = draw_landmarks(os.path.join(root, file), 6)
                image_operations.show_image(image, "Image", 500)


if __name__ == "__main__":
    itarate_over_images("src/casia-raw")

    #main()
    #write_angle("UMUT\casia-webface_FOLDERED\Frontal_faces")
    #sort_angles("angles.txt")
    #plot_with_img_paths("angles.txt", 10, 10)
    #delete_txt_and_jpg("angles.txt", 100)
