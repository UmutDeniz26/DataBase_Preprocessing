import os

# Veri setinin bulunduğu dizin
dataset_path = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\LFW"

# Çıktı dosyasının adı ve kaydedileceği dizin
output_directory = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK"
output_file = 'LFW.txt'

# Tam yol oluştur
output_path = os.path.join(output_directory, output_file)

try:
    with open(output_path, 'w') as file:
        # Dizin içindeki her bir kişiyi işle
        for person_number, person_name in enumerate(os.listdir(dataset_path)):
            person_path = os.path.join(dataset_path, person_name)

            # Eğer bir klasörse işlem yap
            if os.path.isdir(person_path):
                # Kişinin fotoğraflarını sayacak bir sayaç
                image_counter = 0

                # Kişinin fotoğraflarını işle
                for image_file in os.listdir(person_path):
                    # Dosya bir JPEG dosyasıysa işle
                    if image_file.lower().endswith('.jpg'):
                        image_path = os.path.join(person_path, image_file)

                        # ID'leri oluştur
                        person_id = f'{person_number:05d}'
                        image_id = f'{image_counter:05d}'

                        # Dosya adını ve tam yolunu yaz
                        file.write(f'{person_id}_{image_id}\n')

                        # Sayaçları arttır
                        image_counter += 1

    print(f'Liste oluşturuldu ve {output_file} adında kaydedildi.')

except Exception as e:
    print(f'Hata: {str(e)}')
