import os


def delete_files_with_error(folder_path):
    i=0
    twoface_folder = os.path.join(folder_path, "twoface")
    os.makedirs(twoface_folder, exist_ok=True)
    print("twofacec_folder oluşturuldu")
    
    deleted_files = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print('file:',file)
            if file.endswith('.txt'):
                txt_path = os.path.join(root, file)
                with open(txt_path, 'r') as txt_file:
                    content = txt_file.read()
                    #print(content)
                    # Txt içersinde Error geçiyorsa
                    if "Error" in content:
                        #print(txt_path)
                        #print(content)
                        os.remove(txt_path)  # txt dosyasını sil
                        print('Txt silindi: ',txt_path)
                        deleted_files.append(txt_path)
                        
                        img_path = os.path.splitext(txt_path)[0] + '.jpg'  # img dosyasının yolunu oluştur
                        if os.path.exists(img_path):
                            os.remove(img_path)  # img dosyasını sil
                            print('Img silindi: ',img_path)
                            deleted_files.append(img_path)
                            
    # Silinen dosya yollarını deleted.txt dosyasına yazıyor
    with open(os.path.join(folder_path, "deleted.txt"), 'w') as f:
        for file_path in deleted_files:
            f.write(file_path + '\n')
                       
folder_path = 'YoutubeFace'
delete_files_with_error(folder_path)
