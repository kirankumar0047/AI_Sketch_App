import os
os.environ["PYTHON_SPEECH_RECOGNITION_USE_SOUNDDEVICE"] = "1"  # Fix PyAudio error

import streamlit as st
import cv2
import numpy as np
import speech_recognition as sr
from PIL import Image
from styles.pencil import pencil_sketch
from styles.charcoal import charcoal_sketch
from styles.cartoon import cartoon_sketch
from duckduckgo_search import DDGS
import requests

# --------------- Utilities ---------------
def fetch_image_from_web(keyword, save_path):
    with DDGS() as ddgs:
        results = ddgs.images(keyword, max_results=1)
        for result in results:
            try:
                img_url = result["image"]
                r = requests.get(img_url)
                if r.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(r.content)
                    return True
            except:
                pass
    return False

def find_image_in_dataset(keyword):
    for ext in ["jpg", "jpeg", "png"]:
        path = f"dataset/{keyword}.{ext}"
        if os.path.exists(path):
            return path
    return None

def apply_ghibli_tint(img):
    if len(img.shape) == 2 or img.shape[2] == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    tint = np.full_like(img, (30, 20, 70))
    return cv2.addWeighted(img, 0.9, tint, 0.1, 0)

def enhance_contrast(img):
    if len(img.shape) == 2 or img.shape[2] == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0)
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

def overlay_frame(base_img, frame_path):
    frame = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
    if frame is None:
        return base_img
    frame = cv2.resize(frame, (base_img.shape[1], base_img.shape[0]))
    if frame.shape[2] == 4:
        alpha = frame[:, :, 3] / 255.0
        for c in range(3):
            base_img[:, :, c] = (1 - alpha) * base_img[:, :, c] + alpha * frame[:, :, c]
    return base_img

# --------------- UI Setup ---------------
st.set_page_config(page_title="AI Sketch Generator", layout="centered")
st.title("🎨 AI Sketch Generator")

tab1, tab2, tab3, tab4 = st.tabs(["Upload Image", "Voice Sketch", "Webcam Sketch", "Gallery"])

frame_options = [f for f in os.listdir("frames") if f.endswith(".png")]
frame_choice = st.sidebar.selectbox("Add Frame (optional)", ["None"] + frame_options)
enhancement = st.sidebar.radio("AI Enhancement", ["None", "Enhance Contrast", "Apply Ghibli Tint"])
intensity = st.sidebar.slider("Pencil Intensity", 0.5, 2.0, 1.0, step=0.1)

# --------------- TAB 1: Upload ---------------
with tab1:
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    style = st.radio("Choose Style", ["Pencil", "Charcoal", "Cartoon"], horizontal=True)

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        if style == "Pencil":
            sketch = pencil_sketch(image, intensity)
        elif style == "Charcoal":
            sketch = charcoal_sketch(image)
        else:
            sketch = cartoon_sketch(image)

        if enhancement == "Enhance Contrast":
            sketch = enhance_contrast(sketch)
        elif enhancement == "Apply Ghibli Tint":
            sketch = apply_ghibli_tint(sketch)

        if frame_choice != "None":
            sketch = overlay_frame(sketch, os.path.join("frames", frame_choice))

        col1, col2 = st.columns(2)
        col1.image(image, caption="Original", use_container_width=True)
        col2.image(sketch, caption=f"{style} Sketch", use_container_width=True)

        output_path = f"output/upload_{style.lower()}.jpg"
        cv2.imwrite(output_path, sketch)

        st.download_button("📥 Download Sketch", data=cv2.imencode(".jpg", sketch)[1].tobytes(), file_name="sketch.jpg")

# --------------- TAB 2: Voice Sketch ---------------
with tab2:
    st.subheader("🎤 Speak an image keyword (e.g., 'dog', 'lion')")
    if st.button("🎙 Start Listening"):
        r = sr.Recognizer()
        mic_index = 0  # ← Set to your working mic index (0 is default)

        try:
            with sr.Microphone(device_index=0) as source:
                st.info("🎧 Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10)

            command = r.recognize_google(audio).lower()
            st.success(f"You said: **{command}**")
            keyword = command.strip().split()[-1]

            img_path = find_image_in_dataset(keyword)
            if img_path is None:
                st.warning("Fetching online...")
                img_path = f"dataset/{keyword}.jpg"
                if not fetch_image_from_web(keyword, img_path):
                    st.error("Could not find image.")
                    st.stop()

            image = cv2.imread(img_path)
            sketch = pencil_sketch(image, intensity)

            if enhancement == "Enhance Contrast":
                sketch = enhance_contrast(sketch)
            elif enhancement == "Apply Ghibli Tint":
                sketch = apply_ghibli_tint(sketch)

            if frame_choice != "None":
                sketch = overlay_frame(sketch, os.path.join("frames", frame_choice))

            col1, col2 = st.columns(2)
            col1.image(image, caption="Original", use_container_width=True)
            col2.image(sketch, caption="Pencil Sketch", use_container_width=True)

            st.download_button("📥 Download", data=cv2.imencode(".jpg", sketch)[1].tobytes(), file_name=f"{keyword}_sketch.jpg")

        except sr.WaitTimeoutError:
            st.error("⏱️ You didn't speak in time.")
        except sr.UnknownValueError:
            st.error("🤷 Could not understand.")
        except sr.RequestError:
            st.error("❌ Could not connect to recognition service.")
        except Exception as e:
            st.error(f"🚨 Error: {e}")

# --------------- TAB 3: Webcam Sketch ---------------
with tab3:
    st.subheader("📷 Webcam to Sketch")
    img_file = st.camera_input("Take a Snapshot")

    if img_file is not None:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        sketch = pencil_sketch(image, intensity)

        if enhancement == "Enhance Contrast":
            sketch = enhance_contrast(sketch)
        elif enhancement == "Apply Ghibli Tint":
            sketch = apply_ghibli_tint(sketch)

        if frame_choice != "None":
            sketch = overlay_frame(sketch, os.path.join("frames", frame_choice))

        col1, col2 = st.columns(2)
        col1.image(image, caption="Original", use_container_width=True)
        col2.image(sketch, caption="Webcam Sketch", use_container_width=True)

        st.download_button("📥 Download", data=cv2.imencode(".jpg", sketch)[1].tobytes(), file_name="webcam_sketch.jpg")

# --------------- TAB 4: Gallery ---------------
with tab4:
    st.subheader("🖼️ Sketch Gallery")
    os.makedirs("output", exist_ok=True)
    images = [f for f in os.listdir("output") if f.endswith((".jpg", ".png"))]

    if images:
        cols = st.columns(3)
        for i, img_file in enumerate(images):
            img = Image.open(os.path.join("output", img_file))
            cols[i % 3].image(img, caption=img_file, use_container_width=True)
    else:
        st.info("No sketches saved yet.")

     # to run this project 

       # Activate your virtual environment:
       # "source .venv/bin/activate"

      # ModuleNotFoundError: No module named 'cv2'
      # "pip install opencv-python" ,"pip install opencv-contrib-python"
        
      # ModuleNotFoundError: No module named 'speech_recognition'
      # "pip install SpeechRecognition"

        
       # ModuleNotFoundError: No module named 'duckduckgo_search'
       #  "pip install duckduckgo-search"

       # "streamlit run app.py"


