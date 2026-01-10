import tkinter as tk

from image_handler import open_image, display_image, save_image
import os
from blur_effect import apply_blur, apply_blur_with_roi  # Import blur functions
from brightness_adjust import adjust_brightness, adjust_brightness_with_roi # Import brightness functions
from contrast_adjust import adjust_contrast, adjust_contrast_with_roi # Import contrast functions
from sharpen import apply_sharpen, apply_sharpen_with_roi  # Import sharpen functions
from noise_reduction import apply_median_blur, apply_median_blur_with_roi #Import noise reduction functions
from grayscale import apply_grayscale, apply_grayscale_with_roi #Import greyscale functions
import PIL.ImageTk as ImageTk
import numpy as np

class PixelForgeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelForge - Image Editor")
        current_dir = os.path.dirname(__file__)
        icon_path = os.path.join(current_dir, "logo.jpg")

        try:
            self.icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, self.icon)
        except Exception as e:
            print(f"Icon not found at {icon_path}. Error: {e}")
        
        self.root.geometry("800x600")
        self.root.configure(bg="#1F1F1F")  # Gray background

        # Store the original image (managed in image_handler)
        self.original_bgr = None
        self.current_image = None
        self.temp_image = None  # Temporary image for preview

        # ROI selection variables
        self.roi_start = None 
        self.roi_rect = None 
        self.selection_mode = False 
        self.selected_roi = None
        self.copied_fragment = None

        # Blur variables
        self.blur_kernel = 5  # Default kernel size

        # Brightness variables
        self.brightness_value = 0  # Default brightness adjustment

        # Contrast variables
        self.contrast_value = 0  # Default contrast adjustment

        # Create frames for interfaces
        self.welcome_frame = tk.Frame(root, bg="#1F1F1F")
        self.select_frame = tk.Frame(root, bg="#1F1F1F")
        self.features_frame = tk.Frame(root, bg="#1F1F1F")

        # Initialize interfaces
        self.create_welcome_interface()
        self.create_select_image_interface()
        self.create_features_interface()

        self.show_welcome()

        # Photo reference for canvas (used in display_image)
        self.photo = None

    # -----------------------------
    # Welcome Interface
    # -----------------------------

    def create_welcome_interface(self):
        """Create a modernized welcome screen."""
        self.welcome_frame.pack(fill="both", expand=True)
        self.welcome_frame.configure(bg="#1F1F1F")

        # Main Title with a 'Forge' accent
        title_label = tk.Label(
            self.welcome_frame,
            text="PIXELFORGE",
            font=("Impact", 48),
            bg="#1F1F1F",
            fg="#FFA500" 
        )
        title_label.pack(pady=(120, 5))

        subtitle_label = tk.Label(
            self.welcome_frame,
            text="Forging Perfection, One Pixel at a Time",
            font=("Arial", 12, "italic"),
            bg="#1F1F1F",
            fg="#aaaaaa"
        )
        subtitle_label.pack(pady=(0, 40))

        button_frame = tk.Frame(self.welcome_frame, bg="#1F1F1F")
        button_frame.pack()

        start_btn = tk.Button(
            button_frame,
            text="Start Editing",
            command=self.show_select_image,
            bg="#404040",
            fg="white",
            font=("Arial", 14),
            width=15,
            height=2
        )
        start_btn.pack(side="left", padx=10)

        exit_btn = tk.Button(
            button_frame,
            text="Exit Program",
            command=self.root.quit,
            bg="#404040",
            fg="white",
            font=("Arial", 14),
            width=15,
            height=2
        )
        exit_btn.pack(side="left", padx=10)

        version_label = tk.Label(
            self.welcome_frame,
            text="v1.0.0 | © 2026 PixelForge",
            bg="#1F1F1F",
            fg="#444444",
            font=("Arial", 8)
        )
        version_label.pack(side="bottom", pady=20)

    # -----------------------------
    # Select Image Interface
    # -----------------------------
    def create_select_image_interface(self):
        """Create the select image screen."""
        left_frame = tk.Frame(self.select_frame, bg="#1F1F1F")
        left_frame.pack(side="left", fill="y", padx=20, pady=20)

        title_label = tk.Label(
            left_frame,
            text="Select Image",
            font=("Arial", 18, "bold"),
            bg="#1F1F1F",
            fg="white"
        )
        title_label.pack(anchor="w", pady=(0, 10))

        open_btn = tk.Button(
            left_frame,
            text="Open Image",
            command=self.handle_open_image,
            bg="#FFA500",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2
        )
        open_btn.pack(anchor="w", pady=(0, 10))

        next_btn = tk.Button(
            left_frame,
            text="Next",
            command=self.show_features,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        next_btn.pack(anchor="w", pady=(0, 20))

        back_btn = tk.Button(
            left_frame,
            text="Back",
            command=self.show_welcome,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        back_btn.pack(side="bottom", anchor="sw", pady=(20, 0))

        right_frame = tk.Frame(self.select_frame, bg="#1F1F1F")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.canvas_select = tk.Canvas(
            right_frame,
            width=600,
            height=400,
            bg="#959595", 
            highlightthickness=1,
            highlightbackground="#404040"
        )
        self.canvas_select.pack(pady=(0, 10))

        self.status_label_select = tk.Label(
            right_frame,
            text="No Image Loaded",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 12)
        )
        self.status_label_select.pack()

    # -----------------------------
    # Features Interface
    # -----------------------------
    def create_features_interface(self):
        """Create the features interface."""
        left_frame = tk.Frame(self.features_frame, bg="#1F1F1F")
        left_frame.pack(side="left", fill="y", padx=20, pady=20)

        title_label = tk.Label(
            left_frame,
            text="Features",
            font=("Arial", 18, "bold"),
            bg="#1F1F1F",
            fg="white"
        )
        title_label.pack(anchor="w", pady=(0, 10))

        # ROI selection button
        roi_btn = tk.Button(
            left_frame,
            text="Select ROI (Optional)",
            command=self.start_optional_roi_selection,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        )
        roi_btn.pack(anchor="w", pady=(0, 10))

        # Feature buttons
        tk.Button(
            left_frame,
            text="Apply Blur",
            command=self.apply_blur_feature,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(anchor="w", pady=(0, 10))

        tk.Button(
            left_frame,
            text="Adjust Brightness",
            command=self.apply_brightness_feature,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(anchor="w", pady=(0, 10))

        tk.Button(
            left_frame,
            text="Adjust Contrast",
            command=self.apply_contrast_feature,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(anchor="w", pady=(0, 10))

        tk.Button(
            left_frame,
            text="Sharpen",
            command=self.show_sharpen_controls,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(anchor="w", pady=(0, 10))

        tk.Button(
            left_frame,
            text="Noise Reduction",
            command=self.apply_noise_reduction_feature,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(anchor="w", pady=(0, 10))

        tk.Button(
            left_frame,
            text="Apply Grayscale",
            command=self.apply_grayscale_feature,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(anchor="w", pady=(0, 10))

        # Bottom Button 
        bottom_btn_frame = tk.Frame(left_frame, bg="#1F1F1F")
        bottom_btn_frame.pack(side="bottom", anchor="w", pady=(20, 0), fill="x")

        # 1. Back Button
        back_btn = tk.Button(
            bottom_btn_frame,
            text="Back",
            command=self.show_select_image,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        back_btn.pack(side="left", padx=(0, 10))

        # Right frame for canvas + sliders
        right_frame = tk.Frame(self.features_frame, bg="#1F1F1F")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.canvas_features = tk.Canvas(
            right_frame,
            width=600,
            height=400,
            bg="#959595",
            highlightthickness=1,
            highlightbackground="#404040"
        )
        self.canvas_features.pack(pady=(0, 10))

        action_btn_frame = tk.Frame(right_frame, bg="#1F1F1F")
        action_btn_frame.pack(side="bottom", fill="x", pady=(20, 0))

        # 1. Save Button
        save_btn = tk.Button(
            action_btn_frame,
            text="Save",
            command=self.handle_save_image,
            bg="#28a745",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        save_btn.pack(side="right", padx=(10, 0))

        # 2. Reset Button
        reset_btn = tk.Button(
            action_btn_frame,
            text="Reset",
            command=self.reset_to_original, 
            bg="#dc3545",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        reset_btn.pack(side="right")

        # -----------------------------
        # Control Frames (Blur, Brightness, Contrast, Sharpen)
        # -----------------------------
        
        # Blur Controls 
        self.blur_controls_frame = tk.Frame(right_frame, bg="#1F1F1F")
        
        blur_top_row = tk.Frame(self.blur_controls_frame, bg="#1F1F1F")
        blur_top_row.pack(side="top", pady=(0, 15))

        self.blur_slider_label = tk.Label(
            blur_top_row,
            text="Blur Intensity:",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 15)
        )
        self.blur_slider_label.pack(side="left", padx=(0, 15))

        self.blur_slider = tk.Scale(
            blur_top_row,
            from_=0,
            to=100,
            resolution=1,
            orient="horizontal",
            length=150,
            bg="#1F1F1F",
            fg="white",
            highlightbackground="#404040",
            command=self.update_blur_preview
        )
        self.blur_slider.set(33)
        self.blur_slider.pack(side="left", padx=(0, 10))

        blur_bottom_row = tk.Frame(self.blur_controls_frame, bg="#1F1F1F")
        blur_bottom_row.pack(side="top")

        self.apply_blur_btn = tk.Button(
            blur_bottom_row,
            text="Apply",
            command=self.confirm_blur,
            bg="#FFA500",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.apply_blur_btn.pack(side="left", padx=(0, 5))

        self.cancel_blur_btn = tk.Button(
            blur_bottom_row,
            text="Cancel",
            command=self.cancel_blur,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.cancel_blur_btn.pack(side="left")

        # Brightness Controls
        self.brightness_controls_frame = tk.Frame(right_frame, bg="#1F1F1F")
        
        bright_top_row = tk.Frame(self.brightness_controls_frame, bg="#1F1F1F")
        bright_top_row.pack(side="top", pady=(0, 15))

        self.brightness_slider_label = tk.Label(
            bright_top_row,
            text="Brightness:",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 15)
        )
        self.brightness_slider_label.pack(side="left", padx=(0, 15))

        self.brightness_slider = tk.Scale(
            bright_top_row,
            from_=-100,
            to=100,
            resolution=10,
            orient="horizontal",
            length=150,
            bg="#1F1F1F",
            fg="white",
            highlightbackground="#404040",
            command=self.update_brightness_preview
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(side="left", padx=(0, 10))

        bright_bottom_row = tk.Frame(self.brightness_controls_frame, bg="#1F1F1F")
        bright_bottom_row.pack(side="top")

        self.apply_brightness_btn = tk.Button(
            bright_bottom_row,
            text="Apply",
            command=self.confirm_brightness,
            bg="#FFA500",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.apply_brightness_btn.pack(side="left", padx=(0, 5))

        self.cancel_brightness_btn = tk.Button(
            bright_bottom_row,
            text="Cancel",
            command=self.cancel_brightness,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.cancel_brightness_btn.pack(side="left")

        # Contrast Controls 
        self.contrast_controls_frame = tk.Frame(right_frame, bg="#1F1F1F")
        
        contrast_top_row = tk.Frame(self.contrast_controls_frame, bg="#1F1F1F")
        contrast_top_row.pack(side="top", pady=(0, 15))

        self.contrast_slider_label = tk.Label(
            contrast_top_row,
            text="Contrast:",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 15)
        )
        self.contrast_slider_label.pack(side="left", padx=(0, 15))

        self.contrast_slider = tk.Scale(
            contrast_top_row,
            from_=-100,
            to=100,
            resolution=10,
            orient="horizontal",
            length=150,
            bg="#1F1F1F",
            fg="white",
            highlightbackground="#404040",
            command=self.update_contrast_preview
        )
        self.contrast_slider.set(0)
        self.contrast_slider.pack(side="left", padx=(0, 10))

        contrast_bottom_row = tk.Frame(self.contrast_controls_frame, bg="#1F1F1F")
        contrast_bottom_row.pack(side="top")

        self.apply_contrast_btn = tk.Button(
            contrast_bottom_row,
            text="Apply",
            command=self.confirm_contrast,
            bg="#FFA500",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.apply_contrast_btn.pack(side="left", padx=(0, 5))

        self.cancel_contrast_btn = tk.Button(
            contrast_bottom_row,
            text="Cancel",
            command=self.cancel_contrast,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.cancel_contrast_btn.pack(side="left")

        # Sharpen controls 
        self.sharpen_controls_frame = tk.Frame(right_frame, bg="#1F1F1F")

        sharpen_top_row = tk.Frame(self.sharpen_controls_frame, bg="#1F1F1F")
        sharpen_top_row.pack(side="top", pady=(0, 15))

        self.sharpen_slider_label = tk.Label(
            sharpen_top_row,
            text="Sharpen Strength:",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 15)
        )
        self.sharpen_slider_label.pack(side="left", padx=(0, 15))

        self.sharpen_slider = tk.Scale(
            sharpen_top_row,
            from_=0,
            to=100,
            orient="horizontal",
            length=150,
            bg="#1F1F1F",
            fg="white",
            highlightbackground="#404040",
            command=self.update_sharpen_preview
        )
        self.sharpen_slider.set(0)
        self.sharpen_slider.pack(side="left", padx=(0, 10))

        sharpen_bottom_row = tk.Frame(self.sharpen_controls_frame, bg="#1F1F1F")
        sharpen_bottom_row.pack(side="top")

        self.apply_sharpen_btn = tk.Button(
            sharpen_bottom_row,
            text="Apply ",
            command=self.confirm_sharpen,
            bg="#FFA500",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.apply_sharpen_btn.pack(side="left", padx=(0, 5))

        self.cancel_sharpen_btn = tk.Button(
            sharpen_bottom_row,
            text="Cancel",
            command=self.cancel_sharpen,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.cancel_sharpen_btn.pack(side="left")

        # Noise Reduction Controls 
        self.noise_controls_frame = tk.Frame(right_frame, bg="#1F1F1F")

        noise_top_row = tk.Frame(self.noise_controls_frame, bg="#1F1F1F")
        noise_top_row.pack(side="top", pady=(0, 15))

        tk.Label(
            noise_top_row,
            text="Denoise Strength:",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 15)
        ).pack(side="left", padx=(0, 15))

        self.noise_slider = tk.Scale(
            noise_top_row,
            from_=0,
            to=100,
            resolution=2,
            orient="horizontal",
            length=150,
            bg="#1F1F1F",
            fg="white",
            highlightbackground="#404040",
            command=self.update_noise_reduction_preview
        )
        self.noise_slider.set(20)
        self.noise_slider.pack(side="left", padx=(0, 10))

        noise_bottom_row = tk.Frame(self.noise_controls_frame, bg="#1F1F1F")
        noise_bottom_row.pack(side="top")

        self.apply_noise_btn = tk.Button(
            noise_bottom_row,
            text="Apply",
            command=self.confirm_noise_reduction,
            bg="#FFA500",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.apply_noise_btn.pack(side="left", padx=(0, 5))

        self.cancel_noise_btn = tk.Button(
            noise_bottom_row,
            text="Cancel",
            command=self.cancel_noise_reduction,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.cancel_noise_btn.pack(side="left")

        # Grayscale Controls 
        self.grayscale_controls_frame = tk.Frame(right_frame, bg="#1F1F1F")

        gray_top_row = tk.Frame(self.grayscale_controls_frame, bg="#1F1F1F")
        gray_top_row.pack(side="top", pady=(0, 15))

        tk.Label(
            gray_top_row,
            text="Convert to Grayscale",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 15)
        ).pack(side="left", padx=(0, 15))

        gray_bottom_row = tk.Frame(self.grayscale_controls_frame, bg="#1F1F1F")
        gray_bottom_row.pack(side="top")

        self.apply_gray_btn = tk.Button(
            gray_bottom_row,
            text="Apply",
            command=self.confirm_grayscale,
            bg="#FFA500",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.apply_gray_btn.pack(side="left", padx=(0, 5))

        self.cancel_gray_btn = tk.Button(
            gray_bottom_row,
            text="Cancel",
            command=self.cancel_grayscale,
            bg="#404040",
            fg="white",
            font=("Arial", 12),
            width=15,
            height=2
        )
        self.cancel_gray_btn.pack(side="left")

        # Status label
        self.status_label_features = tk.Label(
            right_frame,
            text="No Image Loaded",
            bg="#1F1F1F",
            fg="white",
            font=("Arial", 12)
        )
        self.status_label_features.pack(pady=(10, 0))

    # --------------------------------------
    # Unified show/hide feature controls
    # --------------------------------------
    def show_feature_controls(self, feature):
        """Show the specified feature controls and hide all others."""
        self.hide_all_feature_controls()
        if feature == "blur":
            self.blur_controls_frame.pack(pady=(0, 10))
        elif feature == "brightness":
            self.brightness_controls_frame.pack(pady=(0, 10))
        elif feature == "contrast":
            self.contrast_controls_frame.pack(pady=(0, 10))
        elif feature == "sharpen":
            self.sharpen_controls_frame.pack(pady=(0, 10))
        elif feature == "grayscale": 
            self.grayscale_controls_frame.pack(pady=(0, 10))
        elif feature == "noise":
            self.noise_controls_frame.pack(pady=(0, 10))

    def hide_all_feature_controls(self):
        """Hide all feature control frames."""
        self.blur_controls_frame.pack_forget()
        self.brightness_controls_frame.pack_forget()
        self.contrast_controls_frame.pack_forget()
        self.sharpen_controls_frame.pack_forget()
        self.grayscale_controls_frame.pack_forget()
        self.noise_controls_frame.pack_forget()

    # --------------------------------------
    # Screen navigation
    # --------------------------------------
    def show_welcome(self):
        self.select_frame.pack_forget()
        self.features_frame.pack_forget()
        self.welcome_frame.pack(fill="both", expand=True)
        self.original_bgr = None
        self.current_image = None
        self.temp_image = None
        self.canvas_select.delete("all")
        self.canvas_features.delete("all")
        self.status_label_select.config(text="No Image Loaded")
        self.status_label_features.config(text="No Image Loaded")
        self.reset_roi_selection()
        self.hide_all_feature_controls()

    def show_select_image(self):
        self.welcome_frame.pack_forget()
        self.features_frame.pack_forget()
        self.select_frame.pack(fill="both", expand=True)
        if self.current_image is not None:
            display_image(self, self.current_image, canvas=self.canvas_select, status_label=self.status_label_select)
        self.reset_roi_selection()
        self.hide_all_feature_controls()

    def show_features(self):
        self.welcome_frame.pack_forget()
        self.select_frame.pack_forget()
        self.features_frame.pack(fill="both", expand=True)
        if self.current_image is not None:
            display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.reset_roi_selection()
        self.hide_all_feature_controls()

    # --------------------------------------
    # Image handling
    # --------------------------------------
    def handle_open_image(self):
        result = open_image(self, self.status_label_select)
        if result:
            self.original_bgr, self.current_image = result
            self.original_rgb_copy = self.current_image.copy()
            display_image(self, self.current_image, canvas=self.canvas_select, status_label=self.status_label_select)

    def canvas_to_image_coords(self, x1, y1, x2, y2, canvas):
        if self.current_image is None:
            return None
        canvas_width, canvas_height = 600, 400
        img_height, img_width = self.current_image.shape[:2]
        scale = min(canvas_width / img_width, canvas_height / img_height)
        scaled_width = int(img_width * scale)
        scaled_height = int(img_height * scale)
        x_offset = (canvas_width - scaled_width) // 2
        y_offset = (canvas_height - scaled_height) // 2
        scaled_x1 = max(0, x1 - x_offset)
        scaled_y1 = max(0, y1 - y_offset)
        scaled_x2 = min(scaled_width, x2 - x_offset)
        scaled_y2 = min(scaled_height, y2 - y_offset)
        img_x1 = int(scaled_x1 / scale)
        img_y1 = int(scaled_y1 / scale)
        img_x2 = int(scaled_x2 / scale)
        img_y2 = int(scaled_y2 / scale)
        return (img_x1, img_y1, img_x2, img_y2)

    # --------------------------------------
    # ROI selection
    # --------------------------------------
    def start_optional_roi_selection(self):
        if self.current_image is None:
            self.status_label_features.config(text="No image loaded", fg="red")
            return

        self.selection_mode = True
        self.status_label_features.config(text="Drag Left-Click to Copy | Right-Click to Paste", fg="orange")
        self.hide_all_feature_controls()

        self.canvas_features.bind("<ButtonPress-1>", self.start_roi_selection)
        self.canvas_features.bind("<B1-Motion>", self.update_roi_selection)
        self.canvas_features.bind("<ButtonRelease-1>", self.finish_roi_selection)
        
        self.canvas_features.bind("<Button-3>", self.handle_right_click_paste) # Windows/Linux

    def start_roi_selection(self, event):
        if not self.selection_mode:
            return
        self.roi_start = (event.x, event.y)
        if self.roi_rect:
            self.canvas_features.delete(self.roi_rect)
        self.roi_rect = self.canvas_features.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

    def update_roi_selection(self, event):
        if not self.selection_mode or not self.roi_start:
            return
        self.canvas_features.coords(self.roi_rect, self.roi_start[0], self.roi_start[1], event.x, event.y)

    def finish_roi_selection(self, event):
        if not self.selection_mode or not self.roi_start:
            return

        x1, y1, x2, y2 = self.canvas_features.coords(self.roi_rect)
        self.selected_roi = self.canvas_to_image_coords(x1, y1, x2, y2, self.canvas_features)
        
        if self.selected_roi:
            ix1, iy1, ix2, iy2 = self.selected_roi
            self.copied_fragment = self.current_image[iy1:iy2, ix1:ix2].copy()
            self.status_label_features.config(text="Fragment Copied! Right-click to paste it.", fg="green")

        self.roi_start = None

    def reset_roi_selection(self):
        self.selection_mode = False
        self.roi_start = None
        self.selected_roi = None
        self.temp_image = None
        if self.roi_rect:
            self.canvas_features.delete(self.roi_rect)
            self.roi_rect = None
        self.canvas_features.unbind("<ButtonPress-1>")
        self.canvas_features.unbind("<B1-Motion>")
        self.canvas_features.unbind("<ButtonRelease-1>")

    # --------------------------------------
    # Paste Feature
    # --------------------------------------

    def handle_right_click_paste(self, event):
        """Logic to paste the copied fragment at the mouse cursor position."""
        if self.copied_fragment is None:
            self.status_label_features.config(text="Nothing copied yet! Drag left-click first.", fg="red")
            return

        img_coords = self.canvas_to_image_coords(event.x, event.y, event.x, event.y, self.canvas_features)
        if not img_coords: return
        
        start_x, start_y = img_coords[0], img_coords[1]
        
        frag_h, frag_w = self.copied_fragment.shape[:2]
        img_h, img_w = self.current_image.shape[:2]

        end_y = min(start_y + frag_h, img_h)
        end_x = min(start_x + frag_w, img_w)
        
        visible_h = end_y - start_y
        visible_w = end_x - start_x

        if visible_h > 0 and visible_w > 0:
            self.temp_image = self.current_image.copy()
            
            self.current_image[start_y:end_y, start_x:end_x] = self.copied_fragment[0:visible_h, 0:visible_w]
            
            display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
            self.status_label_features.config(text="Fragment Pasted!", fg="green")

    def stop_roi_mode(self):
        """Call this to exit selection mode and clean up binds."""
        self.selection_mode = False
        self.canvas_features.unbind("<ButtonPress-1>")
        self.canvas_features.unbind("<B1-Motion>")
        self.canvas_features.unbind("<ButtonRelease-1>")
        self.canvas_features.unbind("<Button-3>")
        self.canvas_features.unbind("<Button-2>")
        if self.roi_rect:
            self.canvas_features.delete(self.roi_rect)

    # --------------------------------------
    # Blur Feature
    # --------------------------------------
    def apply_blur_feature(self):
        if self.current_image is None:
            self.status_label_features.config(text="No image to blur", fg="red")
            return
        self.temp_image = self.current_image.copy()
        self.blur_slider.set(self.blur_kernel)
        self.show_feature_controls("blur")
        self.status_label_features.config(text="Adjust blur intensity (live preview). ROI will be used if selected.", fg="orange")

    def update_blur_preview(self, value):
        if self.temp_image is None:
            return

        intensity = int(value)

        if self.selected_roi:
            preview = apply_blur_with_roi(self.temp_image.copy(), self.selected_roi, intensity=intensity)
        else:
            preview = apply_blur(self.temp_image.copy(), intensity=intensity)

        display_image(self, preview, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text=f"Preview: Blur (Intensity {intensity})", fg="blue")

    def confirm_blur(self):
        if self.temp_image is None:
            return
        if self.selected_roi:
            self.current_image = apply_blur_with_roi(self.temp_image.copy(), self.selected_roi, kernel_size=self.blur_kernel)
        else:
            self.current_image = apply_blur(self.temp_image.copy(), kernel_size=self.blur_kernel)
        display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text=f"Blur applied ({self.blur_kernel})", fg="green")
        self.hide_all_feature_controls()
        self.temp_image = None
        self.reset_roi_selection() 

    def cancel_blur(self):
        if self.temp_image is not None:
            self.current_image = self.temp_image.copy()
            display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
            self.status_label_features.config(text="Blur cancelled", fg="red")
        self.hide_all_feature_controls()
        self.reset_roi_selection()

    # --------------------------------------
    # Brightness Feature
    # --------------------------------------
    def apply_brightness_feature(self):
        if self.current_image is None:
            self.status_label_features.config(text="No image loaded", fg="red")
            return
        self.temp_image = self.current_image.copy()
        self.brightness_slider.set(self.brightness_value)
        self.show_feature_controls("brightness")
        self.status_label_features.config(text="Adjust brightness using the slider", fg="orange")

    def update_brightness_preview(self, value):
        if self.temp_image is None:
            return
        self.brightness_value = int(value)
        
        if self.selected_roi:
            preview = adjust_brightness_with_roi(self.temp_image.copy(), self.selected_roi, self.brightness_value)
        else:
            preview = adjust_brightness(self.temp_image.copy(), self.brightness_value)
            
        display_image(self, preview, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text=f"Preview: Brightness ({self.brightness_value})", fg="blue")

    def confirm_brightness(self):
        if self.temp_image is None: return
        val = self.brightness_slider.get()
        if self.selected_roi:
            self.current_image = adjust_brightness_with_roi(self.temp_image.copy(), self.selected_roi, val)
        else:
            self.current_image = adjust_brightness(self.temp_image.copy(), val)
        
        display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text=f"Brightness applied: {val}", fg="green")
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None

    def cancel_brightness(self):
        if self.temp_image is not None:
            display_image(self, self.temp_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None
        self.status_label_features.config(text="Brightness cancelled", fg="red")

    # --------------------------------------
    # Contrast Feature
    # --------------------------------------
    def apply_contrast_feature(self):
        if self.current_image is None:
            self.status_label_features.config(text="No image loaded", fg="red")
            return
        self.temp_image = self.current_image.copy()
        self.contrast_slider.set(self.contrast_value)
        self.show_feature_controls("contrast")
        self.status_label_features.config(text="Adjust contrast using the slider", fg="orange")

    def update_contrast_preview(self, value):
        if self.temp_image is None:
            return
        self.contrast_value = int(value)
        
        if self.selected_roi:
            preview = adjust_contrast_with_roi(self.temp_image.copy(), self.selected_roi, self.contrast_value)
        else:
            preview = adjust_contrast(self.temp_image.copy(), self.contrast_value)
            
        display_image(self, preview, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text=f"Preview: Contrast ({self.contrast_value})", fg="blue")

    def confirm_contrast(self):
        if self.temp_image is None: return
        val = self.contrast_slider.get()
        if self.selected_roi:
            self.current_image = adjust_contrast_with_roi(self.temp_image.copy(), self.selected_roi, val)
        else:
            self.current_image = adjust_contrast(self.temp_image.copy(), val)
            
        display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text="Contrast applied", fg="green")
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None

    def cancel_contrast(self):
        if self.temp_image is not None:
            display_image(self, self.temp_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None
        self.status_label_features.config(text="Contrast cancelled", fg="red")

    # --------------------------------------
    # Sharpen Feature
    # --------------------------------------
    def show_sharpen_controls(self):
        if self.current_image is None:
            self.status_label_features.config(text="No image loaded", fg="red")
            return
        self.temp_image = self.current_image.copy()
        self.sharpen_slider.set(0)
        self.show_feature_controls("sharpen")
        self.status_label_features.config(text="Adjust sharpen strength", fg="orange")

    def update_sharpen_preview(self, value):
        if self.temp_image is None:
            return
        strength = int(round(float(value)))
        if self.selected_roi:
            preview = apply_sharpen_with_roi(self.temp_image.copy(), self.selected_roi, strength)
        else:
            preview = apply_sharpen(self.temp_image.copy(), strength)
        display_image(self, preview, canvas=self.canvas_features, status_label=self.status_label_features)

    def confirm_sharpen(self):
        if self.temp_image is None: return
        strength = self.sharpen_slider.get()
        if self.selected_roi:
            self.current_image = apply_sharpen_with_roi(self.temp_image.copy(), self.selected_roi, strength)
        else:
            self.current_image = apply_sharpen(self.temp_image.copy(), strength)
            
        display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text=f"Sharpen applied ({strength})", fg="green")
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None
        
    def cancel_sharpen(self):
        if self.temp_image is not None:
            display_image(self, self.temp_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None
        self.status_label_features.config(text="Sharpen cancelled", fg="red")

    # --------------------------------------
    # Noise Reduction Feature
    # --------------------------------------

    def apply_noise_reduction_feature(self):
        if self.current_image is None:
            self.status_label_features.config(text="No image loaded", fg="red")
            return
        self.temp_image = self.current_image.copy()
        self.show_feature_controls("noise")
        self.status_label_features.config(text="Adjust denoise strength", fg="orange")

    def update_noise_reduction_preview(self, value):
        if self.temp_image is None:
            return
        
        kernel = kernel = max(1, int(int(value) * 15 / 100))

        if kernel % 2 == 0: kernel += 1
        
        if self.selected_roi:
            preview = apply_median_blur_with_roi(self.temp_image.copy(), self.selected_roi, kernel)
        else:
            preview = apply_median_blur(self.temp_image.copy(), kernel)
        
        display_image(self, preview, canvas=self.canvas_features, status_label=self.status_label_features)

    def confirm_noise_reduction(self):
        if self.temp_image is None: return
        kernel = self.noise_slider.get()
        if self.selected_roi:
            self.current_image = apply_median_blur_with_roi(self.temp_image.copy(), self.selected_roi, kernel)
        else:
            self.current_image = apply_median_blur(self.temp_image.copy(), kernel)
        
        display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text="Noise reduction applied", fg="green")
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None

    def cancel_noise_reduction(self):
        if self.temp_image is not None:
            display_image(self, self.temp_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.hide_all_feature_controls()
        self.reset_roi_selection()
    
    # --------------------------------------
    # Grayscale Feature
    # --------------------------------------
    def apply_grayscale_feature(self):
        if self.current_image is None:
            self.status_label_features.config(text="No image loaded", fg="red")
            return
        
        self.temp_image = self.current_image.copy()
        
        if self.selected_roi:
            preview = apply_grayscale_with_roi(self.temp_image.copy(), self.selected_roi)
        else:
            preview = apply_grayscale(self.temp_image.copy())
            
        display_image(self, preview, canvas=self.canvas_features, status_label=self.status_label_features)
        
        self.show_feature_controls("grayscale")
        self.status_label_features.config(text="Previewing Grayscale", fg="blue")

    def confirm_grayscale(self):
        if self.temp_image is None: return
        if self.selected_roi:
            self.current_image = apply_grayscale_with_roi(self.temp_image.copy(), self.selected_roi)
        else:
            self.current_image = apply_grayscale(self.temp_image.copy())
            
        display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
        self.status_label_features.config(text="Grayscale applied", fg="green")
        self.hide_all_feature_controls()
        self.reset_roi_selection()
        self.temp_image = None

    def cancel_grayscale(self):
        if self.temp_image is not None:
            # Revert to before preview
            display_image(self, self.temp_image, canvas=self.canvas_features, status_label=self.status_label_features)
        
        self.hide_all_feature_controls()
        self.temp_image = None
        self.status_label_features.config(text="Grayscale cancelled", fg="red")
        
    # --------------------------------------
    # Reset Feature
    # --------------------------------------
    def reset_to_original(self):
        """Revert the current image to the original state."""
        if hasattr(self, 'original_rgb_copy') and self.original_rgb_copy is not None:
            # Restore the image from the clean copy
            self.current_image = self.original_rgb_copy.copy()
            self.temp_image = None # Clear any temp previews
            
            # Reset all sliders to their default values
            self.blur_slider.set(5)
            self.brightness_slider.set(0)
            self.contrast_slider.set(0)
            self.sharpen_slider.set(0)
            
            # Hide any active tool controls
            self.hide_all_feature_controls()
            
            # Update the display
            display_image(self, self.current_image, canvas=self.canvas_features, status_label=self.status_label_features)
            self.status_label_features.config(text="Image reset to default", fg="orange")
        else:
            self.status_label_features.config(text="Nothing to reset", fg="red")

    # --------------------------------------
    # Save Image Feature
    # --------------------------------------
    def handle_save_image(self):
        """Open file dialog and save the current image."""
        if self.current_image is None:
            self.status_label_features.config(text="No image to save!", fg="red")
            return

        # Open Save As dialog
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG file", "*.png"),
                ("JPEG file", "*.jpg"),
                ("All Files", "*.*")
            ],
            title="Save Image As"
        )

        if file_path:
            # Call the save function we added to image_handler
            success = save_image(self.current_image, file_path)
            
            if success:
                filename = os.path.basename(file_path)
                self.status_label_features.config(text=f"Saved: {filename}", fg="green")
            else:
                self.status_label_features.config(text="Error saving file", fg="red")