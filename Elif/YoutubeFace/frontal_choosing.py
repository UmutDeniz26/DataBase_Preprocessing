import os
import json
import math
import shutil
import sys


def deleted_frontal_foldered(subfolder_path):
    frontal_path = os.path.join(subfolder_path, "frontal")
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
    
    if os.path.exists(os.path.join(folder_path,"Frontal_Faces")):
        shutil.rmtree(os.path.join(folder_path,"Frontal_Faces"))
    os.makedirs( os.path.join(folder_path,"Frontal_Faces") ,exist_ok=True)


    for person_name in os.listdir(folder_path):
            person_path = os.path.join(folder_path, person_name)

            # Klasörleri kontrol et ve içerisindeki dosyaları listele
            if os.path.isdir(person_path):
            # file.write(f'{person_name}')

                # Person'a ait tüm alt klasörlerdeki görselleri listele
                person_images = []

                for subfolder_name in os.listdir(person_path):
                    subfolder_path = os.path.join(person_path, subfolder_name)
                    min_abs_value = sys.maxsize
                    img_path = ""
                    if os.path.isdir(subfolder_path):
                        deleted_frontal_foldered(subfolder_path)
                        # Alt klasördeki dosyaları listele
                        for image_file in os.listdir(subfolder_path):
                            image_path = os.path.join(subfolder_path, image_file)
                            if image_file.endswith(('.txt')):
                                try:
                                    with open(image_path, "r") as file:
                                        content = file.read()
                                        content = json.loads(content)
                                except:
                                    print("Error: " + image_file + " is not a valid json file!")
                                    continue
                                try:
                                    distance_nose_left_eye = math.sqrt((content["left_eye"][0] - content["nose"][0])**2 + (content["left_eye"][1] - content["nose"][1])**2)
                                    distance_nose_right_eye = math.sqrt((content["right_eye"][0] - content["nose"][0])**2 + (content["right_eye"][1] - content["nose"][1])**2)
                                    difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)
                                    if difference_between_le_re < min_abs_value:
                                        min_abs_value = difference_between_le_re
                                        img_path = os.path.splitext(image_file)[0] + '.jpg'
                                        #max_abs_image = file.replace(".txt",".jpg")
                                             
                                except:
                                    difference_between_le_re = 1000.0

                        #if min_abs_value == -1 or max_abs_image == "":
                        try:
                            new_frontal_path = os.path.join(subfolder_path, "Frontal")
                                            
                            if os.path.exists(new_frontal_path):
                                shutil.rmtree(new_frontal_path)
                            os.makedirs(new_frontal_path,exist_ok=True)

                            print("Yeni frontal klasörü oluşturuldu: ", new_frontal_path)
                            if img_path and os.path.exists(new_frontal_path):
                                shutil.copy(os.path.join(subfolder_path, img_path), new_frontal_path)
                                shutil.copy(os.path.join(subfolder_path, img_path), os.path.join(folder_path,"Frontal_Faces"))
                                print("Frontal img kopyalandı")
                            #return 0,  '.'.join( os.listdir(root_path)[0].split('.')[:-1] )
                        except FileNotFoundError:
                            print(f"Hata: {img_path} dosyası bulunamadı.")


if __name__ == '__main__':
    main( folder_path = 'Elif/foldered')
