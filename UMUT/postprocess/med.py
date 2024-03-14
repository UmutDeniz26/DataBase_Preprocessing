import os
import numpy as np
import cv2
import mediapipe as mp
import shutil

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
def draw_landmarks(image, results):
    for face_landmarks in results:
        cv2.circle(image, (int(face_landmarks.x * image.shape[1]), int(face_landmarks.y * image.shape[0])), 2, (0, 255, 0), -1)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        

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


if __name__ == "__main__":
    #main()
    write_angle("UMUT\casia-webface_FOLDERED\Frontal_faces")
    sort_angles("angles.txt")
    plot_with_img_paths("angles.txt", 10, 10)
    #delete_txt_and_jpg("angles.txt", 100)
