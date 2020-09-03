from view.menu import MainMenu


def show_ui(controller):  # Calls required functions to show each sub menu
    # root = Tk()
    # label = Label(root, text="Gesture Application")
    # label.pack()
    # root.mainloop()
    # Initialize required variables here
    MainMenu.show(controller)
    print("SYSTEM TERMINATED")
