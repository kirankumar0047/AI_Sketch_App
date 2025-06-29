import cv2
from styles.pencil import pencil_sketch

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Webcam not accessible")
    exit()

print("✅ Press 'q' to quit...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    sketch = pencil_sketch(frame)
    combined = cv2.hconcat([frame, sketch])

    cv2.imshow("Live Pencil Sketch (Left: Original | Right: Sketch)", combined)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()