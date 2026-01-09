import cv2
import numpy as np

def apply_blur(image, kernel_size=5):
    """Apply a Gaussian blur to the entire image"""
    
    if kernel_size % 2 == 0:
        kernel_size += 1 
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred

def apply_blur_with_roi(image, roi_coords, kernel_size=5):
    """Apply Gaussian blur to a specific ROI (Region of Interest) in the image"""

    if kernel_size % 2 == 0:
        kernel_size += 1
    x1, y1, x2, y2 = roi_coords
    height, width = image.shape[:2]
    
    # ROI is within bounds
    x1, x2 = max(0, min(x1, x2)), min(width, max(x1, x2))
    y1, y2 = max(0, min(y1, y2)), min(height, max(y1, y2))
    
    if x1 >= x2 or y1 >= y2:
        return image  # Invalid ROI
    
    # Create a copy of the image
    result = image.copy()
    
    # Extract the ROI
    roi = image[y1:y2, x1:x2]
    
    # Blur the ROI
    blurred_roi = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
    
    # Place the blurred ROI back
    result[y1:y2, x1:x2] = blurred_roi
    return result