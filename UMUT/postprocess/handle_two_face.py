import os
import sys
import cv2
import shutil
import matplotlib.pyplot as plt
from deepface import DeepFace

selected_face = 0
last_final_cropped_img = 0
hold_intra = ""

sys.path.insert(0, './retinaface_custom/main')
import RetinaFace
print("RetinaFace imported from", RetinaFace.__file__)

sys.path.insert(0, './UMUT')
import txtFileOperations

def print_list(list):
    for item in list:
        print(item)

def find_a_correct_face(folder_path):
    for root_path, dir_names, file_names in os.walk(folder_path):
        for file_name in file_names:
            if file_name.endswith('.txt'):
                with open(os.path.join(root_path, file_name), 'r') as f:
                    content = f.read()
                if "right_eye" in content:
                    img = cv2.imread(os.path.join(root_path, file_name).replace('.txt','.jpg'))
                    return img 
    return False
                
                
def find_eucledian_distance(point1,point2):
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5

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

def extract_crop_faces(faces, hold_original_img, dynamic_offset):
    face_crops = [];face_crops_without_offset = []
    for key, value in faces.items():
        facial_area = value['facial_area']
        offset = dynamic_offset * 20 - 10
        static_offset = 10
        face_img = hold_original_img[
            int(facial_area[1]) - offset:int(facial_area[3]) + offset,
            int(facial_area[0]) - offset:int(facial_area[2]) + offset
        ]
        face_img_without_offset = hold_original_img[
            int(facial_area[1]) - static_offset:int(facial_area[3]) + static_offset, 
            int(facial_area[0]) - static_offset:int(facial_area[2]) + static_offset
        ]
        face_crops.append(face_img)
        face_crops_without_offset.append(face_img_without_offset)
    return face_crops, face_crops_without_offset

def process_faces(img_path ,faces ,hold_original_img, make_decision, dynamic_offset=0):
    global selected_face,last_final_cropped_img    
    
    face_crops, face_crops_without_offset = extract_crop_faces(faces, hold_original_img, dynamic_offset)
    
    # Select the face if make_decision is True
    if make_decision:
            print("Select the face: ")
            selected_face = select_face(face_crops,hold_original_img,img_path)    
        

    correct_face = find_a_correct_face(os.path.split(img_path)[0])
    if correct_face is False:
        correct_face = face_crops[selected_face]

    # if hold last face is not empty, then calculate the difference
    if len(face_crops_without_offset) <= selected_face:
        print("Selected face is not in the list, select the face again: ")
        selected_face = select_face(face_crops, hold_original_img, img_path)

    result = DeepFace.verify(
        face_crops_without_offset[selected_face], correct_face, enforce_detection=False
    )

    # If the selected face is not verified, then select the face again
    if result.get("verified") == False:
        print("Select the face:: ")
        selected_face = select_face(face_crops, hold_original_img, img_path)
        if dynamic_offset == 4:
            return {
                "Error": str("Stack Overflow while finding face( DeepFace Error ): " +img_path) 
            }, hold_original_img

        write_value_dict, final_cropped_img = process_faces(
            img_path= img_path,faces=faces,hold_original_img=hold_original_img,
            make_decision=False,dynamic_offset=dynamic_offset+1
        )    
        return write_value_dict, final_cropped_img    

    
    if face_crops[selected_face].shape[0] != 0 and face_crops[selected_face].shape[1] != 0:
        resp = RetinaFace.extract_faces(face_crops[selected_face],align=True,align_first=True)
    else:
        resp = {}

    if len(list(resp.keys())) >1 or len(list(resp.keys())) == 0:    
        if dynamic_offset == 4:
            return {"Error": str("Stack Overflow while finding face( more than 4 loop ): " +img_path) }, hold_original_img
        write_value_dict, final_cropped_img = process_faces(
            img_path=img_path,faces=faces,
            hold_original_img=hold_original_img,make_decision=False,
            dynamic_offset=dynamic_offset+1
        )    
        return write_value_dict, final_cropped_img    
    elif len(list(resp.keys())) == 1:
        result = DeepFace.verify(
            resp.get('face_1').get('face'), correct_face, enforce_detection=False
            ).get("verified")
        if result == False:
            if dynamic_offset == 4:
                return {"Error": str("Stack Overflow while finding face( result and target are different ): " +img_path) }, hold_original_img
            write_value_dict, final_cropped_img = process_faces(
                img_path= img_path,faces=faces,hold_original_img=hold_original_img,
                make_decision=False,dynamic_offset=dynamic_offset+1
            )    
            return write_value_dict, final_cropped_img


    write_value_dict = resp.get('face_1').get('landmarks')
    final_cropped_img = resp.get('face_1').get('face')
    return write_value_dict, final_cropped_img


def select_which_face_is_true(txt_path):
    global selected_face,hold_intra
    txt_path = os.path.normpath(txt_path)
    img_path = txt_path.replace('.txt','.jpg')

    try:
        if len(txt_path.split('\\')[-1].split('.')[0].split('_')) == 1:
            intra = txt_path.split('\\')[-2]
        else:
            intra = txt_path.split('\\')[-1].split('.')[0].split('_')[1]
    except:
        print("Error ( cannot found intra ): ", txt_path)
        exit()

    if os.path.exists(img_path):
        hold_original_img = cv2.imread(img_path)
        faces = RetinaFace.detect_faces(img_path)
        if len (faces) == 0:
            return
        else:
            
            make_decision = True if hold_intra != intra or hold_intra == "" else False
            
            hold_intra = intra
            
            write_value_dict, final_cropped_img = process_faces(
                img_path=img_path,faces=faces,
                hold_original_img=hold_original_img,
                make_decision=make_decision
            )
            
        txtFileOperations.writeLandmarksTxtFile(txt_path, write_value_dict)
        cv2.imwrite(img_path, final_cropped_img)
        if "TwoPeopleDetected" in list(write_value_dict.values())[0]:
            print("Two people detected: ", img_path)
        elif "Stack Overflow" in list(write_value_dict.values())[0]:
            print("Stack Overflow: ", img_path)
        else:
            print("Completed the process for: ", img_path)
    else:
        print("Image does not exist: ", img_path);exit()

import numpy as np

def handle_error_paths(error_paths_txt_path):

    with open(error_paths_txt_path, 'r') as f:
        error_paths_list = f.readlines()

    index = 0
    hold_intra_index = ''
    # Remove the images with error
    for file_path in error_paths_list:
        file_path = file_path.strip()
        file_path = os.path.normpath(file_path)
        
        if os.path.exists(file_path) and file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                content = f.read()
        else:
            continue
        if len(file_path.split('\\')[-1].split('.')[0].split('_')) == 1:
            intra = file_path.split('\\')[-2]
        else:
            intra = file_path.split('\\')[-1].split('.')[0].split('_')[1]

        if hold_intra_index != intra or hold_intra_index == "":
            index = 0 
        hold_intra_index = intra

        intra_folder_path = os.sep.join(os.path.split(file_path)[:-1])
        
        limit_error = 20
        correct_file_counter = 0
        temp_error_paths_list = []
        
        for file_name in os.listdir(intra_folder_path):
            intra_file_path = os.path.join(intra_folder_path, file_name)
            if intra_file_path.endswith('.txt'):
                with open(intra_file_path, 'r') as f:
                    content = f.read()
                if (
                    "TwoPeopleDetected" in content or "Error" in content or "Stack Overflow" in content or "too small" in content or "LandmarkError" in content
                    ) == False:
                    correct_file_counter += 1
                elif("TwoPeopleDetected" in content or "Stack Overflow" in content):
                    temp_error_paths_list.append(intra_file_path)
        if limit_error > len(temp_error_paths_list):
            limit_error = len(temp_error_paths_list)

        error_path_list_linespace = np.linspace(0, len(temp_error_paths_list) - 1, limit_error+1, dtype=int)

        if index > limit_error-1:
            print()

        if correct_file_counter > limit_error-1 or index > limit_error-1:
            continue
        
        select_which_face_is_true(temp_error_paths_list[error_path_list_linespace[index]])
        
        index+=1


def main(error_paths_txt_path):
    handle_error_paths(error_paths_txt_path)
    print("Completed the process...")

if __name__ == '__main__':
    main( 
        error_paths_txt_path = "UMUT\Error_Handle\error_paths.txt"
    )
