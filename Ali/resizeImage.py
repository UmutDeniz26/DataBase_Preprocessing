import os
import cv2


def resize_and_overwrite_images(root_directory, target_width=120, target_height=96):
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Eğer dosya bir görsel dosyası ise
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Görseli oku
                img = cv2.imread(file_path)

                # Görseli belirtilen boyuta yeniden boyutlandır cv2.INTER_LINEAR (bilineer interpolasyon) yöntemidir.
                resized_img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

                # Yeniden boyutlandırılmış görseli orijinal dosyanın üzerine kaydet
                cv2.imwrite(file_path, resized_img)

    print("Yeniden boyutlandırma ve üzerine yazma tamamlandı.")

path = r"UMUT/database/LFPW_FOLDERED_without_errors"
resize_and_overwrite_images(path)
