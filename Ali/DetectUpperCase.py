import os

def save_second_letter_upper(directory, output_file):
    counterTwoLetter = 0
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
                counterTwoLetter+=1
                uppercase_files.append(filename)

    # Büyük harf içeren dosyaları belirtilen metin dosyasına yaz
    with open(output_file, 'w') as file:
        for filename in uppercase_files:
            file.write(filename + '\n')
    return counterTwoLetter

def rename_second_letter_lowercase(directory):
    counterTwoLetter = 0
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
                counterTwoLetter+=1
                # Dosya adını değiştir
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                os.rename(old_path, new_path)

    return counterTwoLetter
