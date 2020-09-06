import sys
from string import lower, upper
import time

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
        print("(1) - Manual Acquisition")
        print("(2) - Systematic Acquisition : Training Set")
        print("(3) - Systematic Acquisition : Testing Set")
        print("(0) - Back")

        choice = raw_input("Your Choice: ")

        if choice == '1':
            manual_acquisition(controller=controller)
            pass
        elif choice == '2':
            training_acquisition(controller=controller)
            pass
        elif choice == '3':
            pass
        elif choice == '0':
            done = True
            pass
        else:
            print("Please try again.")
            pass
    pass

def training_acquisition(controller):
    print("--------------------")
    print("TRAINING ACQUISITION")
    print("--------------------")
    print("1 --> Counting Gestures (6 Gestures)")
    print("2 --> Status Gestures (10 Gestures)")
    print("3 --> American Sign Language (ASL) (26 Gestures)")

    time.sleep(1)
    # Initialize acquisitor with subject name
    subject_name = prompt_subject_name()
    acquisitor = LeapDataAcquisitor(leap_controller=controller, subject_name=subject_name, supervised=False)
    gesture_src = ['gestures_counting.txt', 'gestures_status.txt', 'gestures_asl.txt']
    gesture_titles = ['Counting Gestures', 'Status Gestures', 'American Sign Language Gestures']
    hand_config = ['LEFT HAND', 'RIGHT HAND']
    lighting_config = ['WELL LIT ENVIRONMENT', 'DIMLY LIT ENVIRONMENT']

    # Change this between sessions
    cur_lighting = lighting_config[0]

    i_src = 0
    while i_src < len(gesture_src):
        print("* * * * * * * * " + gesture_titles[i_src] + "* * * * * * * * ")
        # Obtain gestures from file
        gesture_list = io.read_col(gesture_src[i_src])

        # Loop between gestures
        i_ges = 0
        while i_ges < len(gesture_list):
            cur_gesture = gesture_list[i_ges]

            # Loop between hands
            i_hand = 0
            while i_hand < len(hand_config):
                print("Acquiring Gesture : " + upper(cur_gesture) + " --> " + hand_config[i_hand] + " ")

                # Loop between each gesture data taken
                print("\rProgress ----> " + str(0) + "/50 acquired"),
                raw_input("\nSystem       :       Press any key to get data: "),
                time.sleep(2)
                n_taken = 0
                # raw_input("\rSystem       :       Valid hand(s) detected --> Press any key to get data: \r"),
                while n_taken < 50:
                    # Acquire data
                    acquisitor.get_all_hand_feature_type(gesture_name=cur_gesture)
                    n_taken += 1
                    print("\rProgress ----> " + str(n_taken) + "/50 acquired"),

                    if n_taken % 10 == 0:
                        if n_taken == 50:
                            raw_input("\nSystem       :       Gesture Checkpoint reached. Press any key to continue"),
                        else:
                            raw_input("\nSystem       :       Press any key to get data: "),
                    pass

                print(" -- SUCCESS!\n")
                i_hand += 1
                pass

            i_ges += 1
            pass

        i_src += 1
        pass

    print("")
    print("* * * * Counting Gestures * * * *")
    print("Acquiring Gesture : Five")

    pass

def testing_acquisition(controller):
    pass


def manual_acquisition(controller):
    done = False
    acquisitor = None
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
            subject_name = prompt_subject_name()
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


def prompt_subject_name():
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


def prompt_gesture_name(gesture_src='gestures_asl.txt'):
    # Prompts user for name of gesture
    done = False

    while done is False:
        gesture_list = io.read_col(gesture_src)
        print("* List of Valid Gestures *")
        printer.print_numbered_list(gesture_list)
        choice = raw_input("Enter the Gesture Name: ")
        gesture_name = lower(gesture_list[int(choice) - 1])
        print("")

        num_choice = int(choice)

        if num_choice < 1 and num_choice > len(gesture_list):
            print("Please try again")
        else:
            return gesture_name

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
