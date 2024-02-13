import sys
sys.path.insert(0,'Elif/YoutubeFace')
import img_sayısı_200
import listeleme_sirali

dataset_path="./UMUT/YoutubeFace"
output_file='./UMUT/YoutubeFace.txt'
output_folder = './UMUT/YoutubeFace200'

img_sayısı_200.main(dataset_path,output_folder)
listeleme_sirali.main(output_folder, output_file)
