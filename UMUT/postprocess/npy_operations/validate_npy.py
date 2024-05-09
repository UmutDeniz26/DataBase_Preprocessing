import numpy as np
import os
import cv2
def main(npy_folder_path,npy_concat_path=None) -> None:
    """
        Main function for the validation of the npy files.
        
        Args:
            npy_folder_path (str): Path to the npy file
            npy_concat_path (str): Path to the npy file to concatenate with the first one
    """
    data = np.load(npy_folder_path)

    for index,path in enumerate(data["mask"]):
        print("Counter: ",index," Path: ",path) if index%20000==0 else None
        
        try:
            if not os.path.exists(path):
                print("Path is not valid: ", path)
                exit()
        except:
            print("Outer Path is not valid: ", path)
            exit()

    for index,path in enumerate(data["path"]):
        print("Counter: ",index," Path: ",path) if index%20000==0 else None

        try:
            if not os.path.exists(path):
                print("Path is not valid: ", path)
                exit()
        except:
            print("Outer Path is not valid: ", path)
            exit()

    print("\n")
    if npy_concat_path is not None:
        data2 = np.load( npy_concat_path, allow_pickle=True)
        try:
            data3 = np.concatenate((data, data2))
            print("Concatenation is successful")
        except:
            print("Concatenation is not successful")
        print("Data path: ", npy_folder_path)
        print("Concated path: ", npy_concat_path)
        print("Data shape: ", data.shape)
        print("Concated data shape: ", data2.shape)
        print("Output shape: ", data3.shape,"\n")

    print("10 examples from the data: ")
    for i in range(0,300,30):
        print(data[i])

if __name__ == '__main__':
    main(
        npy_folder_path= "casia-webface/_Info.npy", 
        npy_concat_path="src/others/esogu_sets_meta_10_people.npy"
        )
    pass
