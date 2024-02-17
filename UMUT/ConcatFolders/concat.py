import os
import shutil

def return_files(path):
    return os.scandir(path)

def main(output_folder_path):
    os.makedirs(output_folder_path, exist_ok=True)
    input_folder = os.scandir('UMUT/ConcatFolders/Input')

    person_id = 0
    intra_id = 0
    inter_id = 0

    for data_base_part in input_folder:
        persons = return_files(data_base_part.path)
        for person in persons:
            if person.name == 'Frontal_Faces':
                print(f'{person.name} is frontal folder')
                continue
            if person.is_file():
                print(f'{person.name} is a file')
                continue
            intras = return_files(person.path)
            for intra in intras:
                inters = return_files(intra.path)
                for inter in inters:
                    os.makedirs(f'{output_folder_path}/{person_id:08d}/{intra_id:08d}', exist_ok=True)
                    if inter.is_file():
                        # Copy file to output
                        extention = inter.name.split('.')[-1]
                        shutil.copy(inter.path, f'{output_folder_path}/{person_id:08d}/{intra_id:08d}/{inter_id:08d}.{extention}')
                        inter_id += 1
                intra_id += 1
            person_id += 1
if __name__ == '__main__':
    main('UMUT/ConcatFolders/Output')
