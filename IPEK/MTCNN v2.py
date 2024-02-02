from mtcnn import MTCNN
import cv2
import os

# initialize the MTCNN detector
detector = MTCNN()

# define the folder path containing images
folder_path = r'./IPEK/lfw-deepfunneled'

files = os.listdir(folder_path)

# loop through the images in the folder
for file in files:
        
    inner_folder = folder_path+ "/" + file 
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

        # if a frontal face is found, display it
        if best_face:
            # print the filename associated with the most frontal face
            
            x, y, w, h = best_face
         
            extracted_face = image[y:y+h, x:x+w]

            # display the extracted face
            #cv2.imshow(filename, extracted_face)
            #cv2.waitKey(0)  # wait for any key press
            #cv2.destroyAllWindows()  # close the window after any key press
    
    print("Most frontal face in", image_name," its confidence: ", str(best_confidence))
    best_confidence = 0