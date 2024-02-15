import sys
sys.path.insert(0,'./Elif/YoutubeFace')
import img_sayısı_200
import listeleme_sirali

dataset_path="./IPEK/LFW"
output_file='./IPEK/LFW.txt'
output_folder = './UMUT/YoutubeFace200'

# img_sayısı_200.main(dataset_path,output_folder)
listeleme_sirali.main(dataset_path, output_file)
