import face_recognition
import cv2
import os

def find_best_frontal_face(image):
    """
    Find the face with the best frontal angle in the image.
    """
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return None

    best_face = None
    best_face_area = 0

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_area = (bottom - top) * (right - left)
        if face_area > best_face_area:
            best_face = face_location
            best_face_area = face_area

    return best_face

# Load the reference image of the person
reference_image_path = r"C:\Users\ipekb\Desktop\staj lwf\DataBase_Preprocessing\IPEK\lfw-deepfunneled\Aaron_Peirsol"
reference_image = face_recognition.load_image_file(reference_image_path)
reference_encoding = face_recognition.face_encodings(reference_image)[0]

# Directory containing the images you want to search
image_dir = "directory_containing_images"

# Iterate through each image in the directory
for filename in os.listdir(image_dir):
    image_path = os.path.join(image_dir, filename)
    image = face_recognition.load_image_file(image_path)

    # Find the best frontal face in the image
    face_location = find_best_frontal_face(image)

    if face_location is not None:
        # Encode the best face found
        face_encoding = face_recognition.face_encodings(image, [face_location])[0]

        # Compare the face encoding with the reference encoding
        match = face_recognition.compare_faces([reference_encoding], face_encoding)

        if match[0]:  # If the encoding matches the reference encoding
            print(f"Found a match for {filename}")

            # Display the image with the detected face
            cv2.rectangle(image, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 255, 0), 2)
            cv2.imshow("Matched Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
