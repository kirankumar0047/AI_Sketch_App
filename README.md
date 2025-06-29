🎨 AI Sketch App — Intelligent Drawing with Voice, Image & Camera Input:

![developer](https://img.shields.io/badge/Developed%20By%20%3A-Kolla%20KiranKumar-red)
---

A next-gen AI-powered app that transforms **images, webcam feed**, or **voice prompts** into intelligent sketches in various styles. Supports **multi-object detection**, **depth-aware 3D sketches**, and **real-time drawing**, all with a clean **Streamlit** UI.

Features:
- Upload image → Get AI Sketch
- Voice prompt → Auto search & sketch (e.g., "dog with hat")
- Live webcam sketching
- Multi-object detection sketch (YOLO-based)
- Multiple sketch styles (pencil, charcoal, cartoon)
- Depth-aware 3D-style sketches
- Streamlit-based clean user interface

Tech Stack:
________________________________________________________
| Component           | Tech Used                      |
|---------------------|-------------------------------|
| AI/ML Frameworks    | OpenCV, YOLOv5, PIL, NumPy     |
| Voice Input         | `speech_recognition`, `gTTS`   |
| Image Search        | `duckduckgo_search` API        |
| UI Framework        | `Streamlit`                    |
| 3D Depth Mapping    | `MiDaS` / `OpenCV` Depth utils |
| Object Detection    | YOLOv5 pretrained models       |

How It Works:
1. Choose Input**: Upload image / Webcam / Voice prompt
2. Detect Objects** (if enabled)
3. Sketch Generation**:
   - Pencil sketch
   - Charcoal effect
   - Cartoonized version
   - 3D Depth outline
4. Display in Streamlit GUI
5. (Optional) Save or download output image

Run It Locally:
1. Create virtual environment

2. Install dependencies
pip install -r requirements.txt

3. Run the app
streamlit run app.py

Outcomes:
____________________________________________________________
| Input                     |      Output                   |
|___________________________|_______________________________|
| 1.Uploaded photo          |  Pencil Sketch                |
| 2.Puppy with sunglasses   |  Sketch from Google image     |
| 3.Webcam face             | Live drawing with depth filter|
_____________________________________________________________
