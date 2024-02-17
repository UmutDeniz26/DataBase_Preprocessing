# sıralı olaral listeledik. txt ve img aynı id aldı.
import os
import shutil

def main(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                src_txt_id = int(file.split('.')[0])
                src_img_id = src_txt_id-1

                old_id = file.split('.')[0]
                new_id = int(file.split('.')[0]) - 1

                new_id_half = int( int(new_id) * 1.0 / 2 * 1.0)
                old_id_half = int( int(old_id) * 1.0 / 2 * 1.0)

                new_id_half = f'{new_id_half:08d}'
                old_id_half = f'{old_id_half:08d}'
                new_id = f'{new_id:08d}'

                os.rename(os.path.join(root, f'{src_txt_id:08d}' + '.txt') , os.path.join(root, new_id_half + '.txt'))
                os.rename(os.path.join(root, f'{src_img_id:08d}' + '.jpg') , os.path.join(root, new_id_half + '.jpg'))


if __name__ == "__main__":
    main("Elif\Two_Face_Handle\Output_copy")
