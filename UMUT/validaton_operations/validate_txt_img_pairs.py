import os

def main(folder_path):
    error_txt_count = 0
    error_img_count = 0
    file_count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_count += 1
            if file.endswith('.txt'):
                img_file = file.replace('.txt', '.jpg')
                img_path = os.path.join(root, img_file)
                if not os.path.exists(img_path) and not 'info' in img_path.lower():
                    print(f'{img_path} does not exist')
                    error_img_count += 1

            if file.endswith('.jpg'):
                txt_file = file.replace('.jpg', '.txt')
                txt_path = os.path.join(root, txt_file)
                if not os.path.exists(txt_path) and not 'frontal' in txt_path.lower():
                    print(f'{txt_path} does not exist')
                    error_txt_count += 1

    print("\nValidation is done\n------------------")
    if error_txt_count == 0 and error_img_count == 0:
        print('All txt and img pairs are valid')
        print(f'File count: {file_count}\n')
    else:
        print(f'Error txt count: {error_txt_count}')
        print(f'Error img count: {error_img_count}\n')

if __name__ == '__main__':
    main('UMUT/casia-webface_FOLDERED')
