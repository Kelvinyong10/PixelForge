import cv2
import numpy as np

def adjust_brightness(image, brightness_value):
    """Adjust the brightness of the entire image"""
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, brightness_value)
    v = np.clip(v, 0, 255)
    hsv_adjusted = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2RGB)

def adjust_brightness_with_roi(image, roi_coords, brightness_value):
    """Adjust brightness only within the specified ROI"""
    x1, y1, x2, y2 = roi_coords
    result = image.copy()
    
    roi = image[y1:y2, x1:x2]
    
    processed_roi = adjust_brightness(roi, brightness_value)
    
    result[y1:y2, x1:x2] = processed_roi
    return result