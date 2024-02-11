from deepface import DeepFace
img1_path=r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\LFW\Aaron_Peirsol\Aaron_Peirsol_0001.jpg"
img2_path=r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\LFW\Abdoulaye_Wade\Abdoulaye_Wade_0001.jpg"
obj = DeepFace.verify(img1_path,img2_path
          , model_name = 'ArcFace', detector_backend = 'retinaface')
print(obj["verified"])
