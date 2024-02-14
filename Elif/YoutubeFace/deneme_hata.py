import os

def read_txt_file(txt_file):
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

def count_images_in_folders(dataset_folder):
    image_counts = {}
    for person_id in os.listdir(dataset_folder):
        person_folder = os.path.join(dataset_folder, person_id)
        if os.path.isdir(person_folder):
            image_counts[person_id] = len([f for f in os.listdir(person_folder) if f.endswith('.jpg')])
    return image_counts

def check_dataset_consistency(txt_file, dataset_folder):
    # Txt dosyasını oku
    txt_data = read_txt_file(txt_file)

    # Klasördeki görüntü sayısını al
    image_counts = count_images_in_folders(dataset_folder)

    # Her bir "person" için klasördeki görüntü sayısını kontrol et
    for line in txt_data:
        person_id = line.split('_')[0]  # Person ID'sini al
        img_count = int(line.split('_')[-1]) + 1  # Görüntü sayısını al

        if person_id not in image_counts:
            print(f"Hata: {person_id} için klasör bulunamadı.")
            return False

        if image_counts[person_id] != img_count:
            print(f"Hata: {person_id} için beklenen görüntü sayısı: {img_count}, gerçek sayı: {image_counts[person_id]}")
            return False

    print("Veri seti uyumluluğu doğrulandı.")
    return True


# Kullanım örneği
txt_file = './Elif/YoutubeFace/YoutubeFace.txt'
dataset_folder = './Elif/YoutubeFace/YoutubeFace'

# Veri seti uyumluluğunu kontrol et
check_dataset_consistency(txt_file, dataset_folder)
