# ------------------ Smart Mood Lamp with OpenCV ------------------
import cv2
import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------ Haar Cascades ------------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

def detect_stress():
    ret, frame = cap.read()
    if not ret:
        return 'L'

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    stress_score = 0

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 20)

        # Heuristic rules:
        # - No eyes detected in face → frowning → stress
        # - No smile detected → neutral/tensed → slight stress
        face_stress = 0
        if len(eyes) == 0:
            face_stress = 2  # high stress
        elif len(smiles) == 0:
            face_stress = 1  # medium stress
        stress_score = max(stress_score, face_stress)

    # Map score to stress level
    if stress_score == 0:
        return 'L'
    elif stress_score == 1:
        return 'M'
    else:
        return 'H'

# ------------------ Lamp GUI + Graph ------------------
class MoodLamp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mood-Aware Study Lamp")
        self.root.geometry("400x500")
        self.lamp_color = "#00FF00"
        self.root.configure(bg=self.lamp_color)
        self.last_high_time = None
        self.stress_history = []
        self.time_history = []
        self.start_time = time.time()

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(4,2))
        self.ax.set_ylim(0,2)
        self.ax.set_xlim(0,60)
        self.ax.set_yticks([0,1,2])
        self.ax.set_yticklabels(['Low','Medium','High'])
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Stress Level')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=20)

        self.update_lamp()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def update_lamp(self):
        stress = detect_stress()
        current_time = int(time.time() - self.start_time)

        if stress == 'L':
            self.lamp_color = "#00FF00"
            stress_value = 0
            self.last_high_time = None
        elif stress == 'M':
            self.lamp_color = "#FFFF00"
            stress_value = 1
            self.last_high_time = None
        else:
            self.lamp_color = "#FF0000"
            stress_value = 2
            if self.last_high_time is None:
                self.last_high_time = time.time()
            elif time.time() - self.last_high_time > 600:
                messagebox.showinfo("Break Alert", "High stress detected! Take a short break.")
                self.last_high_time = time.time()

        self.root.configure(bg=self.lamp_color)

        # Update stress history
        self.stress_history.append(stress_value)
        self.time_history.append(current_time)
        self.ax.clear()
        self.ax.set_ylim(0,2)
        self.ax.set_xlim(max(0,current_time-60), current_time+1)
        self.ax.set_yticks([0,1,2])
        self.ax.set_yticklabels(['Low','Medium','High'])
        self.ax.plot(self.time_history, self.stress_history, color='blue', marker='o')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Stress Level')
        self.canvas.draw()

        self.root.after(1000, self.update_lamp)

    def on_close(self):
        cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

# ------------------ Run ------------------
if __name__ == "__main__":
    MoodLamp()