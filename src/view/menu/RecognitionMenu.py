import time
from controller.LeapDataAcquisitor import LeapDataAcquisitor
from controller.LeapDataTrainer import SVM_Trainer
import leapio.LeapIO as io
import leapio.Printer as printer
import numpy as np


def show(leap_controller):
    done = False
    while done is False:
        print("---------------------")
        print("REAL TIME RECOGNITION")
        print("---------------------")
        print("(1) - Live Demo")
        print("(2) - Loop Demo")
        print("(9) - One Gesture Test")
        print("(0) - Exit Program")

        choice = raw_input("Your Choice: ")
        print("Your Input : " + choice)
        if choice == '1':
            acquisitor = LeapDataAcquisitor(leap_controller=leap_controller, subject_name=None, supervised=False)
            start_time = time.time()

            sample_list = []
            hand_list = []

            # Show files available for classification (pickle files)
            list_data_files = io.get_pickle_files()
            print("* List of Pickle Files *")
            printer.print_numbered_list(list_data_files)
            print("\n")

            choice = raw_input("Enter the pickle file for classifier \nPickle Index  : ")
            chosen_pickle = list_data_files[int(choice) - 1]
            chosen_pickle_no_extension = chosen_pickle.rsplit(".", 1)[0]
            kernel_type = chosen_pickle_no_extension.rsplit("_", 1)[-1]

            # Show feature type and kernel type based on chosen pickle file
            print("Chosen Pickle : " + chosen_pickle)
            print("Kernel Type   : " + kernel_type + "\n")

            # Call data classification functions
            trainer = SVM_Trainer(subject_name="JOSHUA", feature_type=chosen_pickle_no_extension, kernel_type=kernel_type)
            trainer.load(chosen_pickle)

            # Do demo for 1 minute
            time_elapsed = 0.0
            stack = 0
            print("\r.."),
            while time_elapsed <= 60:
                time_elapsed = round(time.time() - start_time, 2)

                frame = leap_controller.frame()
                hands = frame.hands
                if len(hands) > 0:
                    data = acquisitor.get_palm_to_finger_distance_set(return_mode=True)
                    prediction = trainer.classify([data])

                    while prediction == trainer.classify([acquisitor.get_palm_to_finger_distance_set(return_mode=True)]) and stack < 5:
                        stack += 1

                    if stack >= 5:
                        print("\rTime Elapsed : " + str(time_elapsed) + " seconds ---> Prediction : " + str(prediction[0])),
                        stack = 0

                    time.sleep(0.1)
                else:
                    print("\rTime Elapsed : " + str(time_elapsed) + " seconds ---> Prediction : None"),
                    stack = 0

            print("System       : Demo has completed.\n\n")
            print("----------------------------------------------------")
            print("Number of Samples          : " + str(len(sample_list)))
            print("Number of Frame per Sample : " + str(len(hand_list)))
            print("----------------------------------------------------\n\n")

            pass
        elif choice == '2':
            done = True
            print("")
            while done is True:
                frame = leap_controller.frame()
                hand = frame.hands[0]

                x_d = round(hand.palm_normal.x, 5)
                y_d = round(hand.palm_normal.y, 5)
                z_d = round(hand.palm_normal.z, 5)
                print("\r" + str(x_d) + ", " + str(y_d) + ", " + str(z_d)),
            pass
        elif choice == '9':
            pass
        elif choice == '0':
            # Exit
            done = True
            pass
