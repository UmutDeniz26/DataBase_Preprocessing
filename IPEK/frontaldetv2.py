import os
import cv2

# Function to detect faces using Haar Cascade model and save frontal faces to a new directory
def detect_and_save_frontal_faces(folder_path, output_folder):
    # Load the Haar Cascade model
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through images in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):  # Assuming images are JPG or PNG format
                image_path = os.path.join(root, file)
                print("Processing:", image_path)

                # Read the input image
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces in the image
                faces = face_detector.detectMultiScale(gray, 1.3, 5)

                # Loop over the detections
                for (x, y, w, h) in faces:
                    # Check if the detected face is frontal
                    if w > 0.7 * h:
                        # Save the frontal face to the output directory
                        face_image = image[y:y+h, x:x+w]
                        output_path = os.path.join(output_folder, file)
                        cv2.imwrite(output_path, face_image)
                        print("Frontal face saved:", output_path)


# Provide the path to the folder containing images
folder_path = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\lfw-deepfunneled"

output_folder = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\frontal"

detect_and_save_frontal_faces(folder_path, output_folder)

