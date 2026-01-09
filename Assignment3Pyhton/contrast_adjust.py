import cv2
import numpy as np

def adjust_contrast(image, contrast_value):
    """
    contrast_value: integer from -100 to +100
    """
    alpha = 1.0 + (contrast_value / 100.0)
    beta = 0

    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted
