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

def process_faces(img_path ,faces ,hold_original_img, make_decision, dynamic_offset=0):
    global selected_face,hold_last_face
    face_crops = []

    for key, value in faces.items():
        facial_area = value['facial_area']
        offset = dynamic_offset * 20 - 10
        face_img = hold_original_img[
            int(facial_area[1]) - offset:int(facial_area[3]) + offset, int(facial_area[0]) - offset:int(facial_area[2]) + offset
        ]
        face_crops.append(face_img)
        

    if len(hold_last_face)>1:
        current_size_square = face_crops[selected_face].shape[0] * face_crops[selected_face].shape[1]
        size_square = hold_last_face.shape[0] * hold_last_face.shape[1]
        if abs(current_size_square - size_square) > current_size_square * 0.5:
            print("Size difference is more than 20%")
            print("Current size: ", current_size_square)
            print("Last size: ", size_square)
            print("Difference: ", abs(current_size_square - size_square), "is greater than", current_size_square * 0.2)
            make_decision = True

    if make_decision:
        fig, axs = plt.subplots(1, len(face_crops) + 1, figsize=(15, 5))
        fig.suptitle(img_path)

        for i, face_img in enumerate(face_crops):
            if face_img.shape[0] != 0 and face_img.shape[1] != 0:    
                axs[i].imshow(face_img)
                axs[i].set_title("Selected Face " + str(i))

        axs[len(face_crops)].imshow(hold_original_img)
        axs[len(face_crops)].set_title("Original")
        plt.show()

        selected_face = int(input("Which face is true? (0,1,2,3 ...)"))
        

    if len(face_crops) != 0 and face_crops[selected_face].shape[0] != 0 and face_crops[selected_face].shape[1] != 0:
        cv2.imwrite(img_path, face_crops[selected_face])
        resp = RetinaFace.extract_faces(img_path,align=True,align_first=True)
    else:
        return {"Error": str("Stack Overflow while finding face( len(face_crops) == 0 ): " +img_path) }, hold_original_img
        
    if len(list(resp.keys())) >1 or len(list(resp.keys())) == 0:
        if dynamic_offset == 4:
            return {"Error": str("Stack Overflow while finding face( more than 4 loop ): " +img_path) }, hold_original_img
        write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img,False,dynamic_offset+1)
        return write_value_dict, final_cropped_img
    
    
    write_value_dict = resp.get('face_1').get('landmarks')
    final_cropped_img = resp.get('face_1').get('face')
    return write_value_dict, final_cropped_img

hold_last_face = []

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
            hold_last_face = final_cropped_img

        txtFileOperations.writeLandmarksTxtFile(txt_path, write_value_dict)
        cv2.imwrite(img_path, final_cropped_img)
        
        print("Completed the process for: ", img_path)
        hold_intra = intra
    else:
        print("Image does not exist: ", img_path);exit()


def handle_error_paths(error_txt_path, error_paths_txt_path, work_on_copy=False):
    # Read the txt files and remove the images with error
    with open(error_txt_path, 'r') as f:
        error_list = f.readlines()

    with open(error_paths_txt_path, 'r') as f:
        error_paths_list = f.readlines()

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
        
        select_which_face_is_true(file_path)
        

def main(folder_path, output_folder_path, error_txt_path, error_paths_txt_path, work_on_copy=False):
    handle_error_paths(error_txt_path, error_paths_txt_path, work_on_copy)
    print("Completed the process...")

if __name__ == '__main__':
    main( 
        folder_path = 'UMUT\ConcatFolders\Output', output_folder_path='./Umut/Two_Face_Handle',
        error_txt_path = "UMUT\Error_Handle\error.txt" , error_paths_txt_path = "UMUT\Error_Handle\error_paths.txt",
        work_on_copy=False
    )
