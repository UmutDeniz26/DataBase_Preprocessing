
def get_avg_difference(difference_vector: list) -> float:
    """
        Get the average difference from the difference vector.

        Args:
            difference_vector (list): Difference vector

        Returns:
            float: Average difference
    """
    total = 0
    for elem in difference_vector:
        total += elem["Result"]
    return total / len(difference_vector)