import os
import sys
import numpy as np

def main(destination_folder_path, data_base_name, upper_folder_name):

    dtype = np.dtype([('path', 'U99'), ('class_inter', 'i4'), ('class_intra', 'i4'), ('mask', 'U99')])

    img_count = 0
    for root, dirs, files in os.walk(destination_folder_path):
        for file in files:
            if file.endswith(".jpg"):
                img_count += 1

    data = np.zeros(
        img_count,
        dtype=dtype
    )

    inter = 0
    intra = 0
    person_id = 0
    cnt=0
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
                    mask_path = mask_path.replace("\\", "/")
                    img_path = os.path.join(root, file.replace("txt","jpg"))
                    img_path = img_path.replace("\\", "/")

                    # if data is not empty, concatenate the new data to the old data

                    dtype_data = np.array((img_path, person_counter, intra, mask_path), dtype=dtype)
                    data[cnt] = dtype_data
                    cnt+=1


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
    main(destination_folder_path="AFW", data_base_name="AFW", upper_folder_name="UMUT")
    # main(folder_path="HELEN", data_base_name="HELEN", upper_folder_name="UMUT")
    # main(folder_path="LFPW", data_base_name="LFPW", upper_folder_name="UMUT")
