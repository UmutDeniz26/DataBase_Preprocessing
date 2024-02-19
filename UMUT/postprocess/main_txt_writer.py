import os
import sys
import numpy as np

sys.path.insert(0, './UMUT')
import txtFileOperations

def main(destination_folder_path, data_base_name, upper_folder_name):

    dtype = np.dtype([("path", object), ("class_inter", int), ("class_intra", int), ("mask", object)])
    data = np.array([], dtype=dtype)  # Initialize data as an empty numpy array

    inter = 0
    intra = 0
    person_id = 0
    person_counter = 0
    hold_person_id = 'init'

    skip_inter = False
    for root, dirs, files in sorted(os.walk(destination_folder_path)):
        if len(files) > 1:
            for file in files:
                if file.endswith(".txt"):
                    if "frontal" in os.path.join(root, file).lower() or "info" in os.path.join(root, file).lower():
                        skip_inter = True
                        continue
                    else:
                        skip_inter = False

                    # find mask of this image's folder
                    folder_path = os.path.dirname(os.path.join(root, file))
                    frontal_path = os.path.join(folder_path, "frontal")
                    frontal_image_name = os.listdir(frontal_path)[0]
                    mask_path = os.path.join(folder_path, frontal_image_name)
                    data = np.concatenate((data, np.array([(os.path.join(root, file), person_counter, inter, mask_path)], dtype=dtype)))

                    intra += 1
            if not skip_inter:
                inter += 1

        slices = root.split("\\")
        number_of_digit_slices = [slice for slice in slices if slice.isdigit()]

        if len(number_of_digit_slices) == 2 or len(number_of_digit_slices) == 1:
            person_id = number_of_digit_slices[0]
            person_id = int(person_id)
            if hold_person_id == 'init':
                hold_person_id = person_id
            elif hold_person_id != person_id:
                """
                print(f"file: {file} inter: {inter}")
                print(f"person_id: {person_id} person_counter: {person_counter}")
                print(f"hold_person_id: {hold_person_id}\n\n")
                """
                person_counter += 1
                hold_person_id = person_id

    np.save(os.path.join(destination_folder_path, data_base_name + "_Info.npy"), data)  # Save the data to a file

    #read
    data = np.load(os.path.join(destination_folder_path, data_base_name + "_Info.npy"), allow_pickle=True)
    print(os.path.join(destination_folder_path, data_base_name + "_Info.npy"))

if __name__ == "__main__":
    main(destination_folder_path="Ali/CASIA-FaceV5(BMP)_FOLDERED", data_base_name="CASIA", upper_folder_name="UMUT")
    # main(folder_path="HELEN", data_base_name="HELEN", upper_folder_name="UMUT")
    # main(folder_path="LFPW", data_base_name="LFPW", upper_folder_name="UMUT")
