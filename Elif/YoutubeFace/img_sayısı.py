import os

# Veri setinin bulunduğu dizin
dataset_path = "./Elif/Two_Face_Handle/Output_copy"

# Çıktı dosyasının adı
output_file = './Elif/YoutubeFace/Last_edition.txt'

counter = 0
a=0
b=0

# Dosya açma işlemi
with open(output_file, 'w') as file:
    file.write("PersonName_SubfolderName_TotalImg_MoreThan100Img\n")
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        b +=1

        if os.path.isdir(person_path):
            person_images = []

            for subfolder_name in os.listdir(person_path):
                subfolder_path = os.path.join(person_path, subfolder_name)

                if os.path.isdir(subfolder_path):
                    total_img = len(os.listdir(subfolder_path))
                    if total_img >= 202:
                        a+=1
                        person_images.append(f'{b}_{person_name}_{subfolder_name}_{total_img}_{a}')
                    else:
                        person_images.append(f'{b}_{person_name}_{subfolder_name}_{total_img}_{a}')

            # Person'a ait tüm görselleri tek bir satırda listeleyerek yaz
            file.write('\n'.join(person_images))
            file.write('\n')

            counter += 1

# Bilgileri içeren txt dosyası oluşturuldu
print(f'Liste oluşturuldu ve {output_file} adında kaydedildi.')
