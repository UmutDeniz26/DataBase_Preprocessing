import os
def run(txt_path, resp):
    new_dict = {key: value for key, value in resp.items() if key not in ['distance_nose_left_eye', 'distance_nose_right_eye', 'difference_between_le_re']}
    keys = list(new_dict.keys())

    if txt_path.endswith(".bmp"):
        txt_path = txt_path.replace(".bmp", ".txt")
    if txt_path.endswith(".jpg"):
        txt_path = txt_path.replace(".jpg", ".txt")

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
