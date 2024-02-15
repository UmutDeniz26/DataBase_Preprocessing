import os
import shutil
import sys

sys.path.insert(0, './retinaface_custom/main')
import RetinaFace

print("RetinaFace imported from", RetinaFace.__file__)


def print_list(list):
    for item in list:
        print(item)


def extract_error_paths(folder_path,output_folder_path, reset=False):
    os.makedirs(output_folder_path, exist_ok=True)

    # to work in copy the folder to folder_path+'_copy' and work on it
    folder_path_copy = os.path.join(output_folder_path, folder_path.split('/')[-1]+'_copy')
    os.makedirs(folder_path_copy, exist_ok=True)
    if not os.path.exists(folder_path_copy) or reset == True:
        if reset == True:
            shutil.rmtree(folder_path_copy)
        shutil.copytree(folder_path, folder_path_copy)
        print("Copied the folder to: ", folder_path_copy)
    folder_path = folder_path_copy

    # error_file_names -> Represents the txt and img file paths with error
    error_file_names = [];error_counter = 0;root_path_holder = 'init'

    too_much_error_txt_path = os.path.join(output_folder_path, "too_much_error.txt")
    too_much_error_folders = []

    few_error_txt_path = os.path.join(output_folder_path, "few_error.txt")
    few_error_file_paths = [];too_much_error_file_paths = []

    for root_path, dir_names, file_names in os.walk(folder_path):
        for file_name in file_names:
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
        for too_much_error_path in too_much_error_folders:
            if too_much_error_path in file_path:
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
import txtFileOperations

selected_face = 0
square_threshold = 3000

def process_faces(img_path ,faces ,hold_original_img ,change_face_selection ,dynamic_offset=0):
    global selected_face
    face_crops = []
    for key, value in faces.items():
        facial_area = value['facial_area']
        offset = dynamic_offset * 10 - 10
        face_img = hold_original_img[
            int(facial_area[1])-offset:int(facial_area[3])+offset, int(facial_area[0])-offset:int(facial_area[2])+offset
        ]
        face_crops.append(face_img)

    if change_face_selection == True:
        for i, face_crop in enumerate(face_crops):
            try:
                WINDOW_NAME = img_path
                cv2.namedWindow(WINDOW_NAME)
                cv2.startWindowThread()
                cv2.imshow(WINDOW_NAME,face_crop)

                cv2.waitKey();cv2.destroyAllWindows()
                print("Is it the correct face? (y/n)")
                correct_face = input()
                if correct_face == 'y':
                    selected_face = i
                    break
            except:
                None

    if len(face_crops) != 0 and face_crops[selected_face].shape[0] != 0 and face_crops[selected_face].shape[1] != 0:
        cv2.imwrite(img_path, face_crops[selected_face])
        resp = RetinaFace.extract_faces(img_path,align=True,align_first=True)
    else:
        resp = {}

    if len(list(resp.keys())) >1 or len(list(resp.keys())) == 0:
        if dynamic_offset == 4:
            return {"Response": str("Stack Overflow while finding face( more than 4 loop ): " +img_path) }, hold_original_img
        write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img,False,dynamic_offset+1)
        return write_value_dict, final_cropped_img

    write_value_dict = resp.get('face_1').get('landmarks')
    final_cropped_img = resp.get('face_1').get('face')
    return write_value_dict, final_cropped_img


def select_which_face_is_true(txt_path,change_face_selection):
    global selected_face
    img_path = os.path.splitext(txt_path)[0] + '.jpg'
    if os.path.exists(img_path):

        hold_original_img = cv2.imread(img_path)
        faces = RetinaFace.detect_faces(img_path)

        if len (faces) == 0:
            input("No face found in the image: "+ img_path + "\nPress Enter to continue...")
            return

        write_value_dict, final_cropped_img = process_faces(img_path,faces,hold_original_img,change_face_selection)

        try:
            facial_area = write_value_dict.get('face_1').get('facial_area')
            square = abs(facial_area[2]-facial_area[0]) * abs(facial_area[3]-facial_area[1])

            # if the face area is too small, then return ,
            global square_threshold
            if square < square_threshold:
                write_value_dict = {"Response": "Face area is too small: " + str(square) + " " + img_path}
                final_cropped_img = hold_original_img
        except:
            None
        txtFileOperations.writeLandmarksTxtFile(txt_path, write_value_dict)
        cv2.imwrite(img_path, final_cropped_img)

    else:
        print("Image does not exist: ", img_path)
        exit()


def handle_error_paths(few_error_txt_path, too_much_error_txt_path):
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
            try:
                intra = file_path.split('\\')[-1].split('.')[0].split('_')[1]
            except:
                intra = file_path.split('/')[-1].split('.')[0].split('_')[1]

            if hold_intra != intra:
                change_face_selection = True
            else:
                change_face_selection = False

            select_which_face_is_true(file_path,change_face_selection)
            hold_intra = intra
        elif not os.path.exists(file_path):
            print(" * File does not exist: ", file_path)
            exit()

def main(folder_path, output_folder_path, reset):
    few_error_txt_path, too_much_error_txt_path = extract_error_paths(folder_path, output_folder_path, reset)
    handle_error_paths(few_error_txt_path, too_much_error_txt_path)

    few_error_txt_path, too_much_error_txt_path = extract_error_paths(folder_path, output_folder_path, False)
    handle_error_paths(few_error_txt_path, too_much_error_txt_path)
    print("Completed the process...")

if __name__ == '__main__':
    main( folder_path = './Umut/AFW_FOLDERED', output_folder_path='./Umut/Two_Face_Handle', reset=True )
