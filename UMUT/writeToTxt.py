import os
import Common

def run(txt_path, resp, logFolderPath=False):
    if type(resp) is not dict:
        txt_path = txt_path.replace(".txt", "_FaceNotFound.txt")
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        if logFolderPath != False:
            Common.writeLog(log=txt_path, log_file_path=logFolderPath + '/logFaceNotFound.txt')

        with open(txt_path , 'w') as file:
            file.write("FaceNotFound")
        return "FaceNotFound"
        
    #new_dict = {key: value for key, value in resp.items() if key not in ['distance_nose_left_eye', 'distance_nose_right_eye', 'difference_between_le_re','frontal_score']}
    new_dict = resp
    keys = list(new_dict.keys())

    if txt_path.endswith(".bmp"):
        txt_path = txt_path.replace(".bmp", ".txt")
    if txt_path.endswith(".jpg"):
        txt_path = txt_path.replace(".jpg", ".txt")
    if os.path.isdir(txt_path):
        print("Error: " + txt_path + " is a directory!")
        exit()

    #txt file operations
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    with open(txt_path , 'w') as file:
        file.write("{\n")
        for key, value in new_dict.items():
            if key == keys[-1]:
                file.write(f" \"{key}\" : {value}\n")
            else:
                file.write(f" \"{key}\" : {value},\n")
        file.write("}") 
    return "Added txt: " + txt_path + " successfully!"
