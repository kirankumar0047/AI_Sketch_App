import cv2
import numpy as np

def apply_3d_shading(image, depth_map, intensity=0.15):
    # Apply colormap based on depth
    shading = cv2.applyColorMap(depth_map, cv2.COLORMAP_TWILIGHT)
    shading = cv2.GaussianBlur(shading, (9, 9), 0)

    # Blend shading with original image
    shaded = cv2.addWeighted(image, 1 - intensity, shading, intensity, 0)
    return shaded