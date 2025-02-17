import os
import sys
import numpy as np
def prepare_data(destination_folder_path):
    dtype = np.dtype([('path', 'U99'), ('class_inter', 'i4'), ('class_intra', 'i4'), ('mask', 'U99')])
    img_count = 0
    for root, dirs, files in os.walk(destination_folder_path):
        for file in files:
            if "frontal" in os.path.join(root, file).lower() or "info" in os.path.join(root, file).lower():
                continue
            if file.endswith(".jpg"):
                img_count += 1
    print("Img count:",img_count)
    data = np.zeros(
        img_count,
        dtype=dtype
    )
    return data, dtype

import shutil

def main(destination_folder_path,data_base_name):

    data,dtype = prepare_data(destination_folder_path)

    inter = 0;intra = 0
    person_id = 0;person_counter = -1
    hold_person_id = 0

    skip_inter = False
    for root, dirs, files in os.walk(destination_folder_path):
        if len(files) > 1:
            for file in files:
                if file.endswith(".jpg"):
                    file_path = os.path.join(root, file)

                    skip_inter = False
                    if any(keyword in file_path.lower() for keyword in ["frontal","info"]):
                        skip_inter = True
                        continue

                    # find mask of this image's folder
                    folder_path = os.path.dirname(file_path)
                    frontal_path = os.path.join(folder_path, "frontal")
                    frontal_image_name = os.listdir(frontal_path)[0]

                    mask_path = os.path.join(folder_path, frontal_image_name)
                    mask_path = os.path.join(os.sep.join(mask_path.split(os.sep)[1:]))
                    mask_path = os.path.join(data_base_name, mask_path)

                    img_path = os.path.join(root, file.replace("txt","jpg"))
                    img_path = os.path.join(os.sep.join(img_path.split(os.sep)[1:]))
                    img_path = os.path.join(data_base_name, img_path)
                    
                    img_path = img_path.replace("\\", "/")
                    mask_path = mask_path.replace("\\", "/")
                    
                    # if data is not empty, concatenate the new data to the old data

                    dtype_data = np.array((img_path, person_counter, inter, mask_path), dtype=dtype)
                    data[intra] = dtype_data

                    if intra%10000==0:
                        print("Counter: ",intra," Path: ",img_path)
                    intra += 1
                    

            if not skip_inter:
                inter += 1

        slices = root.split("\\")
        slices_include_digit = [slice for slice in slices if slice.isdigit()]

        if len(slices_include_digit) == 2 or len(slices_include_digit) == 1:
            person_id = int(slices_include_digit[0])

            if hold_person_id != person_id:
                person_counter += 1
                hold_person_id = person_id


    if os.path.exists(os.path.join(destination_folder_path, "_Info.npy")):
        os.remove(os.path.join(destination_folder_path, "_Info.npy"))
    np.save(os.path.join(destination_folder_path, "_Info.npy"), data)  # Save the data to a file

    #read
    data = np.load(os.path.join(destination_folder_path, "_Info.npy"))
    print("Data shape: ",data.shape, "Npy is saved to: ",os.path.join(destination_folder_path, "_Info.npy"))
    print("Data: ",data)

if __name__ == "__main__":
    main(destination_folder_path="casia-webface",data_base_name="casia-webface")