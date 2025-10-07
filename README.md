Smart Mood Lamp with OpenCV

A mood-aware study lamp that uses computer vision to monitor facial expressions and indicate stress levels in real-time with a changing lamp color and a stress-level graph.


---

Features

Real-time stress detection using OpenCV Haar cascades (faces, eyes, smiles).

Color-coded lamp for stress levels:

Green → Low stress

Yellow → Medium stress

Red → High stress (with break alert notification)


Dynamic stress graph showing stress level history over time.

Break alert if high stress is detected for more than 10 minutes.

Easy-to-use Tkinter GUI.



---

Screenshots
![Mood lamp showinf red color for high stressbwith break alert](<2025-10-07 (11).png>)
![Mood lamp showing yellow color for medium stree](<2025-10-07 (14).png>)
![Mood lamp showing green color for low stree](<2025-10-07 (3).png>)


---

Installation

1. Clone the repository:
git clone <https://github.com/AFIA-REFAL/SmartMoodLamp>
cd smart-mood-lamp

2. Install required packages:
pip install opencv-python matplotlib

> Tkinter is included with most Python installations by default.

3. Run the application:
python mood_lamp.py
---

Usage

1. Launch the application.


2. Allow camera access when prompted.


3. The lamp background color will change based on your detected stress level.


4. A graph displays your stress level over time.


5. If stress is high for more than 10 minutes, a break alert will pop up.

---

How It Works

Captures video from your webcam.

Detects faces, eyes, and smiles using OpenCV Haar cascades.

Uses a simple heuristic to determine stress level:

No eyes detected → high stress

No smile detected → medium stress

Otherwise → low stress


Updates the lamp color and graph in real-time.
---

Dependencies

Python 3.x

OpenCV (opencv-python)

Matplotlib (matplotlib)

Tkinter (usually pre-installed with Python)
---
Future Improvements

Use deep learning models for more accurate stress detection.

Add sound or vibration alerts for high stress.

Integrate with smart home lights for real ambient lighting.

License

MIT License © 2025