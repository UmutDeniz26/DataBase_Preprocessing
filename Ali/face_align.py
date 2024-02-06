import numpy as np
import cv2
from skimage import transform
import matplotlib.pyplot as plt

def face_align_landmark(img, landmark, image_size=(128, 128), method="similar"):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if method == "affine":
        tform = transform.AffineTransform()
    else:
        tform = transform.SimilarityTransform()

    src = np.array(
        [[38.2946, 51.6963], [73.5318, 51.5014], [56.0252, 71.7366], [41.5493, 92.3655], [70.729904, 92.2041]],
        dtype=np.float32
    )
    tform.estimate(landmark, src)

    M = tform.params[0:2, :]
    ndimage = cv2.warpAffine(img, M, image_size, borderValue=0.0)
    if len(ndimage.shape) == 2:
        ndimage = np.stack([ndimage, ndimage, ndimage], -1)
    else:
        ndimage = cv2.cvtColor(ndimage, cv2.COLOR_BGR2GRAY)

    return ndimage
img = cv2.imread("/home/ali/Desktop/github/DataBase_Preprocessing/Ali/CASIA-FaceV5(BMP)/Face/000/000_1.bmp")

landmark = [[323.50842, 193.07437],[270.62537, 203.47632],[296.82043, 229.079],[326.9064, 247.5332],[286.04813, 255.89275]]
landmark = np.array(landmark)

def save_image_to_txt(image, output_path):
    np.savetxt(output_path, image.flatten(), delimiter=",")

img = cv2.imread("/home/ali/Desktop/github/DataBase_Preprocessing/Ali/CASIA-FaceV5(BMP)/Face/000/000_0.bmp")
landmark = [[323.50842, 193.07437], [270.62537, 203.47632], [296.82043, 229.079], [326.9064, 247.5332], [286.04813, 255.89275]]
landmark = np.array(landmark)
aligned_face = face_align_landmark(img, landmark)
plt.imshow(aligned_face)
plt.show()
output_path = "/home/ali/Desktop/github/DataBase_Preprocessing/Ali/aligned_face.txt"
save_image_to_txt(aligned_face, output_path)