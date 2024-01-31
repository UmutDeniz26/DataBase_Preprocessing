
def detect_best_frontal_face(image_path):
   import math
   from retinaface import RetinaFace

   resp = RetinaFace.detect_faces(image_path)
   landmarks = resp['face_1']['landmarks']
   nose_point = landmarks['nose']
   left_eye_point = landmarks['left_eye']
   right_eye_point = landmarks['right_eye']

   distance_nose_left_eye = math.sqrt((left_eye_point[0] - nose_point[0])**2 + (left_eye_point[1] - nose_point[1])**2)
   distance_nose_right_eye = math.sqrt((right_eye_point[0] - nose_point[0])**2 + (right_eye_point[1] - nose_point[1])**2)
   difference_between_le_re = abs(distance_nose_left_eye-distance_nose_right_eye)

   result_dict = {
        "distance_nose_left_eye": distance_nose_left_eye,
        "distance_nose_right_eye": distance_nose_right_eye,
        "difference_between_le_re": difference_between_le_re
    }
   return result_dict


