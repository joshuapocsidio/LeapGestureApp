import time
from string import lower

import leapio.LeapIO as io
import leapio.Printer as printer
from controller.LeapDataAcquisitor import LeapDataAcquisitor
from controller.LeapDataTrainer import SVM_Trainer
from controller.LeapDataClassifier import LeapDataClassifier
from sklearn.preprocessing import StandardScaler


class ClassificationMenu:
    def __init__(self, leap_controller):
        self.classification_controller = LeapDataClassifier(leap_controller=leap_controller)

    def show(self):
        # Shows menu for classifying gesture data
        done = False

        while done is False:
            print("-------------------")
            print("DATA CLASSIFICATION")
            print("-------------------")
            print("(1) - Single Feature:Kernel Classification Test")
            print("(2) - Multiple Feature:Kernel Classification Test")
            print("(0) - Back")

            choice = raw_input("Your Choice: ")

            if choice != '0' and choice is not None and choice != '':
                subject_list = io.read_col("subjects.txt")
                print("------------")
                print("SUBJECT NAME")
                print("------------")
                printer.print_numbered_list(subject_list)

                subject_choice = raw_input("Choose subject name: ")
                subject_name = subject_list[int(subject_choice) - 1]
                print("")

                # Initialise the Acquisitor
                self.classification_controller.initialize(subject_name=subject_name)

            if choice == '1':
                self.single_feature_classification()
                done = True
                pass
            elif choice == '2':
                self.multiple_feature_classification()
                done = True
                pass
            elif choice == '0':
                done = True
                pass
            else:
                print("Please try again.")

    def single_feature_classification(self):
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

        # Prompt user for gesture name
        chosen_gesture = self.prompt_gesture_name()

        # Obtain subject name
        subject_name = self.classification_controller.subject_name

        # Create time and classification dictionaries
        time_dict = {}
        cls_dict = {}

        # Call data classification functions
        trainer_list = []
        trainer = SVM_Trainer(subject_name=subject_name, feature_type=chosen_pickle_no_extension,
                              kernel_type=kernel_type)
        trainer.load(chosen_pickle)
        trainer_list.append(trainer)

        # Append to dictionaries
        time_dict[trainer] = []
        cls_dict[trainer] = 0

        # Do Classification
        self.classification_controller.do_classification(
            chosen_gesture=chosen_gesture,
            trainer_list=trainer_list,
            cls_dict=cls_dict,
            time_dict=time_dict
        )

    def multiple_feature_classification(self):
        # Show files available for classification (pickle files)
        list_data_files = io.get_pickle_files()
        print("* List of Pickle Files *")
        printer.print_numbered_list(list_data_files)
        print("\n")

        # Prompt user for gesture name
        chosen_gesture = self.prompt_gesture_name()

        # Create time and classification dictionaries
        time_dict = {}
        cls_dict = {}

        # Create Leap Data Trainer for each feature type
        trainer_list = []
        for current_pickle in list_data_files:
            # Obtain pickle file name and kernel type
            current_pickle_no_extension = current_pickle.rsplit(".", 1)[0]
            kernel_type = current_pickle_no_extension.rsplit("_", 1)[-1]

            subject_name = self.classification_controller.subject_name
            # Create a Leap Data Trainer based on obtained pickle name and kernel type
            trainer = SVM_Trainer(subject_name=subject_name, feature_type=current_pickle_no_extension,
                                  kernel_type=kernel_type)
            trainer.load(current_pickle)

            # Append to list of trainers
            trainer_list.append(trainer)
            # Append to dictionaries
            time_dict[trainer] = []
            cls_dict[trainer] = 0

        self.classification_controller.do_classification(
            chosen_gesture=chosen_gesture,
            trainer_list=trainer_list,
            cls_dict=cls_dict,
            time_dict=time_dict
        )

    def prompt_gesture_name(self):
        # Prompts user for name of gesture
        done = False
        gesture_list = self.classification_controller.gesture_list

        while done is False:
            print("* List of Valid Gestures *")
            printer.print_numbered_list(gesture_list)
            choice = raw_input("Enter the Gesture Name: ")
            gesture_name = lower(gesture_list[int(choice) - 1])
            print("\n")

            if gesture_name is not None or gesture_name is not "":
                done = True
                return gesture_name
            else:
                print("Please try again")
