import cv2
import numpy as np

def adjust_contrast(image, contrast_value):
    """Adjust contrast for the entire image"""
    alpha = 1.0 + (contrast_value / 100.0)
    return cv2.convertScaleAbs(image, alpha=alpha, beta=0)

def adjust_contrast_with_roi(image, roi_coords, contrast_value):
    """Adjust contrast only within the specified ROI"""
    x1, y1, x2, y2 = roi_coords
    result = image.copy()
    
    roi = image[y1:y2, x1:x2]
    processed_roi = adjust_contrast(roi, contrast_value)
    
    result[y1:y2, x1:x2] = processed_roi
    return result