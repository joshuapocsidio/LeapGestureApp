from view.menu import AcquisitionMenu, RecognitionMenu
from view.menu.ClassificationMenu import ClassificationMenu
from view.menu.TrainingMenu import TrainingMenu


def show(controller):
    # Shows menu for main menu
    done = False

    while done is False:
        print("---------")
        print("MAIN MENU")
        print("---------")
        print("(1) - Gesture Data Acquisition")
        print("(2) - Gesture Data Training")
        print("(3) - Gesture Classification Testing")
        print("(4) - Real Time Gesture Recognition")
        print("(0) - Exit Program")

        choice = raw_input("Your Choice: ")
        print("YOUR INPUT: " + choice)
        if choice == '1':
            AcquisitionMenu.show(controller)
        elif choice == '2':
            training_menu = TrainingMenu()
            training_menu.show()
        elif choice == '3':
            classification_menu = ClassificationMenu(leap_controller=controller)
            classification_menu.show()
        elif choice == '4':
            recognition_menu = RecognitionMenu.show(leap_controller=controller)
            pass
        elif choice == '0':
            # Shows GUI for exiting the program
            done = True