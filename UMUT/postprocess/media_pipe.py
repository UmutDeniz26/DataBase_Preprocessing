import os
import numpy as np
import cv2
import mediapipe as mp
import shutil
import matplotlib.pyplot as plt

def main():

    dataset_path = "Esogu-sets/Esogu-sets/"
    target_path = "non-frontal-test"

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    
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
                    head_poses = head_pose_estimation( results, image)
                    average_angle = calculate_average_angle( head_poses )
                    files_with_angles.append( (image_path, average_angle) )
                except Exception as e:
                    print("Error:", e)
                
            files_with_angles = clip_paths_due_to_angles(files_with_angles, clip_frontal_faces_limit)
            for file_angle in files_with_angles:
                image_path = file_angle[0]
                target = os.path.join(target_path, folder)
                if not os.path.exists(target):
                    os.makedirs(target)
                shutil.copy(image_path, target)

    face_mesh.close()
    return 0

def write_angle(folder_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    txt_path = "angles.txt"

    with open(txt_path, "w") as file:
        file.write("")

    for root, dirs, files in os.walk(folder_path):
        print("Length of files: ", len(files))
        for file in files:
            #print("File: ", file)
            if "462_" in file:
                print("File: ", file)
            if file.endswith(".jpg"):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)
                results = face_mesh.process( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )
                head_poses = head_pose_estimation( results, image)
                if head_poses is None:
                    average_angle = 999
                else:
                    average_angle = calculate_average_angle( head_poses )
                
                with open(txt_path, "a") as file:
                    file.write(image_path + " " + str(average_angle) + "\n")


def clip_paths_due_to_angles(files_with_angles, target_size):
    files_with_angles.sort(key=lambda x: x[1], reverse=True)
    return files_with_angles[:target_size]


def head_pose_estimation(results, image):
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

def calculate_average_angle(angles):
    sum_angle = 0
    for angle in angles:
        sum_angle += np.abs(angle)

    return sum_angle / len(angles)

def sort_angles(txt_path):
    with open(txt_path, "r") as f:
        lines = f.readlines()
    lines.sort(key=lambda x: float(x.split(" ")[1]),reverse=True)
    with open(txt_path, "w") as f:
        for line in lines:
            f.write(line)

import matplotlib.pyplot as plt
def plot_with_img_paths(txt_path, row, col):
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

def delete_txt_and_jpg(txt_path, delete_count):
    with open(txt_path, "r") as f:
        lines = f.readlines()
    # Delete the first delete_count lines
    for i in range(delete_count):
        # Replace Frontal_faces part
        img_path_slices = lines[i].split(" ")[0].split(".")[0].split("\\")[-1].split("_")
        path = lines[i].split(" ")[0]
        img_path = path.replace("Frontal_faces", f"{img_path_slices[0]}\\{img_path_slices[1]}")

        txt_path = img_path.replace(".jpg", ".txt")
        os.remove(img_path)
        os.remove(txt_path)

def calculate_angle_between_2_points(p1, p2):
    if isinstance(p1, tuple):
        x1, y1 = p1
        x2, y2 = p2
    else:
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
    return np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

def calculate_nose_perpendicular_angle(nose_landmarks):
    result_angles = []
    for i, landmark in enumerate(nose_landmarks):
        if i == 0:
            continue        
        line_first_point = (nose_landmarks[i-1].x, nose_landmarks[i-1].y)
        line_second_point = (landmark.x, landmark.y)
        angle_betwee_points = calculate_angle_between_2_points(line_first_point, line_second_point)
        result_angles.append(angle_betwee_points)
    return result_angles

                                       
FACEMESH_TESSELATION = mp.solutions.face_mesh.FACEMESH_TESSELATION
IMG_COUNT = 0
TOTAL_IMG_COUNT = 501000
FRONTAL_FACE_FOLDER_PATH = "src/frontal_faces"

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_nose_landmarks(results):
    nose_landmarks = [ results.multi_face_landmarks[0].landmark[1],
                    results.multi_face_landmarks[0].landmark[4],
                    results.multi_face_landmarks[0].landmark[5],
                    results.multi_face_landmarks[0].landmark[195],
                    results.multi_face_landmarks[0].landmark[197],
                    results.multi_face_landmarks[0].landmark[6] ]
    return nose_landmarks
    

FACE_DRAWINGS_FOLDER = "src/frontal"
def draw_landmarks(image, results, zoom_scale=1, image_path=None, show_flag = True):
    global FACEMESH_TESSELATION, IMG_COUNT, FRONTAL_FACE_FOLDER_PATH
    IMG_COUNT += 1

    if results.multi_face_landmarks is None or image is None:
        return

    if zoom_scale != 1 and show_flag:
        image = cv2.resize(image, (0, 0), fx=zoom_scale, fy=zoom_scale)
    
    multi_face_landmarks = results.multi_face_landmarks[0]
    
    avg_rotation_angle, average_of_result_angles = calculate_rotation_avg_angle_avg(image_path)
    center_of_eyes = get_center_of_eyes(multi_face_landmarks.landmark)
    
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
        
        nose_landmarks = get_nose_landmarks(results)

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

        
    if check_two_frontal_parameter(average_of_result_angles, avg_rotation_angle):
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

    nose_landmarks = get_nose_landmarks(results)
    head_poses = head_pose_estimation( results, image )
    average_angle = calculate_average_angle( head_poses )
    result_angles = calculate_nose_perpendicular_angle( nose_landmarks )

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
        draw_landmarks(image, results,
                        zoom_scale=7, image_path=image_path,
                        show_flag=True)
    except Exception as e:
        print("Error in showing landmarks for ", image_path)
        print("Error: ", e)
        pass

def get_center_of_eyes(landmarks):
    center_of_right_eye = (landmarks[33].x + landmarks[133].x) / 2, (landmarks[33].y + landmarks[133].y) / 2
    center_of_left_eye = (landmarks[362].x + landmarks[263].x) / 2, (landmarks[362].y + landmarks[263].y) / 2
    return center_of_left_eye, center_of_right_eye

def show_folder_images(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg"):
                show_drawn_landmarks(os.path.join(root, file))

def check_two_frontal_parameter(angle_parameter,rotation_parameter):
    if 89 < angle_parameter < 91:
        return True
    return False
        

if __name__ == "__main__":
    shutil.rmtree("src/frontal", ignore_errors=True)
    shutil.rmtree("src/frontal_faces", ignore_errors=True)
    show_folder_images("src/original-casia-webface")
    #main()
    #write_angle("UMUT\casia-webface_FOLDERED\Frontal_faces")
    #sort_angles("angles.txt")
    #plot_with_img_paths("angles.txt", 10, 10)
    #delete_txt_and_jpg("angles.txt", 100)
