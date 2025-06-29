import cv2

def charcoal_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blur = cv2.GaussianBlur(inverted, (35, 35), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)
    charcoal = cv2.GaussianBlur(sketch, (3, 3), 0)
    return charcoal