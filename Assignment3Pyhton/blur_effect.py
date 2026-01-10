import cv2
import numpy as np

def apply_blur(image, intensity=50):
    
    kernel_size = 1 + int((intensity / 100) * 14)
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_blur_with_roi(image, roi_coords, intensity=50):
    
    
    kernel_size = 1 + int((intensity / 100) * 14)
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
    result[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
    return result