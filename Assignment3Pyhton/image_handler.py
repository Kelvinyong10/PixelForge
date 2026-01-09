# image_handler.py
import tkinter as tk
from tkinter import filedialog
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
    """Display RGB image on the specified canvas, resized to fit while maintaining aspect ratio."""
    if canvas is None:
        canvas = editor.canvas_select  # Default to select canvas
    if status_label is None:
        status_label = editor.status_label_select  # Default to select status
    
    canvas_width = 600
    canvas_height = 400
    
    height, width = rgb_image.shape[:2]
    
    # Calculate scaling factor to fit the image into the canvas
    scale_x = canvas_width / width
    scale_y = canvas_height / height
    scale = min(scale_x, scale_y)  # Use the smaller scale to fit without cropping
    
    # Resize the image
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = cv2.resize(rgb_image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # Create PhotoImage from resized image
    editor.photo = tk.PhotoImage(width=new_width, height=new_height)
    
    # Add pixel data row by row
    for y in range(new_height):
        row = []
        for x in range(new_width):
            r, g, b = resized_image[y, x]
            row.append(f"#{r:02x}{g:02x}{b:02x}")
        editor.photo.put("{" + " ".join(row) + "}", to=(0, y))
    
    # Clear and display on canvas (centered)
    canvas.delete("all")
    x_offset = (canvas_width - new_width) // 2
    y_offset = (canvas_height - new_height) // 2
    canvas.create_image(x_offset + new_width // 2, y_offset + new_height // 2, anchor="center", image=editor.photo)

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