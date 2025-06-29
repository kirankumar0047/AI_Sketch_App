import cv2
import numpy as np

def cartoon_sketch(image):
    # Resize for consistency
    img = cv2.resize(image, (image.shape[1], image.shape[0]))

    # Step 1: Apply bilateral filter to smooth textures (like 3D render)
    smooth = cv2.bilateralFilter(img, d=15, sigmaColor=100, sigmaSpace=100)

    # Step 2: Color quantization (reduce colors for painterly feel)
    data = np.float32(smooth).reshape((-1, 3))
    _, labels, centers = cv2.kmeans(
        data, 8, None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5),
        10, cv2.KMEANS_RANDOM_CENTERS
    )
    quantized = centers[labels.flatten()].reshape(img.shape).astype(np.uint8)

    # Step 3: Remove blue/white lighting by applying warm tone
    warm_overlay = np.full_like(quantized, (20, 35, 60))  # BGR warm tint
    warm_image = cv2.addWeighted(quantized, 0.95, warm_overlay, 0.05, 0)

    # Step 4: Add subtle shadow using gamma correction
    gamma = 1.2
    look_up_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in np.arange(0, 256)]).astype("uint8")
    warm_gamma_corrected = cv2.LUT(warm_image, look_up_table)

    return warm_gamma_corrected