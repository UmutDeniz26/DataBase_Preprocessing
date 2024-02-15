# her klasörde max 200 img olacak şekilde veri seti New_YoutubeFace adında güncellendi.

import os
import shutil
import random
import numpy as np

def newFolder(subfolder_path, new_dataset_name, person_name, subfolder_name,selected_images):
    # Yeni klasörün oluşturulacağı yol
    yeni_klasor_yolu = os.path.join(new_dataset_name, person_name, subfolder_name)

    # Yeni klasörü oluştur (exist_ok=True, klasör zaten varsa hata vermez)
    os.makedirs(yeni_klasor_yolu, exist_ok=True)

    # Her bir seçilen görüntüyü yeni klasöre kopyala
    for secilen_gorsel in selected_images:
        # Mevcut görüntünün yolu
        gorsel_yolu = os.path.join(subfolder_path, secilen_gorsel)
        # Yeni klasöre kopyalanacak görüntünün hedef yolu
        yeni_gorsel_yolu = os.path.join(yeni_klasor_yolu, secilen_gorsel)
        # Görüntüyü kopyala
        shutil.copy(gorsel_yolu, yeni_gorsel_yolu)

    """
    if len(selected_images)>195:
        print(gorsel_yolu,"  to  ", yeni_gorsel_yolu)
        exit()
    """

def imgReduction(subfolder_path,N=201):
    total_img = len(sorted(os.listdir(subfolder_path)))
    print(total_img, subfolder_path)
    if total_img <= N:
        selected_images = sorted(os.listdir(subfolder_path))


    else:
        image_files = sorted(os.listdir(subfolder_path))
        minVal = 0
        maxVal = len(sorted(os.listdir(subfolder_path)))
        interval = np.floor((maxVal-minVal)/N)

        x1 = np.linspace(minVal, maxVal, N, endpoint=True)
        arr = np.floor(x1).astype(int)
        #print(arr)
        new_arr = []
        #print(len(np.unique(arr)),len(arr))

        for number in arr:
            sign = np.random.randint(1)
            offset = np.random.randint(interval)
            number = number + offset * (-1) ** (sign)
            new_arr.append(number)

        new_arr[0] = 0
        selected_images = [image_files[i % len(image_files)] for i in new_arr]
        #print(len(selected_images))
        if len(np.unique(new_arr)) == len(new_arr):
            #print(new_arr)
            True
        else:
            print("Error")
    return selected_images

def main(dataset_path, new_dataset_name):
    # Veri setinin bulunduğu dizin -> dataset_path
    # Yeni klasör adı               -> new_dataset_name


    from collections import Counter

    for person_name in sorted(os.listdir(dataset_path)):
        person_path = os.path.join(dataset_path, person_name)

        if os.path.isdir(person_path):
            person_images = []

            for subfolder_name in sorted(os.listdir(person_path)):
                subfolder_path = os.path.join(person_path, subfolder_name)
                #print(subfolder_path)
                if os.path.isdir(subfolder_path):
                    selected_images = imgReduction(subfolder_path)

                    if len(selected_images) >195:
                        for selected_image in selected_images:
                            if selected_images.count(selected_image) > 1:
                                selected_images.pop(-1)

                    newFolder(subfolder_path, new_dataset_name, person_name, subfolder_name,selected_images)
                    """total_img = len(sorted(os.listdir(subfolder_path))
                    print(total_img)
                    if total_img <= 200:
                        newFolder(subfolder_path, new_dataset_name, person_name, subfolder_name,selected_images=None)

                    else:
                        selected_images = imgReduction(subfolder_path, N=200)
                        newFolder(subfolder_path, new_dataset_name, person_name, subfolder_name,selected_images)"""

if __name__ == "__main__":
    main( dataset_path="./Elif/YoutubeFace/YoutubeFace_all",
          new_dataset_name='./Elif/YoutubeFace/YoutubeFace')
