from string import lower

import leapio.LeapIO as io
import leapio.Printer as printer
from controller.LeapDataAcquisitor import LeapDataAcquisitor
from leapio import Printer


def show(controller):
    # Shows menu for data acquisition related menu
    done = False

    while done is False:
        print("----------------")
        print("DATA ACQUISITION")
        print("----------------")
        print("(1) - Feature Data Set : Finger to Palm Distance")
        print("(2) - Feature Data Set : Finger to Palm Angle")
        print("(3) - Feature Data Set : Finger to Palm Distance and Angle")
        print("(4) - Feature Data Set : Finger to Finger Distance")
        print("(9) - Feature Data Set : ALL")
        print("(0) - Back")

        choice = raw_input("Your Choice: ")

        if choice != '0' and choice is not None and choice != '':
            subject_name = prompt_subject_name
            # Initialise the Acquisitor
            acquisitor = LeapDataAcquisitor(leap_controller=controller, subject_name=subject_name)

        if choice == '1':
            # Get the gesture name
            gesture_name = prompt_gesture_name()
            iterations = prompt_iterations()
            # Call Data Acquisitor function
            acquisitor.get_palm_to_finger_distance_set(gesture_name=gesture_name, iterations=iterations)
            pass
        elif choice == '2':
            # Get the gesture name
            gesture_name = prompt_gesture_name()
            iterations = prompt_iterations()
            # Call Data Acquisitor function
            acquisitor.get_palm_to_finger_angle_set(gesture_name=gesture_name, iterations=iterations)
            pass
        elif choice == '3':
            # Get the gesture name
            gesture_name = prompt_gesture_name()
            iterations = prompt_iterations()
            # Call Data Acquisitor function
            acquisitor.get_finger_to_palm_angle_and_distance(gesture_name=gesture_name, iterations=iterations)
            pass
        elif choice == '4':
            # Get the gesture name
            gesture_name = prompt_gesture_name()
            iterations = prompt_iterations()
            # Call Data Acquisitor function
            acquisitor.get_distance_between_fingers_set(gesture_name=gesture_name, iterations=iterations)
            pass
        elif choice == '9':
            # Get the gesture name
            gesture_name = prompt_gesture_name()
            iterations = prompt_iterations()
            # Acquire all feature data
            acquisitor.get_all_hand_feature_type(gesture_name=gesture_name, iterations=iterations)
            pass
        elif choice == '0':
            done = True
            pass
        else:
            print("Please try again")
            pass


def prompt_subject_name(self):
    done = False
    while done is False:
        print("~ ~ ~ ~ ~ ~ ~ ~ SUBJECT NAMES ~ ~ ~ ~ ~ ~ ~ ~")
        subjects = io.read_col('subjects.txt')
        Printer.print_numbered_list(subjects)
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

        choice = raw_input("Enter the subject name to train from: ")

        if int(choice) > len(subjects) or int(choice) < 1:
            print("Please try again.")
        else:
            subject_name = subjects[int(choice) - 1]
            print("Chosen Name : " + subject_name)
            print("")
            return subject_name


def prompt_gesture_name(gesture_src='gestures.txt'):
    # Prompts user for name of gesture
    done = False

    while done is False:
        gesture_list = io.read_col(gesture_src)
        print("* List of Valid Gestures *")
        printer.print_numbered_list(gesture_list)
        choice = raw_input("Enter the Gesture Name: ")
        gesture_name = lower(gesture_list[int(choice) - 1])
        print("")

        if gesture_name is not None or gesture_name is not "":
            done = True
            return gesture_name
        else:
            print("Please try again")


def prompt_iterations():
    # Prompts user for number of iterations
    done = False

    while done is False:
        iterations = raw_input("Training Size: ")

        if iterations.isdigit() is not False or iterations is not None or iterations is not "":
            done = True
            return int(iterations)
        else:
            print("Please try again")
