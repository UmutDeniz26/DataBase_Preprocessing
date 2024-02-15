import os

def delete_files_with_error(folder_path):
    i=0
    twoface_folder = os.path.join(folder_path, "twoface")
    os.makedirs(twoface_folder, exist_ok=True)
    print("twofacec_folder oluşturuldu")

    deleted_files = []

    errorCounter = 0;root_holder = ''

    too_much_error_txt_path = os.path.join(folder_path, "too_much_error.txt")
    too_much_error = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            #print('file:',file)
            if file.endswith('.txt'):
                txt_path = os.path.join(root, file)
                with open(txt_path, 'r') as txt_file:
                    content = txt_file.read()
                    #print(content)
                    # Txt içersinde Error geçiyorsa
                    if "Error" in content:
                        errorCounter += 1
                        print(txt_path)
                        #print(content)
                        # -> os.remove(txt_path)  # txt dosyasını sil
                        # print('Txt silindi: ',txt_path)
                        deleted_files.append(txt_path)

                        img_path = os.path.splitext(txt_path)[0] + '.jpg'  # img dosyasının yolunu oluştur
                        if os.path.exists(img_path):
                            # -> os.remove(img_path)  # img dosyasını sil
                            # print('Img silindi: ',img_path)
                            deleted_files.append(img_path)
                            True

        if root != root_holder or root_holder=='':
            len_files = int((len(files)-1)/2)
            len_files = 1 if len_files == 0 else len_files

            #print("Error Counter: ",errorCounter)
            #print("Len files: ", int((len(files)-1)/2))
            #print("Root: ",root)

            # if errorCounter/len_files > 0.8 then dont delete,
            if errorCounter/len_files > 0.3:
                too_much_error.append(root)
            # else delete all
            elif errorCounter != 0:
                #deleted_files.append(root)
                True
            errorCounter = 0
        root_holder = root

    # Silinen dosya yollarını deleted.txt dosyasına yazıyor
    with open(os.path.join(folder_path, "deleted.txt"), 'w') as f:
        for file_path in deleted_files:
            f.write(file_path + '\n')
    with open(too_much_error_txt_path, 'w') as f:
        for file_path in too_much_error:
            f.write(file_path + '\n')


folder_path = 'Elif/foldered'
delete_files_with_error(folder_path)
