import tkinter as tk

class LeapUI():
    def __init__(self):
        self.main = tk.Tk()
        self.create_widgets()


    def create_widgets(self):
        self.label = tk.Label(self.main, text='')
        self.label.pack()

    def update_label(self, label):
        self.label = tk.Label(self.main, text='label')
