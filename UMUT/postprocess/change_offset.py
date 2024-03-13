import os

def main(src_dataset, dst_dataset):
    src_dataset = os.path.normpath(src_dataset)
    dst_dataset = os.path.normpath(dst_dataset)

    for root, dirs, files in os.walk(dst_dataset):
        for file in files:
            if not file.endswith(".jpg"):
                file_path = os.path.join(root, file)
                file_path = os.path.normpath(file_path)
                print(f"file_path: {file_path}")
                
    

if __name__ == "__main__":
    main(src_dataset = "casia-webface_FOLDERED",
            dst_dataset = "casia-webface_FOLDERED_OFFSET")