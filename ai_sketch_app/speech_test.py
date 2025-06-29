import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("🎤 Say something...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

print("🧠 Recognizing...")

try:
    text = r.recognize_google(audio)
    print(f"✅ You said: {text}")
except sr.UnknownValueError:
    print("🤷 Could not understand audio.")
except sr.RequestError:
    print("❌ Could not connect to the recognition service.")