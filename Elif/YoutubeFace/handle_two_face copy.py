import os
import shutil
import sys

sys.path.insert(0, './retinaface_custom/main')
import RetinaFace

print("RetinaFace imported from", RetinaFace.__file__)


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


def extract_error_paths(folder_path,output_folder_path, delete_small_images, reset=False):
    os.makedirs(output_folder_path, exist_ok=True)

    # to work in copy the folder to folder_path+'_copy' and work on it
    folder_path_copy = os.path.join(output_folder_path, folder_path.split('/')[-1]+'_copy')
    os.makedirs(folder_path_copy, exist_ok=True)
    if not os.path.exists(folder_path_copy) or reset == True:
        if reset == True:
            shutil.rmtree(folder_path_copy)
        shutil.copytree(folder_path, folder_path_copy)
        #shutil.rmtree(os.path.join(folder_path_copy,'Frontal_Faces'))
        #os.remove(os.path.join(folder_path_copy,'HELEN_Info.txt'))
        
        print("Copied the folder to: ", folder_path_copy)
    folder_path = folder_path_copy

    # error_file_names -> Represents the txt and img file paths with error
    error_file_names = [];error_counter = 0;root_path_holder = 'init'

    too_much_error_txt_path = os.path.join(output_folder_path, "too_much_error.txt")
    too_much_error_folders = []

    few_error_txt_path = os.path.join(output_folder_path, "few_error.txt")
    few_error_file_paths = [];too_much_error_file_paths = []

    for root_path, dir_names, file_names in os.walk(folder_path):
        if len(file_names)> 1:
            average_img_size =  calculate_average_img_size(root_path)

        for file_name in file_names:
            if file_name.endswith('.jpg') and delete_small_images == True:
                img_path = os.path.join(root_path, file_name)
                img = cv2.imread(img_path)
                img_size = img.shape[0] * img.shape[1]
                if img_size < average_img_size/4:
                    print("Image size is too small: ", img_path)
                    error_counter += 1
                    error_file_names.append(img_path)
                    txt_path = os.path.join(os.path.splitext(img_path)[0] + '.txt')
                    if os.path.exists(txt_path):
                        error_file_names.append(txt_path)

            if file_name.endswith('.txt'):
                txt_path = os.path.join(root_path, file_name)
                with open(txt_path, 'r') as txt_file:
                    content = txt_file.read()
                    #print(len(content))
                    if len(content) <200:
                        #print( "---------------\ncontent:", content,",path: ", txt_path)
                        None
                    if "Error" in content or "Stack Overflow" in content or "too small" in content or "LandmarkError" in content:
                        error_counter += 1
                        error_file_names.append(txt_path)
                        """
                        new_txt_id = (int(os.path.splitext(txt_path)[0].split('\\')[-1]) - 1 )
                        new_txt_id = f'{new_txt_id:08d}'
                        img_path = os.path.join('\\'.join(os.path.splitext(txt_path)[0].split('\\')[:-1]),new_txt_id) + '.jpg'
                        """
                        img_path = os.path.join(os.path.splitext(txt_path)[0] + '.jpg')

                        if os.path.exists(img_path):
                            error_file_names.append(img_path)
                        else:
                            print("Image does not exist: ", img_path, " for txt: ", txt_path)
                            exit()
            else:
                content = ''

        if root_path != root_path_holder and root_path_holder!='init':
            len_file_names = int((len(file_names)-1)/2)
            len_file_names = 1 if len_file_names == 0 else len_file_names
            if error_counter/len_file_names > 0.3:
                too_much_error_folders.append(root_path)

            error_counter = 0
        root_path_holder = root_path

    for file_path in error_file_names:
        if '\\'.join(file_path.split('\\')[:-1]) in too_much_error_folders:
            too_much_error_file_paths.append(file_path)
        else:
            few_error_file_paths.append(file_path)

        if len (too_much_error_file_paths) == 0:
            few_error_file_paths.append(file_path)

    with open(few_error_txt_path, 'w') as f:
        for file_path in few_error_file_paths:
            f.write(file_path + '\n')
    with open(too_much_error_txt_path, 'w') as f:
        for file_path in too_much_error_file_paths:
            f.write(file_path + '\n')

    return few_error_txt_path, too_much_error_txt_path


import cv2
import sys


sys.path.insert(0, './UMUT')
import txtFileOperations

selected_face = 0
square_threshold = 3000


def find_eucledian_distance(point1,point2):
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5


def find_best_face(faces,hold_original_img):
    min_distance = sys.maxsize
    center_original_img = [int(hold_original_img.shape[1]/2),int(hold_original_img.shape[0]/2)]
    for key, value in faces.items():
        center_face = [int((value['facial_area'][2]-value['facial_area'][0])/2),int((value['facial_area'][3]-value['facial_area'][1])/2)]
        distance = find_eucledian_distance(center_original_img,center_face)
        if distance < min_distance:
            min_distance = distance
            selected_face = list(faces.keys()).index(key)
    return selected_face

