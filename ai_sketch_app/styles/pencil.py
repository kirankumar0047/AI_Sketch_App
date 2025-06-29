import cv2
import numpy as np

def pencil_sketch(image, intensity=1.0):
    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Invert the grayscale image
    inverted = 255 - gray

    # Step 3: Apply Gaussian blur
    blur = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)

    # Step 4: Invert the blurred image
    inverted_blur = 255 - blur

    # Step 5: Blend using dodge technique and apply intensity scaling
    blend = cv2.divide(gray, inverted_blur, scale=256.0)
    sketch = cv2.convertScaleAbs(blend, alpha=intensity)

    # Step 6: Optional sharpening
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sketch = cv2.filter2D(sketch, -1, kernel)

    # Step 7: Convert back to 3-channel image for display
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)