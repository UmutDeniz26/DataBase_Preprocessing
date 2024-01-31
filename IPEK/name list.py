import os

# Veri setinin bulunduğu dizin
dataset_path = r"C:\Users\ipekb\Desktop\file detect\lfw-deepfunneled"

# Çıktı dosyasının adı
output_file = 'output4.txt'

# Dosya açma işlemi
with open(output_file, 'w') as file:
    # Ana dizindeki klasörleri listele
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)

        # Klasörleri kontrol et ve içerisindeki dosyaları listele
        if os.path.isdir(person_path):
            # Person'a ait tüm alt klasörlerdeki görselleri listele
           
                    # Alt klasördeki dosyaları listele
                    for image_file in os.listdir(person_path):
                        # Dosya adını ve yolunu oluştur
                        image_path = os.path.join(person_path, image_file)

                        # Dosya adını yazdır
                        file.write(f'{person_name}_{image_file}\n')

# Bilgileri içeren txt dosyası oluşturuldu
print(f'Liste oluşturuldu ve {output_file} adında kaydedildi.')
