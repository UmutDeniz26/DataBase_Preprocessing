from mtcnn import MTCNN
import cv2
import os

# initialize the MTCNN detector
detector = MTCNN()

# define the folder path containing images
folder_path = r'./IPEK/LFW'

# define the output folder path for saving the best faces
output_folder = r'./IPEK/LFW_BestFaces'

# create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

files = os.listdir(folder_path)

# loop through the images in the folder
for file in files:
        
    inner_folder = folder_path + "/" + file 
    images_paths = os.listdir(inner_folder)
    
    for image_name in images_paths:
        image_path = inner_folder + "/" + image_name
        print(image_path)
    
        # load the image
        image = cv2.imread(image_path)

        # detect faces using MTCNN
        faces = detector.detect_faces(image)

        # variables to track the best face
        best_confidence = 0
        best_face = None

        if len(faces) == 0:
            print("Face Not Found!")
            
        # iterate through detected faces
        for face in faces:
            x, y, w, h = face['box']
            confidence = face['confidence']
            print(confidence)
            
            # check if the face is frontal enough (you may need to adjust this threshold)
            if confidence > best_confidence:
                best_confidence = confidence
                best_face = (x, y, w, h)

        # if a frontal face is found, save it to a file
        if best_face:
            x, y, w, h = best_face
            extracted_face = image[y:y+h, x:x+w]

            # save the extracted face to a file in the output folder
            output_path = output_folder + "/" + file + "/best_face_" + image_name
            if not os.path.exists(output_folder + "/" + file):
                os.makedirs(output_folder + "/" + file)
            cv2.imwrite(output_path, extracted_face)
            print("Best face saved to:", output_path)

    print("Most frontal face in", image_name," its confidence: ", str(best_confidence))
