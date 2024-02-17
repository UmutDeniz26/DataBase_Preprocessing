import os
import sys
import cv2
import shutil
import matplotlib.pyplot as plt
selected_face = 0
hold_intra = ""

sys.path.insert(0, './retinaface_custom/main')
import RetinaFace
print("RetinaFace imported from", RetinaFace.__file__)

sys.path.insert(0, './UMUT')
import txtFileOperations

def print_list(list):
    for item in list:
        print(item)

def calculate_average_img_size(folder_path):
    total_width = 0;total_height = 0;total_counter = 0
    for root_path, dir_names, file_names in os.walk(folder_path):
        for file_name in file_names:
            if file_name.endswith('.jpg'):
                img_path = os.path.join(root_path, file_name)
                img = cv2.imread(img_path)
                total_width += img.shape[1]
                total_height += img.shape[0]
                total_counter += 1
    Average_width = total_width/total_counter
    Average_height = total_height/total_counter
    Average_size = Average_width * Average_height
    return Average_size


def find_eucledian_distance(point1,point2):
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5

def find_best_face(faces,hold_original_img):
    best_face = 0
    best_face_size = 0
    for key, value in faces.items():
        facial_area = value['facial_area']
        face_size = (facial_area[2]-facial_area[0]) * (facial_area[3]-facial_area[1])
        if face_size > best_face_size:
            best_face_size = face_size
            best_face = key
    return best_face

def select_face(face_crops,hold_original_img,img_path):
    global selected_face

    fig, axs = plt.subplots(1, len(face_crops) + 1, figsize=(15, 5))
    fig.suptitle(img_path)

    for i, face_img in enumerate(face_crops):
        if face_img.shape[0] != 0 and face_img.shape[1] != 0:    
            axs[i].imshow(face_img)
            axs[i].set_title("Selected Face " + str(i))

    axs[len(face_crops)].imshow(hold_original_img)
    axs[len(face_crops)].set_title("Original")
    plt.show()

    selected_face = int(input("Which face is true? (0,1,2,3 ...) "))
    return selected_face

def calculate_size_difference(image_1, image_2):
    print("Image 1 square: ", image_1.shape[0] * image_1.shape[1])
    print("Image 2 square: ", image_2.shape[0] * image_2.shape[1])
    print("Difference: ", abs(image_1.shape[0] * image_1.shape[1] - image_2.shape[0] * image_2.shape[1]))
    return abs(image_1.shape[0] * image_1.shape[1] - image_2.shape[0] * image_2.shape[1])

def process_faces(img_path ,faces ,hold_original_img, make_decision, dynamic_offset=0):
    global selected_face,hold_last_face,hold_last_face_without_offset
    face_crops = []
    face_crops_without_offset = []

    for key, value in faces.items():
        facial_area = value['facial_area']
        offset = dynamic_offset * 20 - 10
        face_img = hold_original_img[
            int(facial_area[1]) - offset:int(facial_area[3]) + offset, int(facial_area[0]) - offset:int(facial_area[2]) + offset
        ]
        face_img_without_offset = hold_original_img[
            int(facial_area[1]):int(facial_area[3]), int(facial_area[0]):int(facial_area[2])
        ]

        face_crops.append(face_img)
        face_crops_without_offset.append(face_img_without_offset)

    # if hold last face is not empty, then calculate the difference
    if len(hold_last_face)>1:
        difference = calculate_size_difference(face_crops_without_offset[selected_face],hold_last_face_without_offset)
        if difference > (hold_last_face_without_offset.shape[0] * hold_last_face_without_offset.shape[1]) * 0.3:
            print("Difference is too much, select the face again: ")
            selected_face = select_face(face_crops,hold_original_img,img_path)
    hold_last_face_without_offset = face_crops_without_offset[selected_face]
    
    if make_decision:
        print("Select the face: ")
        selected_face = select_face(face_crops,hold_original_img,img_path)
    
    if face_crops[selected_face].shape[0] != 0 and face_crops[selected_face].shape[1] != 0:
        resp = RetinaFace.extract_faces(face_crops[selected_face],align=True,align_first=True)
    else:
        resp = {}


    if len(list(resp.keys())) >1 or len(list(resp.keys())) == 0:
        hold_last_face = face_crops_without_offset[selected_face]        
        if dynamic_offset == 4:
            return {"Error": str("Stack Overflow while finding face( more than 4 loop ): " +img_path) }, hold_original_img
        write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img,False,dynamic_offset+1)
        return write_value_dict, final_cropped_img    
    elif len(list(resp.keys())) == 1:
        if len(hold_last_face) > 1:
            difference =calculate_size_difference(hold_last_face,resp.get('face_1').get('face'))
            if difference > (resp.get('face_1').get('face').shape[0] * resp.get('face_1').get('face').shape[1]) * 0.5:
                if dynamic_offset == 4:
                    return {"Error": str("Stack Overflow while finding face( too much difference ): " +img_path) }, hold_original_img
                hold_last_face = face_crops[selected_face]        
                write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img,False,dynamic_offset+1)
                return write_value_dict, final_cropped_img
    
    write_value_dict = resp.get('face_1').get('landmarks')
    final_cropped_img = resp.get('face_1').get('face')
    return write_value_dict, final_cropped_img

