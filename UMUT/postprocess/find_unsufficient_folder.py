import os 

def main(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if len(files) < 100:
            print(root, len(files))

if __name__ == "__main__":
    main("")