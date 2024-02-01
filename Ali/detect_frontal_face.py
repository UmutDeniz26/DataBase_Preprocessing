from detect_distences_of_sides import detect_best_frontal_face
import os
import shutil


def copy_max_abs_image_to_folder(source_folder, destination_folder):
    max_abs_value = -1
    max_abs_image = None
    image_info_dict = {}
    for filename in os.listdir(source_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png',"bmp")):
            image_path = os.path.join(source_folder, filename)
            result = detect_best_frontal_face(image_path)
            abs_of_dnle_dnre = result["difference_between_le_re"]

            if abs_of_dnle_dnre > max_abs_value:
                max_abs_value = abs_of_dnle_dnre
                max_abs_image = image_path

    if max_abs_image:
        if max_abs_value < 11:
            image_info_text = f"Belirlenen eşik değeri altında kalan görsel:\n"
            image_info_text += f"Path: {os.path.abspath(max_abs_image)}\n"
            image_info_text += f"Value: {max_abs_value}\n"
            print(image_info_text)
            
            # Save the information to a text file
            info_file_path = os.path.join(destination_folder, "image_info.txt")
            with open(info_file_path, "a") as info_file:
                info_file.write(image_info_text)
                print(f"Bilgiler '{info_file_path}' dosyasına kaydedildi.")
        else:
            os.makedirs(destination_folder, exist_ok=True)

            # "frontel" adlı bir alt klasör oluştur
            frontel_folder = os.path.join(destination_folder, "frontel")
            os.makedirs(frontel_folder, exist_ok=True)

            # Kaynak ve hedef dosya yollarını kontrol et
            source_path = os.path.abspath(max_abs_image)
            destination_path = os.path.abspath(os.path.join(frontel_folder, os.path.basename(max_abs_image)))

            # Aynı dosya değilse kopyala
            if source_path != destination_path:
                shutil.copy(max_abs_image, frontel_folder)
                print(f"En büyük abs_of_dnle_dnre değerine sahip görsel kopyalandı: {max_abs_image}")
            else:
                print("Kaynak ve hedef dosya yolları aynı, kopyalama işlemi yapılmadı.")
    else:
        print("Görsel bulunamadı.")

