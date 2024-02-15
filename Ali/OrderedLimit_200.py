import sys
sys.path.insert(0,'Elif/YoutubeFace')
import img_sayısı_200
import listeleme_sirali

dataset_path="./Ali/1468-1598"
output_file='./Ali/YoutubeFace.txt'
output_folder = './Ali/YoutubeFace'

img_sayısı_200.main(dataset_path,output_folder)
listeleme_sirali.main(output_folder, output_file)
