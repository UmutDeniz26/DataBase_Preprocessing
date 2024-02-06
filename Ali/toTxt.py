import os
import json
def run(folder_path):
    file_paths = []
    data_dicts = []  
    file_names = sorted([filename for filename in os.listdir(folder_path) if filename.split('_')[0].isdigit()], key=lambda x: int(x.split('_')[0]))
    for filename in sorted(file_names):

        if filename.endswith(('.bmp')):
            image_path = os.path.join(folder_path, filename)
            image_path = image_path.replace('./Ali/', "")
            image_path = image_path.replace('bmp', "jpg")
            file_paths.append(image_path)
        if filename.endswith(('.txt')):
            txt_file_path = os.path.join(folder_path, filename)
            with open(txt_file_path, 'r') as file:
                json_data = file.read()
            data_dict = json.loads(json_data)
            data_dicts.append(data_dict)
    return file_paths, data_dicts

def data(folder_path):
    max_abs_value = 999999
    file_paths = []
    file_path_features = []
    file_names = sorted([filename for filename in os.listdir(folder_path) if filename.split('_')[0].isdigit()], key=lambda x: int(x.split('_')[0]))
    for filename in file_names:
        if filename.endswith(('.txt')):
            
            txt_file_path = folder_path + "/" +filename  # TXT dosyasının yolunu belirtin
            with open(txt_file_path, 'r') as file:
                json_data = file.read()
            data_dict = json.loads(json_data)

            file_path_features.append(data_dict)
    return file_paths


source_folder = "./Ali/CASIA-FaceV5(BMP)/Face/"
destination_folder = "./Ali/CASIA-FaceV5(BMP)/Face"


file_paths_list_feature = []
for filename in os.listdir(source_folder):
    image_path = os.path.join(source_folder, filename)
    file_paths, data_dicts = run(image_path)

# Dosyaları kaydetmek için yeni adlar oluşturun
    file_paths_filename = "./sorted_file_paths.txt"
    data_dicts_filename = "./features.txt"

        # Dosyaları oluşturun ve içerikleri yazın
    with open(file_paths_filename, 'a') as file:
        for path in file_paths:
            file.write(path + '\n')

    with open(data_dicts_filename, 'a') as file:
        for data_dict in data_dicts:
            file.write(json.dumps(data_dict, ensure_ascii=False) + '\n')

    with open("./sorted_file_paths.txt", "r") as file:
        file_paths_content = file.readlines()

    with open("./features.txt", "r") as file:
        data_dicts_content = file.readlines()
        
    combined_content = [f"{file_path.strip()},{data_dict.strip()},\n" for file_path, data_dict in zip(file_paths_content, data_dicts_content)]
    # Birleştirilmiş veriyi yeni bir dosyaya yazma
    with open("combined_file.txt", "w") as file:
        file.writelines(combined_content)
    with open("combined_file.txt", "r") as file:
        combined_content = file.readlines()

    def custom_sort(line):
        folder_part = line.split(' ')[0].split('CASIA-FaceV5(BMP)/Face/')[1].split('/')[0]
        file_part = line.split(' ')[0].split('CASIA-FaceV5(BMP)/Face/')[1].split('/')[1]
        return (folder_part, file_part)

# Satırları özel sıralama fonksiyonu kullanarak sıralama
    sorted_content = sorted(combined_content, key=custom_sort)

# Sıralanmış veriyi yeni bir dosyaya yazma  
    with open("sorted_combined_file.txt", "w") as file:
        file.writelines(sorted_content)

# file_paths_list = []
# for filename in os.listdir(source_folder):
#     image_path = os.path.join(source_folder, filename)
#     file_paths_list, data_dicts_list = run(image_path)
#  # Değişiklik: data_dicts_list adlı yeni bir değişken ekleniyor

# output_txt_path = "./sorted_file_paths.txt"
# try:
#     with open(output_txt_path, 'a') as file:
#         for file_path, data_dict in zip(file_paths_list, data_dicts_list):        
#             file.write(f"{file_path} {json.dumps(data_dict, ensure_ascii=False)}\n")
# except Exception as e:
#     print(f"Hata oluştu: {e}")

# output_txt_path1 = "./features.txt"
# with open(output_txt_path1, 'a') as file:
#     for file_path in (file_paths_list_feature):
#         file.write(json.dumps(data_dict) + '\n')
# print(f"Sıralanmış dosya yolları {output_txt_path} dosyasına kaydedildi.")
