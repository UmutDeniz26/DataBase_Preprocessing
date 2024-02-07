from retinaface import RetinaFace
import cv2
import matplotlib.pyplot as plt

img_path = "img1.jpg"

img = RetinaFace.extract_faces(img_path,align=True)

#find index of max eleement in a array
array = [1,2,3] 

def max_index(array):
    max = array[0]
    max_index = 0
    for i in range(1, len(array)):
        if array[i] > max:
            max = array[i]
            max_index = i
    return max_index

img_rect = cv2.imread(img_path)
keys = list(img.keys())
offset = 0
for i in range(len(keys)):
    identity = img[keys[i]]
    facial_area = identity["facial_area"]
    landmarks = identity["landmarks"]

    face_img = img_rect[facial_area[1]-offset:facial_area[3]+offset, facial_area[0]-offset:facial_area[2]+offset]

    print("\n\n Iter: ",i,"   Facial Area: ",facial_area)
    print("Landmarks: ",landmarks)
    
    #save faces to faces folder
    cv2.imwrite("faces/face_"+str(i)+".jpg", face_img)
    
#cv2.imshow( "Input", cv2.imread(img_path))
#cv2.imshow( "Output", img_rect)

cv2.waitKey(0)
cv2.destroyAllWindows()

#IGB Dataset Face Align Landmarks