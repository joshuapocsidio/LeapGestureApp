import time
from string import lower, strip

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
            print("(1) - Real Time Classification Test")
            print("(2) - Unseen Data Classification Test")
            print("(0) - Back")

            choice = raw_input("Your Choice: ")

            if choice == '1':
                self.real_time_classification_test()
                pass
            elif choice == '2':
                self.unseen_data_classification_test()
                pass
            elif choice == '0':
                pass

    def unseen_data_classification_test(self):
        done = False
        while done is False:
            print("--------------------------")
            print("UNSEEN DATA CLASSIFICATION")
            print("--------------------------")
            print("(1) - Single Personalized Test")
            print("(2) - Single Non-Personalized Test")
            print("(3) - Multi Personalized Test")
            print("(4) - Multi Non-Personalized Test")
            print("(0) - Back")

            choice = raw_input("Your Choice: ")

            file_name = None
            unseen_data_files, pickle_files, _, _, subject_name_list = self.get_params()
            if choice == '1':
                choice_subject_name = self.prompt_subject_name()

                # Obtain all trained data for this test subject
                pickle_file_list = []
                for pickle_file in pickle_files:
                    subject_name = pickle_file.rsplit("(", 1)[1].rsplit(")")[0]

                    # Want personalized data -- test with own unseen data
                    if lower(subject_name) == lower(choice_subject_name):
                        # Do Classification Test
                        print(pickle_file)
                        pickle_file_list.append(pickle_file)
                        pass

                # Get Own Unseen Data
                for unseen_data in unseen_data_files:
                    comparison_subject_name = unseen_data.split("(")[1].split(")")[0]
                    unseen_feature_set = unseen_data.split("--")[1].split(".csv")[0]
                    unseen_subject_name = unseen_data.split("(")[1].split(")")[0]
                    unseen_gesture_set = strip(unseen_data.split("--")[0].split(")")[1])
                    for pickle_file in pickle_file_list:
                        # Get File Path without folders
                        file_path = pickle_file.split("\\")[-1]
                        # Get parameters
                        classifier_type = file_path.split(" ")[0]
                        gesture_set = strip(file_path.split("--")[0].split(")")[1])
                        feature_set = file_path.split("--")[1].split(".pickle")[0].split("_")[0]

                        # Only do classification if same type of feature set ---> Otherwise will not work at all
                        if feature_set == unseen_feature_set and \
                                unseen_subject_name == choice_subject_name and \
                                unseen_gesture_set == gesture_set:
                            print("UNSEEN : " + unseen_data)
                            # Do classification from csv
                            file_name = self.classification_controller.do_classification_from_csv(
                                pickle_file=pickle_file,
                                test_subject=choice_subject_name,
                                comparison_subject=comparison_subject_name,
                                classifier_type=classifier_type,
                                gesture_set=gesture_set,
                                feature_set=feature_set,
                                unseen_data=unseen_data,
                                file_name=file_name
                            )

            elif choice == '2':
                choice_subject_name = self.prompt_subject_name()

                # Obtain all trained data for this test subject
                pickle_file_list = []
                for pickle_file in pickle_files:
                    subject_name = pickle_file.rsplit("(", 1)[1].rsplit(")")[0]

                    # Want personalized data -- test with own unseen data
                    if lower(subject_name) == lower(choice_subject_name):
                        # Do Classification Test
                        print(pickle_file)
                        pickle_file_list.append(pickle_file)
                        pass

                # Get Others' Unseen Data
                for unseen_data in unseen_data_files:
                    comparison_subject_name = unseen_data.split("(")[1].split(")")[0]
                    unseen_feature_set = unseen_data.split("--")[1].split(".csv")[0]
                    for pickle_file in pickle_file_list:
                        # Get File Path without folders
                        file_path = pickle_file.split("\\")[-1]
                        # Get parameters
                        classifier_type = file_path.split(" ")[0]
                        gesture_set = strip(file_path.split("--")[0].split(")")[1])
                        feature_set = file_path.split("--")[1].split(".pickle")[0].split("_")[0]

                        # Only do classification if same type of feature set ---> Otherwise will not work at all
                        if feature_set == unseen_feature_set:
                            # Do classification from csv
                            self.classification_controller.do_classification_from_csv(
                                pickle_file=pickle_file,
                                test_subject=choice_subject_name,
                                comparison_subject=comparison_subject_name,
                                classifier_type=classifier_type,
                                gesture_set=gesture_set,
                                feature_set=feature_set,
                                unseen_data=unseen_data,
                                file_name=file_name
                            )

            elif choice == '3':
                for subject_name in subject_name_list:
                    for pickle_file in pickle_files:
                        pickle_subject_name = pickle_file.rsplit("(", 1)[1].rsplit(")")[0]

                        if lower(subject_name) == lower(pickle_subject_name):
                            # Do Classification Test
                            pass

            elif choice == '4':
                for subject_name in subject_name_list:
                    for pickle_file in pickle_files:
                        pickle_subject_name = pickle_file.rsplit("(", 1)[1].rsplit(")")[0]

                        if lower(subject_name) != lower(pickle_subject_name):
                            # Do Classification Test
                            pass

            elif choice == '0':
                done = True
                pass
        pass

    def real_time_classification_test(self):
        # Shows menu for classifying gesture data
        done = False

        while done is False:
            print("------------------------")
            print("REAL TIME CLASSIFICATION")
            print("------------------------")
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

    def prompt_subject_name(self):
        done = False
        while done is False:
            print("~ ~ ~ ~ ~ ~ ~ ~ SUBJECT NAMES ~ ~ ~ ~ ~ ~ ~ ~")
            subjects = io.read_col('subjects.txt')
            printer.print_numbered_list(subjects)
            print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

            choice = raw_input("Enter the subject name to train from: ")

            if int(choice) > len(subjects) or int(choice) < 1:
                print("Please try again.")
            else:
                subject_name = subjects[int(choice) - 1]
                print("Chosen Name : " + subject_name)
                print("")
                return subject_name

    def get_params(self):
        pickle_files = io.get_pickle_files()
        unseen_data_files = io.get_data_files(directory=io.uns_dir)
        feature_set_list = [
            'finger-angle-and-palm-distance',
            'finger-angle-using-bones',
            'finger-between-distance',
            'finger-to-palm-distance',
        ]
        gesture_set_list = [
            'COUNTING GESTURES',
            'STATUS GESTURES',
        ]
        subject_name_list = io.read_col("subjects.txt")


        return unseen_data_files, pickle_files, feature_set_list, gesture_set_list, subject_name_list