hold_last_face = [];hold_last_face_without_offset = []

def select_which_face_is_true(txt_path):
    global selected_face,hold_intra,hold_last_face
    txt_path = os.path.normpath(txt_path)

    try:
        intra = txt_path.split('\\')[-1].split('.')[0].split('_')[1]
    except:
        print("Error ( cannot found intra ): ", txt_path)
        exit()

    img_path = os.path.splitext(txt_path)[0] + '.jpg'
    if os.path.exists(img_path):
        hold_original_img = cv2.imread(img_path)
        faces = RetinaFace.detect_faces(img_path)
        if len (faces) == 0:
            return
        elif len(faces) == 1:
            landmarks = faces["face_1"].get('landmarks')
            facial_area = faces["face_1"].get('facial_area')
            final_cropped_img = hold_original_img[int(facial_area[1]):int(facial_area[3]), int(facial_area[0]):int(facial_area[2])]
            landmarks.update({"facial_area":facial_area})
            write_value_dict = landmarks
        else:
            if hold_intra != intra or hold_intra == "":
                make_decision = True
            else:  
                make_decision = False    
            
            write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img,make_decision)

        txtFileOperations.writeLandmarksTxtFile(txt_path, write_value_dict)
        cv2.imwrite(img_path, final_cropped_img)
        
        print("Completed the process for: ", img_path)
        hold_intra = intra
    else:
        print("Image does not exist: ", img_path);exit()

import numpy as np

def handle_error_paths(error_paths_txt_path):

    with open(error_paths_txt_path, 'r') as f:
        error_paths_list = f.readlines()

    index = 0
    hold_intra = ''
    # Remove the images with error
    for file_path in error_paths_list:
        file_path = file_path.strip()
        file_path = os.path.normpath(file_path)
        
        if os.path.exists(file_path) and file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                content = f.read()
        else:
            continue
    
        if "TwoPeopleDetected" not in content:
            continue

        intra = file_path.split('\\')[-1].split('.')[0].split('_')[1]
        if hold_intra != intra or hold_intra == "":
            index = 0  

        hold_intra = intra

        intra_folder_path = os.sep.join(os.path.split(file_path)[:-1])
        
        limit_error = 20
        correct_file_counter = 0
        temp_error_paths_list = []
        
        for file_name in os.listdir(intra_folder_path):
            intra_file_path = os.path.join(intra_folder_path, file_name)
            if intra_file_path.endswith('.txt'):
                with open(intra_file_path, 'r') as f:
                    content = f.read()
                
                if "TwoPeopleDetected" not in content:
                    correct_file_counter += 1
                else:
                    temp_error_paths_list.append(intra_file_path)
        if limit_error > len(temp_error_paths_list):
            limit_error = len(temp_error_paths_list)

        error_path_list_linespace = np.linspace(0, len(temp_error_paths_list) - 1, limit_error, dtype=int)

        if correct_file_counter > limit_error:
            continue
        
        select_which_face_is_true(temp_error_paths_list[error_path_list_linespace[index]])
        index+=1


def main(error_paths_txt_path, work_on_copy=False):
    handle_error_paths(error_paths_txt_path)
    print("Completed the process...")

if __name__ == '__main__':
    main( 
        error_paths_txt_path = "UMUT\Error_Handle\error_paths.txt", work_on_copy=False
    )
