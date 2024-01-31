from detect_distences_of_sides import detect_best_frontal_face
import os
import shutil


def copy_max_abs_image_to_folder(source_folder, destination_folder):
    max_abs_value = -1
    max_abs_image = None

    for filename in os.listdir(source_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png',"bmp")):
            image_path = os.path.join(source_folder, filename)
            result = detect_best_frontal_face(image_path)
            abs_of_dnle_dnre = result["difference_between_le_re"]

            if abs_of_dnle_dnre > max_abs_value:
                max_abs_value = abs_of_dnle_dnre
                max_abs_image = image_path

    if max_abs_image:
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

source_folder = "CASIA-FaceV5(BMP)/Face/"
destination_folder = "CASIA-FaceV5(BMP)/Face/"

for filename in os.listdir(source_folder):

    # Dosyanın tam yolu
    image_path = os.path.join(source_folder, filename)

    # copy_max_abs_image_to_folder fonksiyonunu çağır
    copy_max_abs_image_to_folder(image_path, destination_folder)
