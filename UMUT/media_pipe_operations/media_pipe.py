import os
import numpy as np
import cv2
import mediapipe as mp
import shutil
import matplotlib.pyplot as plt

# Custom imports
import common
import landmark_operations
import txt_operations
import folder_operations


FACEMESH_TESSELATION = mp.solutions.face_mesh.FACEMESH_TESSELATION
IMG_COUNT = 0
TOTAL_IMG_COUNT = 501000
                                       
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    

FRONTAL_FACE_FOLDER_PATH = "src/frontal_faces"
ANGLES_TXT_PATH = "src/mediapipe/angles.txt"
FACE_DRAWINGS_FOLDER = "src/frontal"

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

def write_angle(folder_path: str) -> None:
    """
        Write the angles of the images in the folder to a txt file.

        Args:
            folder_path (str): The path of the folder that contains the images.
        
        Returns:
            None
    """
    txt_operations.clear_txt(ANGLES_TXT_PATH)

    for root, _, files in os.walk(folder_path):
        for file in files:
            image_path = os.path.join(root, file)

            if file.endswith(".jpg") and "frontal" not in image_path.lower():    
                # Get image path and image
                image = cv2.imread(image_path)
                
                # Get results and head poses
                results = face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )
                head_poses = landmark_operations.head_pose_estimation( results, image)
                average_angle = 999 if head_poses is None else common.calculate_abs_average( head_poses )
                
                txt_operations.add_to_txt(
                    txt_path = ANGLES_TXT_PATH,
                    data = f"{image_path} {average_angle}\n"
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

def draw_landmarks(image, results, zoom_scale=1, image_path=None, show_flag = True):
    global FACEMESH_TESSELATION, IMG_COUNT, FRONTAL_FACE_FOLDER_PATH
    IMG_COUNT += 1

    if results.multi_face_landmarks is None or image is None:
        return

    if zoom_scale != 1 and show_flag:
        image = cv2.resize(image, (0, 0), fx=zoom_scale, fy=zoom_scale)
    
    multi_face_landmarks = results.multi_face_landmarks[0]
    
    avg_rotation_angle, average_of_result_angles = calculate_rotation_avg_angle_avg(image_path)
    center_of_eyes = landmark_operations.get_center_of_eyes(multi_face_landmarks.landmark)
    
    # It can be changed instead of being embedded in the function.
    # Right now it's a constant value.
    os.makedirs(FRONTAL_FACE_FOLDER_PATH, exist_ok=True)

    progress = round(IMG_COUNT / TOTAL_IMG_COUNT * 100, 3)

    if show_flag:
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(
            image, multi_face_landmarks, FACEMESH_TESSELATION,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0),
            thickness=1, circle_radius=1))
        
        nose_landmarks = landmark_operations.get_nose_landmarks(results)

        for eye in center_of_eyes:
            cv2.circle(image, (int(eye[0] * image.shape[1]), int(eye[1] * image.shape[0])), 5, (0, 0, 255), -1)
        cv2.circle(image, (int(nose_landmarks[0].x * image.shape[1]), int(nose_landmarks[0].y * image.shape[0])), 5, (0, 0, 255), -1)
        cv2.circle(image, (int(nose_landmarks[-1].x * image.shape[1]), int(nose_landmarks[-1].y * image.shape[0])), 5, (0, 0, 255), -1)

        for i,landmark in enumerate(nose_landmarks):
            if i == 0:
                continue
            line_first_point = (int(nose_landmarks[i-1].x * image.shape[1]), int(nose_landmarks[i-1].y * image.shape[0]))
            line_second_point = (int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]))
            cv2.line(image, line_first_point, line_second_point, (0, 0, 255), 2)

        cv2.putText(image, f"Average: {avg_rotation_angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, f"Average of nose perpendicular: {average_of_result_angles:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
        # Center of bottom with larger font
        cv2.putText(image, f"Progress: {progress}%", (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)

        os.makedirs("src/frontal") if not os.path.exists("src/frontal") else None
        new_img_path = os.path.join(FACE_DRAWINGS_FOLDER, image_path.split("/")[-1])
        print("New img path: ", new_img_path)
        cv2.imwrite(new_img_path, image)
        cv2.imshow("Image", image)
        cv2.waitKey(500)
        cv2.destroyAllWindows()
        
    if 89 < average_of_result_angles < 91:
        cv2.putText(image, "Frontal", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        img_name = image_path.split("/")[-1]

        dest_path = os.path.join(FRONTAL_FACE_FOLDER_PATH, image_path.split("/")[-1])
        src_path = os.path.join(FACE_DRAWINGS_FOLDER, image_path.split("/")[-1])
        
        print("\nSrc path: ", src_path)
        print("Dest path: ", dest_path)
        shutil.copy(src_path, dest_path)
    else:
        cv2.putText(image, "Non-frontal", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)


def calculate_rotation_avg_angle_avg(img_path):
    image = cv2.imread(img_path)
    results = face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )

    nose_landmarks = landmark_operations.get_nose_landmarks(results)
    head_poses = landmark_operations.head_pose_estimation( results, image )
    average_angle = common.calculate_abs_average( head_poses )
    result_angles = landmark_operations.calculate_nose_perpendicular_angle( nose_landmarks )

    abs_result_angles = [np.abs(angle) for angle in result_angles]
    average_of_result_angles = np.mean(abs_result_angles)
    
    return average_angle, average_of_result_angles

def write_frontal_faces(img_path):
    img = cv2.imread(img_path)
    img_name = img_path.split("/")[-1]
    if not os.path.exists(FRONTAL_FACE_FOLDER_PATH):
        os.makedirs(FRONTAL_FACE_FOLDER_PATH)

    shutil.copy(os.path.join(FACE_DRAWINGS_FOLDER, img_name),
                os.path.join(FRONTAL_FACE_FOLDER_PATH, img_name)
        )
def show_drawn_landmarks(image_path):
    global mp_face_mesh
    image = cv2.imread(image_path)
    results = face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )
    
    try:
        draw_landmarks(image=image, results=results,
                        zoom_scale=7, image_path=image_path,
                        show_flag=True)
    except Exception as e:
        print("Error in showing landmarks for ", image_path,"\nError: ", e)
        pass


def show_folder_images(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg"):
                show_drawn_landmarks(os.path.join(root, file))

if __name__ == "__main__":
    show_folder_images("src/original-casia-webface")
    
    #main()
    #write_angle("UMUT\casia-webface_FOLDERED\Frontal_faces")
    #sort_angles("angles.txt")
    #plot_with_img_paths("angles.txt", 10, 10)
    #delete_txt_and_jpg("angles.txt", 100)
