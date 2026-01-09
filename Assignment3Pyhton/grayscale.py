import cv2

def apply_grayscale(image):
    """Convert RGB image to a visually grayscale 3-channel image"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

def apply_grayscale_with_roi(image, roi_coords):
    """Convert only the ROI area to grayscale"""
    x1, y1, x2, y2 = roi_coords
    result = image.copy()
    
    roi = image[y1:y2, x1:x2]
    processed_roi = apply_grayscale(roi)
    
    result[y1:y2, x1:x2] = processed_roi
    return result