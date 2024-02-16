import os
import txtFileOperations

def main(folder_path,data_base_name,upper_folder_name):
    print(txtFileOperations.initMainTxtFile(data_base_name,upper_folder_name,
        ["file_path","inter","intra","right_eye","left_eye","nose","mouth_right","mouth_left"]))


    inter = 0
    intra = 0

    for root , dirs, files in os.walk(folder_path):
        if len(files) > 1:
            for file in files:
                if file.endswith(".txt"):
                    resp_dict = txtFileOperations.readJsonDictFromFile(os.path.join(root,file))
                    print(resp_dict)
                    txtFileOperations.writeFileMainTxt(os.path.join(root,file), resp_dict, inter, intra)
                    intra+=1
            inter+=1




if __name__ == "__main__":
    main(folder_path="UMUT/AFW_FOLDERED",data_base_name="AFW",upper_folder_name="UMUT")
