from view.menu import AcquisitionMenu, TrainingMenu, ClassificationMenu


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

        if choice == '1':
            AcquisitionMenu.show(controller)
        elif choice == '2':
            TrainingMenu.show()
        elif choice == '3':
            ClassificationMenu.show(leap_controller=controller)
        elif choice == '4':
            pass
        elif choice == '0':
            # Shows GUI for exiting the program
            done = True