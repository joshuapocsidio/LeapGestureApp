import time
from controller.LeapDataAcquisitor import LeapDataAcquisitor
from controller.LeapDataTrainer import SVM_Trainer
import leapio.LeapIO as io
import leapio.Printer as printer
from string import strip
import numpy as np
import Leap
import pandas as pd


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
            subject_name = chosen_pickle_no_extension.rsplit("(", 1)[1].rsplit(")")[0]
            feature_type = strip(chosen_pickle_no_extension.rsplit(")")[1].rsplit(".")[0])
            # Show feature type and kernel type based on chosen pickle file
            print("Chosen Pickle : " + chosen_pickle)
            print("Kernel Type   : " + kernel_type + "\n")

            # Call data classification functions
            trainer = SVM_Trainer(subject_name=subject_name, feature_type=feature_type, kernel_type=kernel_type)
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
                    hand = hands[0]
                    data = get_relevant_data(kernel_type=kernel_type, file_name=chosen_pickle_no_extension, acquisitor=acquisitor, hand=hand)
                    prediction = trainer.classify(data)

                    hand = leap_controller.frame().hands[0]
                    while prediction == trainer.classify(get_relevant_data(kernel_type=kernel_type, file_name=chosen_pickle_no_extension, acquisitor=acquisitor, hand=hand)) and stack < 5:
                        hand = leap_controller.frame().hands[0]
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
                up = Leap.Vector.up
                round(up.x, 1)
                round(up.y, 1)
                round(up.z, 1)
                print(up)
                x = round(hand.palm_normal.x, 1)
                y = round(hand.palm_normal.y, 1)
                z = round(hand.palm_normal.z, 1)
                print ("(" + str(x) + "," + str(y) + "," + str(z) + ")")
                time.sleep(0.5)
                # x_d = round(hand.palm_normal.x, 5)
                # y_d = round(hand.palm_normal.y, 5)
                # z_d = round(hand.palm_normal.z, 5)
                # print("\r" + str(x_d) + ", " + str(y_d) + ", " + str(z_d)),
            pass
        elif choice == '9':
            pass
        elif choice == '0':
            # Exit
            done = True
            pass


def get_relevant_data(kernel_type, file_name, acquisitor, hand=None):
    if "finger-to-palm-distance" + "_" + kernel_type in file_name:
        data = acquisitor.get_palm_to_finger_distance_set(hand=hand, return_mode=True)
    elif "finger-angle-using-bones" + "_" + kernel_type in file_name:
        data = acquisitor.get_palm_to_finger_angle_set(hand=hand, return_mode=True)
    elif "finger-angle-and-palm-distance" + "_" + kernel_type in file_name:
        data = acquisitor.get_finger_to_palm_angle_and_distance(hand=hand, return_mode=True)
    elif "finger-between-distance" + "_" + kernel_type in file_name:
        data = acquisitor.get_distance_between_fingers_set(hand=hand, return_mode=True)
    # Add the palm vectors data
    xd, yd, zd = acquisitor.get_palm_x_y_z_dir(hand=hand)
    data.append(xd)
    data.append(yd)
    data.append(zd)
    return [data]


    pass