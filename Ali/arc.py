import os

def main(dataset_path, output_file):
    counter = 0
    n = 0

    with open(output_file, 'w') as file:
        # Ana dizindeki klasörleri listele
        for main_folder in sorted(os.listdir(dataset_path)):
            main_folder_path = os.path.join(dataset_path, main_folder)

            # Klasörleri kontrol et ve içerisindeki dosyaları listele
            if os.path.isdir(main_folder_path):
                # Person'a ait tüm alt klasörlerdeki görselleri listele
                for subfolder_name in sorted(os.listdir(main_folder_path)):
                    subfolder_path = os.path.join(main_folder_path, subfolder_name)

                    if os.path.isdir(subfolder_path):
                        # Alt klasördeki dosyaları listele
                        for image_file in sorted(os.listdir(subfolder_path)):
                            person_number = f'{counter:04d}'
                            img_number = f'{n:06d}'

                            file.write(f'{person_number}_{subfolder_name}_{img_number}\n')
                            n += 1

                counter += 1

    print(f'Liste oluşturuldu ve {output_file} adında kaydedildi.')

if __name__ == "__main__":
    main(dataset_path="./Ali/YoutubeFace",
         output_file='new.txt')
