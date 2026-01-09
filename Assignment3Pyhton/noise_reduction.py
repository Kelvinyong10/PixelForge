import cv2
import numpy as np

def apply_median_blur(image, kernel_size=5):
    """Apply median filter to the entire image for noise reduction."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    if kernel_size < 1:
        kernel_size = 1
        
    return cv2.medianBlur(image, kernel_size)

def apply_median_blur_with_roi(image, roi_coords, kernel_size=5):
    """Apply median filter to a specific ROI."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    x1, y1, x2, y2 = roi_coords
    height, width = image.shape[:2]
    
    x1, x2 = max(0, min(x1, x2)), min(width, max(x1, x2))
    y1, y2 = max(0, min(y1, y2)), min(height, max(y1, y2))
    
    if x1 >= x2 or y1 >= y2:
        return image
    
    result = image.copy()
    roi = image[y1:y2, x1:x2]
    
    blurred_roi = cv2.medianBlur(roi, kernel_size)
    
    result[y1:y2, x1:x2] = blurred_roi
    return result