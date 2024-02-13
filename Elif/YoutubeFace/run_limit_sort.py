import sys
sys.path.insert(0,'Elif/YoutubeFace')
import img_sayısı_200
import listeleme_sirali

dataset_path="./Elif/YoutubeFace/YoutubeFace_raw"
output_file='./Elif/YoutubeFace200.txt'
output_folder = './Elif/YoutubeFace200'

img_sayısı_200.main(dataset_path,output_folder)
listeleme_sirali.main(output_folder, output_file)
