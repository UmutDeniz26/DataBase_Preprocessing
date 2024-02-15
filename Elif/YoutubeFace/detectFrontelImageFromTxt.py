import os
import json
import math
import shutil
import sys


def deleted_frontal_foldered(root_path):
    frontal_path = os.path.join(root_path, "frontal")
    if os.path.exists(frontal_path) and os.path.isdir(frontal_path):
        # "Foldered" adında bir alt klasör varsa, sil
        try:
            shutil.rmtree(frontal_path)
            print(f"'Foldered' adındaki klasör başarıyla silindi: {frontal_path}")
        except OSError as e:
            print(f"Hata: {frontal_path} klasörü silinirken bir hata oluştu: {e}")
    else:
        print("'Foldered' adında bir alt klasör bulunamadı.")

    

def main(folder_path):
    max_abs_image= ""
    max_abs_value = sys.maxsize

    for root_path,dirs_names,file_names in os.walk(folder_path):
        for file_name in file_names:
            
            file_path = os.path.join(root_path, file_name)
            if os.path.isfile(file_path):
                if file_name.endswith(('.txt')):
                    try:
                        with open(file_path, "r") as file:
                            content = file.read()
                            content = json.loads(content)
                    except:
                        print("Error: " + file_name + " is not a valid json file!")
                        continue
                    try:
                        distance_nose_left_eye = math.sqrt((content["left_eye"][0] - content["nose"][0])**2 + (content["left_eye"][1] - content["nose"][1])**2)
                        distance_nose_right_eye = math.sqrt((content["right_eye"][0] - content["nose"][0])**2 + (content["right_eye"][1] - content["nose"][1])**2)
                        difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)
                        if difference_between_le_re < max_abs_value:
                            max_abs_value = difference_between_le_re
                            max_abs_image = file.replace(".txt","")
                            
                    except:
                        difference_between_le_re = 1000.0

            deleted_frontal_foldered(root_path)

            if max_abs_value == -1 or max_abs_image == "":
                try:
                    new_frontal_path = os.path.join(root_path, "new_frontal")
                    os.makedirs(new_frontal_path) 
                    print("Yeni frontal oluşturuldu: ")
                    shutil.copy(os.path.join(root_path, f"{max_abs_image}.jpg"), new_frontal_path)
                    print("kopyalandı")
                    #return 0,  '.'.join( os.listdir(root_path)[0].split('.')[:-1] )
                except FileNotFoundError:
                    print(f"Hata: '{max_abs_image}.jpg' dosyası bulunamadı.")

            
                    
            
"""   if max_abs_value == -1 or max_abs_image == "":
        try:
            new_frontal_path = os.path.join(root_path, "new_frontal")
            os.makedirs(new_frontal_path) 
            print("Yeni frontal oluşturuldu: ")
            shutil.copy(os.path.join(root_path, f"{max_abs_image}.jpg"), new_frontal_path)
            print("kopyalandı")
            #return 0,  '.'.join( os.listdir(root_path)[0].split('.')[:-1] )
        except FileNotFoundError:
            print(f"Hata: '{max_abs_image}.jpg' dosyası bulunamadı.")
            
                    
                    #return max_abs_value,max_abs_image
"""

if __name__ == '__main__':
    main( folder_path = 'Elif/foldered')


