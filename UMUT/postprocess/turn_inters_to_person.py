import os 
import shutil
def find_max_person_id(folder_path):
    max_person_id = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                if any(keyword in file_path.lower() for keyword in ["frontal","info"]):
                    continue
                person_id = int(file.split("_")[0])
                if person_id > max_person_id:
                    max_person_id = person_id

    return max_person_id


def main(folder_path,copy=False):
    output_folder = os.path.normpath(
        os.path.join(
            "UMUT/src/turn_inters_to_person_output", 
            os.path.normpath(folder_path).split("\\")[-1] + "_without_inter"
            )
        )
    if copy:
        # Copy the folder to the output folder
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        shutil.copytree(folder_path, output_folder)
    
    if not os.path.exists(folder_path):
        print("Folder does not exist: ",folder_path)
        exit()

    max_person_id = find_max_person_id(output_folder)

    for root, dirs, files in os.walk(output_folder):
        if len(files) > 1:
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    if any(keyword in file_path.lower() for keyword in ["frontal","info"]):
                        continue
        if "frontal" not in dirs:
            if len(os.listdir(output_folder))*(2/3)> len(dirs) > 1:
                print(dirs)
                for index,dir_name in enumerate(dirs):
                    if index == len(dirs)-1:
                        break
                    max_person_id += 1
                    str_max_person_id = f"{max_person_id:08d}"
                    print("Copying from: ",os.path.join(root,dir_name)," to: ",os.path.join(output_folder,str_max_person_id))
                    shutil.move(os.path.join(root,dir_name),os.path.join(output_folder,str_max_person_id,str_max_person_id))


if __name__ == '__main__':
    main("UMUT/src/final_datasets/AFW", copy=True)
    main("UMUT/src/final_datasets/HELEN", copy=False)
    main("UMUT/src/final_datasets/LFPW", copy=False)