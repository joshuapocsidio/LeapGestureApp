import time
from string import lower

import leapio.LeapIO as io
import leapio.Printer as printer
from controller.LeapDataAcquisitor import LeapDataAcquisitor
from controller.LeapDataTrainer import SVM_Trainer


class ClassificationMenu:
    def __init__(self, leap_controller, test_size=5, gesture_src="gestures.txt"):
        # Checks gesture database - if does not exist --> Create default
        if io.does_file_exist(gesture_src) is False:
            io.create_gesture_database(gesture_src)
            pass

        self.leap_controller = leap_controller
        self.test_size = test_size
        self.gesture_list = io.read_col(gesture_src)
        self.acquisitor = None
        self.subject_name = None

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
                self.subject_name = subject_list[int(subject_choice) - 1]
                print("")

                # Initialise the Acquisitor
                self.acquisitor = LeapDataAcquisitor(leap_controller=self.leap_controller,
                                                     subject_name=self.subject_name)

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
                print( "Please try again.")

    def single_feature_classification(self):
        # Show files available for classification (pickle files)
        list_data_files = io.get_data_files('.pickle')
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

        # Call data classification functions
        trainer = SVM_Trainer(feature_type=chosen_pickle_no_extension, kernel_type=kernel_type)
        trainer.load(chosen_pickle)

        i = 0
        time_list = []
        correct_classification = 0

        while i < int(self.test_size):
            classification_res = self.classify_gesture(kernel_type=kernel_type,
                                                       chosen_pickle_no_extension=chosen_pickle_no_extension,
                                                       chosen_gesture=chosen_gesture, trainer=trainer,
                                                       time_list=time_list
                                                       )

            if classification_res is True:
                correct_classification += 1

            i += 1

        # Calculate and display results summary
        self.process_results(
            gesture_name=chosen_gesture,
            correct_classification=correct_classification,
            time_list=time_list
        )

    def multiple_feature_classification(self):
        # Show files available for classification (pickle files)
        list_data_files = io.get_data_files('.pickle')
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

            # Create a Leap Data Trainer based on obtained pickle name and kernel type
            trainer = SVM_Trainer(feature_type=current_pickle_no_extension, kernel_type=kernel_type)
            trainer.load(current_pickle)

            # Append to list of trainers
            trainer_list.append(trainer)
            # Append to dictionaries
            time_dict[trainer] = []
            cls_dict[trainer] = 0

            print(
                    "System   :   Loaded Configuration -- Feature Type = " + current_pickle_no_extension + ", Kernel Type = " + kernel_type)

        num_trainers = len(trainer_list)

        i = 0
        while i < int(self.test_size):
            hand = self.acquisitor.get_hand_data()
            for trainer in trainer_list:
                classification_res = self.classify_gesture(
                    kernel_type=trainer.kernel_type,
                    chosen_pickle_no_extension=trainer.feature_type,
                    chosen_gesture=chosen_gesture,
                    trainer=trainer,
                    time_list=time_dict[trainer],
                    hand=hand
                )

                if classification_res is True:
                    cls_dict[trainer] += 1

            i += 1

        file_name = None
        # Calculate and display results summary of all trainers
        for trainer in trainer_list:
            file_name = self.process_results(
                gesture_name=chosen_gesture,
                file_name=file_name,
                trainer=trainer,
                correct_classification=cls_dict[trainer],
                time_list=time_dict[trainer]
            )

        print("")

    def classify_gesture(self, kernel_type, chosen_pickle_no_extension, chosen_gesture, trainer, time_list, hand):
        X_data = []
        if "finger-to-palm-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = self.acquisitor.get_palm_to_finger_distance_set(gesture_name=chosen_gesture,
                                                                     return_mode=True,
                                                                     hand=hand)
            print(X_data)
        elif "finger-angle-using-bones" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = self.acquisitor.get_palm_to_finger_angle_set(gesture_name=chosen_gesture,
                                                                  return_mode=True,
                                                                  hand=hand)
            print(X_data)
        elif "finger-angle-and-palm-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = self.acquisitor.get_finger_to_palm_angle_and_distance(gesture_name=chosen_gesture,
                                                                           return_mode=True,
                                                                           hand=hand)
            print(X_data)
        elif "finger-between-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = self.acquisitor.get_distance_between_fingers_set(gesture_name=chosen_gesture,
                                                                      return_mode=True,
                                                                      hand=hand)
            print(X_data)

        # Recording timing of classification
        start_time = time.time()
        prediction = trainer.classify([X_data])
        end_time = time.time()
        time_taken = round(end_time - start_time, 7)
        time_list.append(time_taken)

        # Increment correct prediction
        if (prediction[0]) == chosen_gesture:
            print("------- CORRECT PREDICTION -------")
            res = True
        else:
            print("xxxxxx INCORRECT PREDICTION xxxxxx")
            res = False

        print("Feature Used : " + chosen_pickle_no_extension)
        print("Prediction : " + lower(prediction[0]) + "\n")

        return res

    def process_results(self, trainer, correct_classification, time_list, file_name, gesture_name):
        # Calculate average time taken to perform classification algorithms between multiple test hand instances
        avg_time = (sum(time_list)) / (len(time_list))
        # Calculate average accuracy of classification algorithm between multiple test hand instances
        accuracy = round(100.0 * (float(correct_classification) / (float(self.test_size))), 2)

        summary = """____________________________________________________________________________________________________________________________________________________________________________________________________
        Classifier :    %s (%s)
        Gesture    :    %s
        Correct    :    %s
        Incorrect  :    %s
        Result     :    %s / %s
        Accuracy   :    %s %%
        Avg Time   :    %s seconds\n""" % (str(trainer.feature_type),
                                           lower(str(trainer.kernel_type)),
                                           gesture_name,
                                           str(correct_classification),
                                           str(int(self.test_size) - correct_classification),
                                           str(correct_classification),
                                           str(self.test_size),
                                           str(accuracy),
                                           str(avg_time)
                                           )

        # Print out results in summary form
        print(summary)
        # Save summary onto report file
        return io.save_report(file_name=file_name, subject_name=self.subject_name, report_header='classification',
                              line=summary)

    def prompt_gesture_name(self, gesture_src='gestures.txt'):
        # Prompts user for name of gesture
        done = False

        while done is False:
            print("* List of Valid Gestures *")
            printer.print_numbered_list(self.gesture_list)
            choice = raw_input("Enter the Gesture Name: ")
            gesture_name = lower(self.gesture_list[int(choice) - 1])
            print("\n")

            if gesture_name is not None or gesture_name is not "":
                done = True
                return gesture_name
            else:
                print("Please try again")
