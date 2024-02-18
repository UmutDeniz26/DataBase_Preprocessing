"""READMED: Hangi klasörde kaç tane twofaceError ve unknownError olduğunu gösteriyor.
 Unknown error çok olduğu klasörleri el ile temizleyeceğim. Ardından çok fazla klasörde unkError olmadığı için
 deleted_unknown_error fonksiyonu ile unkError sileceğim."""
import os
import json
import math
import shutil
import sys

def main(folder_path,output_file):
    
    
    with open(output_file, 'w') as file_w:
        file_w.write("Subfolfer_path                                                 | txt_cnt     |noError   |twoFace          |pE       |unkn         |tE_rate       |uE_rate         |tE     |uE     |pE\n")
        a = 0
        uE = 0
        tE = 0
        pE = 0
        for person_name in os.listdir(folder_path):
                person_path = os.path.join(folder_path, person_name)
                # Klasörleri kontrol et ve içerisindeki dosyaları listele
                if os.path.isdir(person_path):
                    person_files = []
                    for subfolder_name in os.listdir(person_path):
                        subfolder_path = os.path.join(person_path, subfolder_name)
                    
                       # print(error_counts)

                        txt_cnt = 0
                        unknownError = 0
                        noError = 0
                        pass_E = 0
                        twoFace = 0

                        if os.path.isdir(subfolder_path):
                            # Alt klasördeki dosyaları listele
                            for inner_file in os.listdir(subfolder_path):
                                inner_path = os.path.join(subfolder_path, inner_file)
                                if inner_file.endswith(('.txt')):
                                    txt_cnt += 1
                                    with open(inner_path, "r") as file:
                                        content = file.read()
                                        #print(content)
                                        #content = json.loads(content)

                                        #if content.strip() == {}:
                                        #    b +=1

                                        if "TwoPeopleDetected" in content :
                                            twoFace +=1
                                            tE += 1
                                            #for error_type in error_counts:
                                                #if error_type in content:
                                                    #error_counts[error_type] += 1
                                        
                                        elif "right_eye" in content:
                                            noError +=1
                                        
                                        elif "pass_exception" in content:
                                            pass_E += 1
                                            pE+=1

                                        else:
                                            unknownError += 1
                                            uE += 1
                                            
                                            #deleted_unknown_error(subfolder_path, inner_path)
                            # her klasör için oranları yazalım
                            uE_rate = (unknownError / txt_cnt)
                            uE_rate = f"{uE_rate:.4f}"
                            tE_rate = (twoFace / txt_cnt)
                            tE_rate = f"{tE_rate:.4f}"

                            txt_cnt = f'{txt_cnt:06d}'
                            noError = f'{noError:06d}'
                            twoFace = f'{twoFace:06d}'
                            pass_E = f'{pass_E:06d}'
                            unknownError = f'{unknownError:06d}'            

                            if txt_cnt != noError: 
                                a = int(a)
                                a += 1
                                a = f'{a:04d}'    
                                person_files.append(f'{a}__{subfolder_path}       {txt_cnt}        {noError}        {twoFace}        {pass_E}      {unknownError}       {tE_rate}       {uE_rate}        {tE}         {uE}      {pE}')

                    file_w.write('\n'.join(person_files) + '\n')
                    
                    #print(subfolder_path,'\n')

if __name__ == '__main__':
    main( folder_path = './Elif/Two_Face_Handle/Output_copy',
         output_file='./Elif/Two_Face_Handle/error_newlist_afterunkWDeleted.txt')



