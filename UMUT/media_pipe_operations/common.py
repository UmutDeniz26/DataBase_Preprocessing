import numpy as np

def calculate_angle_between_2_points(p1, p2):
    if isinstance(p1, tuple):
        x1, y1 = p1
        x2, y2 = p2
    else:
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
    return np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi


def calculate_abs_average(arr):
    sum_arr = 0
    for elem in arr:
        sum_arr += np.abs(elem)
    return sum_arr / len(arr)
