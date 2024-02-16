import os
import shutil

def main(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                old_id = file.split('.')[0]
                new_id = int(file.split('.')[0]) - 1
                new_id = f'{new_id:08d}'
                os.rename(os.path.join(root,file), os.path.join(root, new_id + '.txt'))


if __name__ == "__main__":
    main("UMUT\ConcatFolders\Output")
