import json

with open("/home/ali/Desktop/github/DataBase_Preprocessing/sorted_combined_file.txt", 'r') as file:
    lines = file.readlines()

# Yeni değişkenleri eklemek için bir liste oluştur
result_lines = []

# Her satır için sıralı bir sayı ekleyerek yeni bir satır oluştur
for i, line in enumerate(lines):
    # Her bir değişkeni virgül gördükten sonra 0 ile ayır
    variables = line.strip().split(', ')

    # Sıralı sayıları ekleyerek yeni bir satır oluştur
    for j, variable in enumerate(variables):
        result_line = f"{j}, {variable}"
        result_lines.append(result_line)

# Oluşturulan yeni satırları bir txt dosyasına yaz
output_txt_path = "/home/ali/Desktop/github/DataBase_Preprocessing/result_combined_file.txt"
with open(output_txt_path, 'w') as output_file:
    for result_line in result_lines:
        output_file.write(result_line + '\n')

print(f"Yeni satırlar {output_txt_path} dosyasına kaydedildi.")
