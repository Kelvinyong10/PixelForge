# image_handler.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

def open_image(editor, status_label):
    """Open and load an image, returning the original BGR and current RGB images."""
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        # Read with OpenCV (BGR format)
        original_bgr = cv2.imread(file_path)
        
        if original_bgr is not None:
            # Convert to RGB for display
            current_image = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB)
            
            # Update status (using the passed status_label)
            filename = os.path.basename(file_path)
            status_label.config(text=f"Loaded: {filename}", fg="green")
            
            return original_bgr, current_image
    return None

def display_image(editor, rgb_image, canvas=None, status_label=None):
    if canvas is None:
        canvas = editor.canvas_select

    # Convert OpenCV RGB array to PIL Image
    pil_image = Image.fromarray(rgb_image)

    # Resize to fit canvas
    canvas_width = 600
    canvas_height = 400
    pil_image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

    # Convert to ImageTk
    editor.photo = ImageTk.PhotoImage(pil_image)

    # Clear and display
    canvas.delete("all")
    canvas.create_image(canvas_width//2, canvas_height//2, image=editor.photo, anchor="center")

def save_image(rgb_image, file_path):
    """Save the RGB image to the specified file path."""
    if rgb_image is None:
        return False
    
    try:
        # Convert RGB back to BGR for saving with OpenCV (OpenCV uses BGR by default)
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(file_path, bgr_image)
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False