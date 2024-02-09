import os

def save_second_letter_upper(directory, output_file):
    # Belirtilen dizindeki dosya listesini al
    file_list = os.listdir(directory)

    # Büyük olan dosyaları tutmak için bir liste oluştur
    uppercase_files = []

    for filename in file_list:
        # Dosya isminin uzunluğunu kontrol et
        if len(filename) >= 2:
            # Dosya isminin ikinci harfini al
            second_letter = filename[1]

            # Eğer ikinci harf büyükse, dosyayı listeye ekle
            if second_letter.isupper():
                uppercase_files.append(filename)

    # Büyük harf içeren dosyaları belirtilen metin dosyasına yaz
    with open(output_file, 'w') as file:
        for filename in uppercase_files:
            file.write(filename + '\n')

# Kullanım örneği:
directory_path = "/path/to/your/directory"
output_file_path = "uppercase_files.txt"
save_second_letter_upper(directory_path, output_file_path)



def rename_second_letter_lowercase(directory):
    # Belirtilen dizindeki dosya listesini al
    file_list = os.listdir(directory)

    for filename in file_list:
        # Dosya isminin uzunluğunu kontrol et
        if len(filename) >= 2:
            # Dosya isminin ikinci harfini al
            second_letter = filename[1]

            # Eğer ikinci harf büyükse, dosya adını güncelle
            if second_letter.isupper():
                new_filename = filename[0] + second_letter.lower() + filename[2:]

                # Dosya adını değiştir
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                os.rename(old_path, new_path)

# Kullanım örneği:
directory_path = "/path/to/your/directory"
rename_second_letter_lowercase(directory_path)
