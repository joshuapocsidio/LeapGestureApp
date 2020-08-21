import controller.DataOptimizer as Optimizer
import leapio.Printer as Printer
from Tkinter import *
from view.menu import MainMenu, TrainingMenu, ClassificationMenu


def show_ui(controller):  # Calls required functions to show each sub menu
    # root = Tk()
    # label = Label(root, text="Gesture Application")
    # label.pack()
    # root.mainloop()
    # Initialize required variables here
    MainMenu.show(controller)
    print("SYSTEM TERMINATED")
