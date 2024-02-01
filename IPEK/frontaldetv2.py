import os
import cv2

# Function to detect faces using DNN Face Detector
def detect_faces_dnn(image_path):
    # Load the DNN Face Detector model
    face_detector = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

    # Read the input image
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    # Preprocess the image by resizing it and converting it to a blob
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Feed the blob as input to the DNN Face Detector model
    face_detector.setInput(blob)
    detections = face_detector.forward()

    # Loop over the detections and draw a rectangle around each face
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > 0.5:
            # Get the bounding box for the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw a rectangle around the face
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)

    # Show the output image
    cv2.imshow("Output", image)
    cv2.waitKey(0)

# Function to detect faces using Haar Cascade model
def detect_faces_haar(image_path):
    # Load the Haar Cascade model
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Read the input image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Loop over the detections and draw a rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Show the output image
    cv2.imshow("Output", image)
    cv2.waitKey(0)

# Main function to iterate through images in a directory and detect faces
def detect_faces_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):  # Assuming images are JPG or PNG format
                image_path = os.path.join(root, file)
                print("Processing:", image_path)

                # Uncomment one of the following lines based on the method you want to use
                # detect_faces_dnn(image_path)
                # detect_faces_haar(image_path)

# Provide the path to the folder containing images
folder_path = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\lfw-deepfunneled"
detect_faces_in_folder(folder_path)
