import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
from styles.pencil import pencil_sketch

def run_webcam_sketch():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not access the webcam.")
        return

    print("📷 Press 's' to save sketch, 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break

        sketch = pencil_sketch(frame)

        # Stack original and sketch side by side
        stacked = cv2.hconcat([frame, sketch])
        cv2.imshow("🖼️ Webcam Sketch (Left: Original, Right: Pencil)", stacked)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite("output/webcam_sketch_saved.jpg", sketch)
            print("✅ Sketch saved to output/webcam_sketch_saved.jpg")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam_sketch()