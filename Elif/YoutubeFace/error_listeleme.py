import os
import json
import math
import shutil
import sys

def main(folder_path,output_file):
    
    
    with open(output_file, 'w') as file_w:
        file_w.write("Subfolfer_path                                                 | txt_cnt     |noError   |twoFace    |unkn\n")
        a = 0
        for person_name in os.listdir(folder_path):
                person_path = os.path.join(folder_path, person_name)
                # Klasörleri kontrol et ve içerisindeki dosyaları listele
                if os.path.isdir(person_path):
                    person_images = []
                    for subfolder_name in os.listdir(person_path):
                        error_counts = {
                        "two_people_error" : 0,
                        #"stack_overflow_error" : 0,
                        #"too_small_error" : 0,
                        #"landmark_error" : 0,
                        "unknown_error": 0  
                        }
                       # print(error_counts)
                        subfolder_path = os.path.join(person_path, subfolder_name)
                        txt_cnt = 0
                        unknownError = 0
                        noError = 0
                        twoFace = 0

                        if os.path.isdir(subfolder_path):
                            # Alt klasördeki dosyaları listele
                            for image_file in os.listdir(subfolder_path):
                                file_path = os.path.join(subfolder_path, image_file)
                                if image_file.endswith(('.txt')):
                                    txt_cnt += 1
                                    with open(file_path, "r") as file:
                                        content = file.read()
                                        #print(content)
                                        #content = json.loads(content)

                                        #if content.strip() == {}:
                                        #    b +=1

                                        if "TwoPeopleDetected" in content :
                                            twoFace +=1
                                            #for error_type in error_counts:
                                                #if error_type in content:
                                                    #error_counts[error_type] += 1
                                        
                                        elif "right_eye" in content:
                                            noError +=1

                                        else:
                                            unknownError += 1
                                         
                            txt_cnt = f'{txt_cnt:06d}'
                            noError = f'{noError:06d}'
                            twoFace = f'{twoFace:06d}'
                            unknownError = f'{unknownError:06d}'            

                            if txt_cnt != noError: 
                                a = int(a)
                                a += 1
                                a = f'{a:04d}'    
                                person_images.append(f'{a}__{subfolder_path}       {txt_cnt}        {noError}        {twoFace}        {unknownError}')

                    file_w.write('\n'.join(person_images) + '\n')
                    
                    #print(subfolder_path,'\n')

if __name__ == '__main__':
    main( folder_path = './Elif/Two_Face_Handle/Output_copy',
         output_file='./Elif/Two_Face_Handle/error_list.txt')



