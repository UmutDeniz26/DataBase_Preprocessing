import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
from skimage import transform
import torch



class Torch_model_interf:
    def __init__(self, model_file, image_size=(112, 112)):
        import torch
        self.torch = torch
        cvd = os.environ.get("CUDA_VISIBLE_DEVICES", "").strip()
        device_name = "cuda:0" if len(cvd) > 0 and int(cvd) != -1 else "cpu"
        self.device = self.torch.device(device_name)
        
        try:
            self.model = self.torch.jit.load(os.path.join(os.getcwd(), model_file), map_location=device_name)
        except:
            print("Error: %s is weights only, please load and save the entire model by `torch.jit.save`" % model_file)
            self.model = None

    def __call__(self, imgs):
        
        cv2.imwrite(str(imgs.shape)+".jpg", imgs[0])
        
        imgs = imgs.transpose(0, 3, 1, 2).copy().astype("float32")
        imgs = (imgs - 127.5) * 0.0078125
        print(imgs.shape)
        
        output = self.model(self.torch.from_numpy(imgs).to(self.device).float())#Burası çalışmıyor
        exit()
        return output.cpu().detach().numpy()


def face_align_landmark(img, landmark, image_size=(112, 112), method="similar"):
    tform = transform.AffineTransform() if method == "affine" else transform.SimilarityTransform()
    src = np.array(
        [[38.2946, 51.6963], [73.5318, 51.5014], [56.0252, 71.7366], [41.5493, 92.3655], [70.729904, 92.2041]], dtype=np.float32
    )
    
    tform.estimate(landmark, src)
    # ndimage = transform.warp(img, tform.inverse, output_shape=image_size)
    # ndimage = (ndimage * 255).astype(np.uint8)
    M = tform.params[0:2, :]
    ndimage = cv2.warpAffine(img, M, image_size, borderValue=0.0)
    
    if len(ndimage.shape) == 2:
        ndimage = np.stack([ndimage, ndimage, ndimage], -1)
    else:
        ndimage = cv2.cvtColor(ndimage, cv2.COLOR_BGR2RGB)

    return ndimage


def get_embeddings(model_interf, img_names, landmarks, batch_size=5, flip=True):
    steps = int(np.ceil(len(img_names) / batch_size))
    embs, embs_f = [], []
    for batch_id in tqdm(range(0, len(img_names), batch_size), "Embedding", total=steps):
        batch_imgs, batch_landmarks = img_names[batch_id : batch_id + batch_size], landmarks[batch_id : batch_id + batch_size]
        ndimages = [face_align_landmark(cv2.imread(img), landmark) for img, landmark in zip(batch_imgs, batch_landmarks)]
        ndimages = np.stack(ndimages)    

        embs.extend(model_interf(ndimages))
    
        if flip:
            embs_f.extend(model_interf(ndimages[:, :, ::-1, :]))
    return np.array(embs), np.array(embs_f)

model_file= "ms1m_v3_arcface_r100_fp16.pth"
interf_func = Torch_model_interf(model_file)

images_folder = "YoutubeFace_FOLDERED"
img_names = []
landmarks = []

import txtFileOperations

counter=0
for file in os.scandir(images_folder):
    for subfile in os.scandir(file.path):
        for subsubfile in os.scandir(subfile.path):
            counter+=1
            if counter>10:
                break
            print(subsubfile.name)
            if subsubfile.is_file() and subsubfile.name.endswith(".jpg"):
                img_names.append(subsubfile.path)
            if subsubfile.is_file() and subsubfile.name.endswith(".txt"):
                file_path = subsubfile.path
                temp_dict = txtFileOperations.readJsonDictFromFile(file_path)
                landmarks.append( list(temp_dict.values())[0:-1] )
                
                
#print(img_names)
#print(landmarks)
landmarks = [landmarks] + [landmarks] # two batches
img_names = [img_names] + [img_names]

for img_name, landmark in zip(img_names, landmarks):
    embs, embs_f = get_embeddings(interf_func, img_name, landmark, batch_size=5, flip=True)
    print(embs)


    
