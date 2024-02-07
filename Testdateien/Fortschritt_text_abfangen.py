import tkinter as tk
from tkinter import ttk
import time
import sys

class CustomPrintHook:
    def write(self, text):
        if "Spezieller Text" in text:
            # Hier wird der spezielle Text abgefangen, und Sie können Ihren Code hier einfügen
            sys.__stdout__.write("Spezieller Text wurde abgefangen!\n")
            # Führen Sie hier Ihren eigenen Code aus
            sys.__stdout__.write(text)
            print("hi")

    def flush(self):
        pass

# Den Print-Hook aktivieren
sys.stdout = CustomPrintHook()

def update_progress(progress_var, label_var, progress_step=10):
    for i in range(0, 101, progress_step):
        time.sleep(0.1)  # Simuliert eine längere Berechnungsdauer
        progress_var.set(i)
        label_var.config(text=f'Fortschritt: {i}%')
        root.update_idletasks()  # Aktualisiert das GUI-Fenster
    label_var.config(text='Fertig!')


# GUI erstellen
root = tk.Tk()
root.title('Fortschrittsbalken')

# Fortschrittsvariable erstellen
progress_var = tk.IntVar()

# Label für Fortschrittsanzeige erstellen
progress_label = tk.Label(root, text='Fortschritt: 0%')
progress_label.pack(pady=10)

# Fortschrittsbalken erstellen
progress_bar = ttk.Progressbar(root, variable=progress_var, length=300, mode='determinate')
progress_bar.pack(pady=10)

# Button zum Starten der Aktualisierung erstellen
start_button = tk.Button(root, text='Start', command=lambda: update_progress(progress_var, progress_label))
start_button.pack(pady=10)

# GUI starten
root.mainloop()
