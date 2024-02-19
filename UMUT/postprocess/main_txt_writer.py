import os
import sys

sys.path.insert(0, './UMUT')
import txtFileOperations

def main(folder_path,data_base_name,upper_folder_name):
    txt_path = os.path.join(folder_path, data_base_name + "_Info.txt")
    print(txtFileOperations.initMainTxtFile(data_base_name,upper_folder_name,
        ["file_path","inter","intra","right_eye","left_eye","nose","mouth_right","mouth_left"],
        full_path=txt_path, full_path_flag=True))

    inter = 0
    intra = 0
    for root , dirs, files in os.walk(folder_path):
        if len(files) > 1:
            for file in files:
                if file.endswith(".txt"):
                    resp_dict = txtFileOperations.readJsonDictFromFile(os.path.join(root,file))
                    #print(resp_dict)
                    txtFileOperations.writeFileMainTxt( os.path.join(root,file), resp_dict, inter, intra,
                                                        destination=txt_path, full_path_flag=True)
                    intra+=1
            inter+=1

if __name__ == "__main__":
    main(folder_path="UMUT/database/AFW_FOLDERED_without_errors",data_base_name="AFW",upper_folder_name="UMUT")
    main(folder_path="UMUT/database/HELEN_FOLDERED_without_errors",data_base_name="HELEN",upper_folder_name="UMUT")
    main(folder_path="UMUT/database/LFPW_FOLDERED_without_errors",data_base_name="LFPW",upper_folder_name="UMUT")
