import cv2

def detect_best_frontal_face(image_path,resp=False,onlyLandMarksFlag=False):
     import math
     from retinaface import RetinaFace
     if resp == False:
          resp = RetinaFace.detect_faces(image_path)
     if 'face_1' not in resp:
        return False
     else:   
          landmarks = resp['face_1']['landmarks']
          facial_area = resp["face_1"]["facial_area"]
          nose_point = landmarks['nose']
          left_eye_point = landmarks['left_eye']
          right_eye_point = landmarks['right_eye']
          mouth_left_point = landmarks.get('mouth_left')
          mouth_right_point = landmarks.get('mouth_right')

          distance_nose_left_eye = math.sqrt((left_eye_point[0] - nose_point[0])**2 + (left_eye_point[1] - nose_point[1])**2)
          distance_nose_right_eye = math.sqrt((right_eye_point[0] - nose_point[0])**2 + (right_eye_point[1] - nose_point[1])**2)
          difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)

          if onlyLandMarksFlag == False:
               result_dict = {
                         "distance_nose_left_eye": distance_nose_left_eye,
                         "distance_nose_right_eye": distance_nose_right_eye,
                         "difference_between_le_re": difference_between_le_re,
                         'left_eye': left_eye_point,
                         'right_eye':right_eye_point,
                         'nose': nose_point,
                         'mouth_left': mouth_left_point,
                         'mouth_right':mouth_right_point,
                         "facial_area":facial_area
                    }
          else:
               result_dict = {
                         'left_eye': left_eye_point,
                         'right_eye':right_eye_point,
                         'nose': nose_point,
                         'mouth_left': mouth_left_point,
                         'mouth_right':mouth_right_point,
                         "facial_area":facial_area
                    }
          return result_dict
