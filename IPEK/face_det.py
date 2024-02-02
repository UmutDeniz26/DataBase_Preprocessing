import os

def detect_best_frontal_face(image_path):
    import math
    from retinaface import RetinaFace

    resp = RetinaFace.detect_faces(image_path)
    if resp:
        landmarks = resp[0]['landmarks']
        nose_point = landmarks['nose']
        left_eye_point = landmarks['left_eye']
        right_eye_point = landmarks['right_eye']

        distance_nose_left_eye = math.sqrt((left_eye_point[0] - nose_point[0])**2 + (left_eye_point[1] - nose_point[1])**2)
        distance_nose_right_eye = math.sqrt((right_eye_point[0] - nose_point[0])**2 + (right_eye_point[1] - nose_point[1])**2)
        difference_between_le_re = abs(distance_nose_left_eye - distance_nose_right_eye)

        return difference_between_le_re
    else:
        return float('inf')  # Return infinity if no face detected


# Veri setinin bulunduğu dizin
dataset_path = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\lfw-deepfunneled"

# Çıktı dosyasının adı
output_file = 'outputlast.txt'

# Başlangıç klasör numarası
folder_number = 0

# Dosya açma işlemi
with open(output_file, 'w') as file:
    # Ana dizindeki klasörleri listele
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        
        # Eğer bir klasörse devam et
        if os.path.isdir(person_path):
            best_image_path = None
            best_difference = float('inf')  # Initialize with infinity
            
            # Person'a ait tüm alt klasörlerdeki görselleri listele
            for image_file in os.listdir(person_path):
                # Dosya uzantısını kontrol et, sadece JPEG dosyalarını işle
                if image_file.lower().endswith('.jpg'):
                    # Dosya adını ve yolunu oluştur
                    image_path = os.path.join(person_path, image_file)

                    # Yüzün en düzgün göründüğü resmi seç
                    difference = detect_best_frontal_face(image_path)
                    if difference < best_difference:
                        best_difference = difference
                        best_image_path = image_path
                        
            if best_image_path:
                # Dosya adını yazdır
                file.write(f'{folder_number:05d}_{os.path.basename(best_image_path)}\n')  # Klasör numarası + dosya adı
            else:
                file.write(f'{folder_number:05d}_NoFrontalImage\n')  # Eğer düzgün resim bulunamazsa

            folder_number += 1  # Klasör numarasını bir artır

# Bilgileri içeren txt dosyası oluşturuldu
print(f'Liste oluşturuldu ve {output_file} adında kaydedildi.')
