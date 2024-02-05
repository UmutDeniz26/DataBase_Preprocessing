import numpy as np
from skimage import transform  
#pip install scikit-image
import cv2
from skimage import transform as tform
def face_align_landmark(img, landmark,image_size=(128,128),method ="similar"):
    tform= transform.AffineTransform() if method == "affine" else transform.SimilarityTransform()
    src=np.array(
        [[38.2946,51.6963],[73.5318,51.5014],[56.0252,71.7366],[41.5493,92.3655],[70.729904,92.2041]],dtype=np.float32
    )
    tfrom.estimate(landmark,src)
    #ndimage = transform.warp(img, tform.inverse,output_shape=image_size)
    #ndimage =(ndimage * 255).astype(np.uint8)
    M=tform.params[0:2,:]
    ndimage = cv2.warpAffine(img, M ,image_size,borderValue=0.0)
    if len (ndimage.shape) == 2:
        ndimage = np.stack([ndimage ,ndimage, ndimage],-1)
    else:
        ndimage=cv2.cvtColor(ndimage,cv2.COLOR_BGR2GRAY)
    return ndimage
