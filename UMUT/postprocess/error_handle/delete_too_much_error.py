import os
import shutil

def main(txt_path):
    with open(txt_path, "r") as f:
        content = f.readlines()

        for line in content:
            file_path = line.strip()
            file_path = os.path.normpath(file_path).replace("\\", "/")
            file_path_slices = file_path.split(os.sep)
            upper_dir_path = os.path.join(os.sep.join(file_path_slices[:-2]))
            if not os.path.exists(upper_dir_path):
                continue
            shutil.rmtree(upper_dir_path)
            print(f"Deleted: {upper_dir_path}")

            
            

if __name__ == "__main__":
    main("UMUT/Error_Handle/error_path_smaller_than_5.txt")
            