import os

def limit_angles_by_magnitude(angles, target_len):
    angles.sort(key=lambda x: x[1], reverse=True)
    return angles[:target_len]

def sort_angles(txt_path):
    with open(txt_path, "r") as f:
        lines = f.readlines()
    lines.sort(key=lambda x: float(x.split(" ")[1]),reverse=True)
    with open(txt_path, "w") as f:
        for line in lines:
            f.write(line)

def clear_txt(txt_path):
    if not os.path.exists(txt_path):
        os.makedirs(os.path.dirname(txt_path))
        
    with open(txt_path, "w") as f:
        f.write("")

def add_to_txt(txt_path, data):
    with open(txt_path, "a") as f:
        f.write(data)

def read_lines(txt_path):
    with open(txt_path, "r") as f:
        lines = f.readlines()
    return lines