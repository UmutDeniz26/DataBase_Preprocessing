import cv2
import numpy as np

def show_image(image: np.ndarray, window_name: str = "Image", wait_time: int = 0) -> None:
    """
        Shows the image in a window.

        Args:
            image (np.ndarray): Image to be shown
            window_name (str): Name of the window
            wait_time (int): Time to wait for the next operation

        Returns:
            None
    """
    if image is None:
        print("Image was not found.")
        return
    cv2.imshow(window_name, image)
    cv2.waitKey(wait_time)
    cv2.destroyAllWindows()