import cv2
import numpy as np

def adjust_brightness(image, brightness_value):
    """Adjust the brightness of the entire image"""

    # Convert to HSV for better brightness control
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    # 
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, brightness_value)  # Add/subtract brightness
    v = np.clip(v, 0, 255) 
    
    # Merge back and convert to RGB
    hsv_adjusted = cv2.merge([h, s, v])
    adjusted_image = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2RGB)
    
    return adjusted_image