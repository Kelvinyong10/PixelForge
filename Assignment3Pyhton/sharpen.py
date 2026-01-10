import cv2
import numpy as np

def apply_sharpen(image, intensity=1.0):
    
    w = (intensity / 100) * 2
    center = 1 + 8 * w
    kernel = np.array([[-w, -w, -w],
                       [-w, center, -w],
                       [-w, -w, -w]], dtype=np.float32)
    return np.clip(cv2.filter2D(image, -1, kernel), 0, 255).astype(np.uint8)


def apply_sharpen_with_roi(image, roi, strength):
    x1, y1, x2, y2 = roi
    roi_img = image[y1:y2, x1:x2].copy()
    roi_img = apply_sharpen(roi_img, strength)
    image[y1:y2, x1:x2] = roi_img
    return image