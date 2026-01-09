import cv2
import numpy as np

def apply_sharpen(image, strength):
    kernel = np.array([
        [0, -1, 0],
        [-1, 5 + strength, -1],
        [0, -1, 0]
    ])
    return cv2.filter2D(image, -1, kernel)


def apply_sharpen_with_roi(image, roi, strength):
    x1, y1, x2, y2 = roi
    roi_img = image[y1:y2, x1:x2].copy()
    roi_img = apply_sharpen(roi_img, strength)
    image[y1:y2, x1:x2] = roi_img
    return image