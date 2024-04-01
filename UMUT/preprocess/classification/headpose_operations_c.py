from sklearn.cluster import KMeans
import time

def get_most_frontal_face(image_object_list: list) -> None:
    """
        Get the most frontal face from the list of images.

        Args:
            image_object_list (list): List of the images
        Returns:
            None
    """
    
    classes = {"low-angle": [], "medium-angle": [], "high-angle": []}
    sorted_image_object_list = sorted(
        image_object_list, key=lambda x: x.nose_angle_arr["normalized_abs_angle"] if hasattr(x, "nose_angle_arr") else 0
        )

    for obj in image_object_list:
        if not hasattr(obj, "nose_angle_arr"):
            continue

        angle = obj.nose_angle_arr["normalized_abs_angle"]
        if angle < 2:
            classes["low-angle"].append(obj)
        elif angle < 5:
            classes["medium-angle"].append(obj)
        else:
            classes["high-angle"].append(obj)

    valid_data = False if len(classes["low-angle"]) == 0 or len(classes["medium-angle"]) + len(classes["high-angle"]) == 0 else True
    frontal_img = sorted_image_object_list[0]

    if valid_data==False:
        for keys,value in classes.items():
            print(keys," : ",len(value))
            pass
        #time.sleep(3)


    return {"frontal_img": frontal_img, "valid_data": valid_data}
