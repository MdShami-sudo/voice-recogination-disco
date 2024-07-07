import tkinter as tk
from tkinter import ttk
import speech_recognition as sr

class DiscoLightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recognition Disco Light")
        self.root.geometry("600x400")

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)

        self.circle = self.canvas.create_oval(200, 100, 400, 300, fill="white")

        self.label = ttk.Label(self.root, text="Say 'red', 'green', 'blue', or 'yellow' to change the circle color.", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.listen_for_commands()

    def listen_for_commands(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 300
            recognizer.pause_threshold = 0.5
            recognizer.operation_timeout = 1

        def callback(recognizer, audio):
            try:
                command = recognizer.recognize_google(audio, show_all=False).lower()
                self.change_color(command)
            except sr.UnknownValueError:
                self.label.config(text="Could not understand the command. Please try again.")
            except sr.RequestError:
                self.label.config(text="Could not request results from Google Speech Recognition service.")

        recognizer.listen_in_background(microphone, callback, phrase_time_limit=2)

    def change_color(self, command):
        colors = {
            'red': '#FF0000',
            'green': '#00FF00',
            'blue': '#0000FF',
            'yellow': '#FFFF00'
        }
        if command in colors:
            self.canvas.itemconfig(self.circle, fill=colors[command])
            self.label.config(text=f"Changed circle color to {command}.")
        else:
            self.label.config(text=f"Command '{command}' not recognized. Please say 'red', 'green', 'blue', or 'yellow'.")

def main():
    root = tk.Tk()
    app = DiscoLightApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
