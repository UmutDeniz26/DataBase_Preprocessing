import os

# Veri setinin bulunduğu dizin
dataset_path = "/home/ali/Desktop/github/DataBase_Preprocessing/Ali/CASIA-FaceV5(BMP)"

# Çıktı dosyasının adı
output_file = '/home/ali/Desktop/github/DataBase_Preprocessing/Ali/outputlast.txt'

# Başlangıç klasör numarası
folder_number = 0

# Dosya açma işlemi
with open(output_file, 'w') as file:
    # Ana dizindeki klasörleri listele
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)

        # Eğer bir klasörse devam et
        if os.path.isdir(person_path):
            # Başlangıç sayacı
            counter = 0

            # Person'a ait tüm alt klasörlerdeki görselleri listele
            for image_file in os.listdir(person_path):
                # Dosya uzantısını kontrol et, sadece JPEG dosyalarını işle
                if image_file.lower().endswith('.bmp'):
                    # Dosya adını ve yolunu oluştur
                    image_path = os.path.join(person_path, image_file)

                    # Dosya adını yazdır
                    file.write(f'{folder_number:03d}_{counter:0d}\n')  # Klasör numarası + sayacı formatla
                    counter += 1  # Sayacı bir artır
            folder_number += 1  # Klasör numarasını bir artır

# Bilgileri içeren txt dosyası oluşturuldu
print(f'Liste oluşturuldu ve {output_file} adında kaydedildi.')
