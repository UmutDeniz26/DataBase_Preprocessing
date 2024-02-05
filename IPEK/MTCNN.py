from mtcnn import MTCNN
import cv2

# initialize the MTCNN detector
detector = MTCNN()

# load the input image
image = cv2.imread(r"./IPEK/LFW/Abdoulaye_Wade/Abdoulaye_Wade_0002.jpg")

# convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces using MTCNN
faces = detector.detect_faces(image)

# if faces are detected, extract and display them
if faces:
    for face in faces:
        x, y, w, h = face['box']
        extracted_face = image[y:y+h, x:x+w]

        # display the extracted face
        cv2.imshow('Extracted Face', extracted_face)
        cv2.waitKey(0)  # wait for any key press
        cv2.destroyAllWindows()  # close the window after any key press

# if no faces are detected, print a message
else:
    print("No faces detected in the image.")
