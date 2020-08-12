import controller.DataOptimizer as Optimizer
import leapio.Printer as Printer

from view.menu import MainMenu, TrainingMenu, ClassificationMenu


def show_ui(controller):  # Calls required functions to show each sub menu
    # Initialize required variables here
    MainMenu.show(controller)
    print("SYSTEM TERMINATED")
