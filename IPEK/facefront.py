import os
import cv2 as cv

# Initialize the face detector
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kullanıcıdan kodun bulunacağı klasörü iste
folder_path = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\lfw-deepfunneled"

# Kullanıcıdan işlenmiş resimlerin kaydedileceği klasörü iste
output_folder = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\frontal"

# Klasördeki tüm dosyaları al
files = os.listdir(folder_path)

# İşlenmiş resimlerin kaydedileceği klasörü oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Her dosya için işlem yap
for file in files:
    # Dosya yolunu oluştur
    file_path = os.path.join(folder_path, file)
    
    # Dosya bir resim dosyası mı kontrol et
    if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"Yüzler {file} dosyasında bulunuyor:")
        
        # Dosyayı aç ve işlemleri yap
        img = cv.imread(file_path)
        
        # Gri tonlamaya dönüştür
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        # Yüz tespiti yap
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Yüzleri işaretle
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # İşlenmiş resmi ayrı bir klasöre kaydet
        output_file_path = os.path.join(output_folder, file)
        cv.imwrite(output_file_path, img)
        print(f"İşlenmiş görüntü {output_file_path} olarak kaydedildi.")