def process_faces(img_path ,faces ,hold_original_img , dynamic_offset=0):
    global selected_face
    face_crops = []
    for key, value in faces.items():
        facial_area = value['facial_area']
        offset = dynamic_offset * 20 - 10
        face_img = hold_original_img[
            int(facial_area[1])-offset:int(facial_area[3])+offset, int(facial_area[0])-offset:int(facial_area[2])+offset
        ]
        face_crops.append(face_img)

    try:
        with open(img_path.replace('jpg','txt'), 'r') as f:
            txt_content = f.read()
    except:
        txt_content = 'No txt file found'
    
    if "TwoPeopleDetected" in txt_content:
        selected_face = find_best_face(faces,hold_original_img)
        """
        cv2.startWindowThread()
        cv2.imshow("Selected Face",face_crops[selected_face])
        cv2.imshow("Original",hold_original_img)
        cv2.waitKey();cv2.destroyAllWindows()
        """
    else:
        selected_face = 0

    if len(face_crops) != 0 and face_crops[selected_face].shape[0] != 0 and face_crops[selected_face].shape[1] != 0:
        cv2.imwrite(img_path, face_crops[selected_face])
        resp = RetinaFace.extract_faces(img_path,align=True,align_first=True)
    else:
        resp = {}

    if len(list(resp.keys())) >1 or len(list(resp.keys())) == 0:
        if dynamic_offset == 4:
            return {"Error": str("Stack Overflow while finding face( more than 4 loop ): " +img_path) }, hold_original_img
        write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img,dynamic_offset+1)
        return write_value_dict, final_cropped_img

    write_value_dict = resp.get('face_1').get('landmarks')
    final_cropped_img = resp.get('face_1').get('face')
    return write_value_dict, final_cropped_img


def select_which_face_is_true(txt_path):
    global selected_face
    img_path = os.path.splitext(txt_path)[0] + '.jpg'
    if os.path.exists(img_path):

        hold_original_img = cv2.imread(img_path)
        faces = RetinaFace.detect_faces(img_path)

        if len (faces) == 0:
            return

        write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img)

        txtFileOperations.writeLandmarksTxtFile(txt_path, write_value_dict)
        cv2.imwrite(img_path, final_cropped_img)
        print("Completed the process for: ", img_path)
       

    else:
        print("Image does not exist: ", img_path)
        exit()


def handle_error_paths(few_error_txt_path, too_much_error_txt_path,force_reset):
    # Read the txt files and remove the images with error
    with open(few_error_txt_path, 'r') as f:
        few_error_file_paths = f.readlines()
    with open(too_much_error_txt_path, 'r') as f:
        too_much_error_file_paths = f.readlines()

    # Remove the images with error
    for file_path in few_error_file_paths:
        file_path = file_path.strip()
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(" ** File does not exist: ", file_path)
            #exit()

    # Select the correct face and write the landmarks
    hold_intra = 'init'
    for file_path in too_much_error_file_paths:
        file_path = file_path.strip()
        if os.path.exists(file_path) and file_path.endswith('.txt'):
            if force_reset == True:
                os.remove(file_path)

                os.remove(file_path.replace('txt','jpg'))
                continue
            try:
                intra = file_path.split('\\')[-1].split('.')[0].split('_')[1]
            except:
                intra = file_path.split('/')[-1].split('.')[0].split('_')[1]

            select_which_face_is_true(file_path)
            hold_intra = intra
        elif not os.path.exists(file_path):
            print(" * File does not exist: ", file_path)
            #exit()

def main(folder_path, output_folder_path, force_reset, reset):
    few_error_txt_path, too_much_error_txt_path = extract_error_paths(folder_path, output_folder_path, True, reset)
    handle_error_paths(few_error_txt_path, too_much_error_txt_path, force_reset)
  
    shutil.copy(few_error_txt_path, './Umut/Two_Face_Handle/few_error_hold.txt')
    shutil.copy(too_much_error_txt_path, './Umut/Two_Face_Handle/too_much_error_hold.txt')

    few_error_txt_path, too_much_error_txt_path = extract_error_paths(folder_path, output_folder_path, False, False)
    
    with open(too_much_error_txt_path, 'r') as f:
        too_much_error_file_paths = f.readlines()
    with open(few_error_txt_path, 'a') as f:
        for file_path in too_much_error_file_paths:
            f.write(file_path)
    with open(too_much_error_txt_path, 'w') as f:
        f.write("")

    handle_error_paths(few_error_txt_path, too_much_error_txt_path, force_reset)
    print("Completed the process...")

if __name__ == '__main__':
    main( folder_path = './UMUT/ConcatFolders/Output', output_folder_path='./Elif/Two_Face_Handle', force_reset = True ,reset=False)
