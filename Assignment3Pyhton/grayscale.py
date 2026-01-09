import cv2

def apply_grayscale(image):
    """
    Convert the input RGB image to Grayscale.
    Returns a 3-channel RGB image (visually grayscale) to maintain compatibility.
    """
    # Convert RGB to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Convert back to RGB so it remains a 3-channel image for the editor
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    
    return gray_rgb