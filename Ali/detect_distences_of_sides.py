import cv2

def detect_best_frontal_face(image_path):
     import math
     from retinaface import RetinaFace
     
     resp = RetinaFace.detect_faces(image_path)
     if 'face_1' not in resp:
        return False
     else:   
          landmarks = resp['face_1']['landmarks']
          facial_area = resp["face_1"]["facial_area"]
          score = resp['face_1']['score']
          nose_point = landmarks['nose']
          left_eye_point = landmarks['left_eye']
          right_eye_point = landmarks['right_eye']
          mouth_left_point = landmarks.get('mouth_left')
          mouth_right_point = landmarks.get('mouth_right')

          distance_nose_left_eye = math.sqrt((left_eye_point[0] - nose_point[0])**2 + (left_eye_point[1] - nose_point[1])**2)
          distance_nose_right_eye = math.sqrt((right_eye_point[0] - nose_point[0])**2 + (right_eye_point[1] - nose_point[1])**2)
          difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)

          # high treshold, be sure that the face is detected
          face_cascade = cv2.CascadeClassifier('./UMUT/haarcascade_frontalface_default.xml')
          img = cv2.imread(image_path)
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

          if len(faces) != 0:
               haarFaceDetected = 1
          else:
               haarFaceDetected = 0

          # Filter out faces that are not frontal
          for (x, y, w, h) in faces:
               # Check the aspect ratio to identify frontal faces
               aspect_ratio = w / h
               if 0.7 < aspect_ratio < 1.3:
                    haarFaceDetected = 1
               else:
                    haarFaceDetected = 0


          result_dict = {
                    "distance_nose_left_eye": distance_nose_left_eye,
                    "distance_nose_right_eye": distance_nose_right_eye,
                    "difference_between_le_re": difference_between_le_re,
                    "haarFaceDetected": haarFaceDetected,
                    "score": score,
                    'left_eye': left_eye_point,
                    'right_eye':right_eye_point,
                    'nose': nose_point,
                    'mouth_left': mouth_left_point,
                    'mouth_right':mouth_right_point,
                    "facial_area":facial_area
               }
          return result_dict
