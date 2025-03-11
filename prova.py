import cv2 as cv
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Webcam su Tkinter Canvas")
        self.geometry("800x600")

        # Creazione del Canvas per la webcam
        self.canvas = tk.Canvas(self, width=640, height=480, bg="black")
        self.canvas.pack(pady=20)

        # Inizializzazione della webcam
        self.cap = cv.VideoCapture(0)
        self.update_webcam()

        # Bottone per chiudere
        self.quit_button = tk.Button(self, text="Chiudi", command=self.quit)
        self.quit_button.pack()

    def update_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            # Converti il frame in formato Tkinter
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)

            # Aggiorna il canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
            self.canvas.image = frame  # Importante: evitare che venga garbage collected

        # Richiama la funzione ogni 20ms
        self.after(20, self.update_webcam)

    def quit(self):
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
