from datetime import time

import leapio.LeapIO as io
import leapio.Printer as printer
import controller.LeapDataAcquisitor as acquisitor
from controller.LeapDataTrainer import LeapTrainer
from string import lower


# TODO : FOCUS ON CLASSIFICATION NOW

class ClassificationMenu:
    def __init__(self, leap_controller, test_size=25, gesture_src="gesture_database.txt"):
        # Checks gesture database - if does not exist --> Create default
        if io.does_file_exist(gesture_src) is False:
            io.create_gesture_database(gesture_src)
            pass

        self.leap_controller = leap_controller
        self.test_size = test_size
        self.gesture_list = io.read_gesture_database(gesture_src)
        self.report_file = io.create_classification_report()

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

            if choice == '1':
                self.single_feature_classification()
                done = True
                pass
            elif choice == '2':
                self.multiple_feature_classification()
                done = True
                pass

    def single_feature_classification(self):
        # Show files available for classification (pickle files)
        list_data_files = io.get_data_files('.pickle')
        print("* List of Pickle Files *")
        printer.print_numbered_list(list_data_files)

        choice = raw_input("Enter the pickle file for classifier \nPickle Index  : ")
        chosen_pickle = list_data_files[int(choice) - 1]
        chosen_pickle_no_extension = chosen_pickle.rsplit(".", 1)[0]
        kernel_type = chosen_pickle_no_extension.rsplit("_", 1)[-1]

        # Show feature type and kernel type based on chosen pickle file
        print("Chosen Pickle : " + chosen_pickle)
        print("Kernel Type   : " + kernel_type + "\n")

        print("* List of Valid Gestures *")
        printer.print_numbered_list(self.gesture_list)
        choice = raw_input("Enter the Gesture Name: ")
        chosen_gesture = lower(self.gesture_list[int(choice) - 1])
        print("")

        # Call data classification functions
        trainer = LeapTrainer(classifier_name=chosen_pickle_no_extension, kernel_type=kernel_type)
        trainer.load_classifier(chosen_pickle)

        i = 0
        time_list = []
        correct_classification = 0

        while i < int(self.test_size):
            classification_res = self.classify_gesture(kernel_type=kernel_type,
                                                       chosen_pickle_no_extension=chosen_pickle_no_extension,
                                                       chosen_gesture=chosen_gesture, trainer=trainer,
                                                       time_list=time_list)

            if classification_res is True:
                correct_classification += 1

            i += 1

        # Calculate and display results summary
        self.process_results(correct_classification=correct_classification, time_list=time_list)

    def multiple_feature_classification(self):
        # Show files available for classification (pickle files)
        list_data_files = io.get_data_files('.pickle')
        print("* List of Pickle Files *")
        printer.print_numbered_list(list_data_files)

        print("* List of Valid Gestures *")
        printer.print_numbered_list(self.gesture_list)
        choice = raw_input("Enter the Gesture Name: ")
        chosen_gesture = lower(self.gesture_list[int(choice) - 1])

        # Create Leap Data Trainer for each feature type
        trainer_list = []
        for current_pickle in list_data_files:
            # Obtain pickle file name and kernel type
            current_pickle_no_extension = current_pickle.rsplit(".", 1)[0]
            kernel_type = current_pickle_no_extension.rsplit("_", 1)[-1]

            # Create a Leap Data Trainer based on obtained pickle name and kernel type
            trainer = LeapTrainer(classifier_name=current_pickle_no_extension, kernel_type=kernel_type)
            trainer.load_classifier(current_pickle)

            # Append to list of trainers
            trainer_list.append(trainer)

            print(
                        "System   :   Loaded Configuration -- Feature Type = " + current_pickle_no_extension + ", Kernel Type = " + kernel_type)

        # Classify for each feature
        for trainer in trainer_list:
            classifier_name = trainer.classifier_name
            kernel_type = trainer.kernel_type

            time_list = []
            correct_classification = 0

            # Classify up to number of iterations for ALL feature types
            i = 0
            while i < int(self.test_size):
                classification_res = self.classify_gesture(
                    kernel_type=kernel_type,
                    chosen_pickle_no_extension=classifier_name,
                    chosen_gesture=chosen_gesture,
                    trainer=trainer,
                    time_list=time_list
                )

                if classification_res is True:
                    correct_classification += 1

                i += 1

            # Calculate and display results summary
            self.process_results(correct_classification=correct_classification, time_list=time_list)

        print("")

    def classify_gesture(self, kernel_type, chosen_pickle_no_extension, chosen_gesture, trainer, time_list):
        if "finger-to-palm-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = acquisitor.get_palm_to_finger_distance_set(leap_controller=self.leap_controller,
                                                                gesture_name=chosen_gesture)
            print(X_data)
        elif "finger-angle-using-bones" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = acquisitor.get_palm_to_finger_angle_set(leap_controller=self.leap_controller)
            print(X_data)
        elif "finger-angle-and-palm-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = acquisitor.get_finger_to_palm_angle_and_distance(leap_controller=self.leap_controller)
            print(X_data)
        elif "finger-between-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = acquisitor.get_distance_between_fingers_set(leap_controller=self.leap_controller)
            print(X_data)

        # Recording timing of classification
        start_time = time.time()
        prediction = trainer.classify([X_data])
        end_time = time.time()
        time_taken = round(end_time - start_time, 7)
        time_list.append(time_taken)

        # Increment correct prediction
        if lower(prediction[0]) == chosen_gesture:
            print "------- CORRECT PREDICTION -------"
            res = True
        else:
            print("xxxxxx INCORRECT PREDICTION xxxxxx")
            res = False

        print "Feature Used : " + chosen_pickle_no_extension
        print "Prediction : " + lower(prediction[0]) + "\n"

        return res

    def process_results(self, correct_classification, time_list):
        # Calculate average time taken to perform classification algorithms between multiple test hand instances
        avg_time = (sum(time_list)) / (len(time_list))
        # Calculate average accuracy of classification algorithm between multiple test hand instances
        accuracy = round(100.0 * (float(correct_classification) / (float(self.test_size))), 2)

        summary = """FINAL RESULT
                    Correct    :    %s
                    Incorrect  :    %s
                    Result     :    %s / %s
                    Accuracy   :    %s %%
                    Avg Time   :    %s seconds\n""" % (str(correct_classification),
                                                       str(int(self.test_size) - correct_classification),
                                                       str(correct_classification),
                                                       str(self.test_size),
                                                       str(accuracy),
                                                       str(avg_time)
                                                       )

        # Print out results in summary form
        print summary
        # Save summary onto report file
        io.append_to_report(self.report_file, summary)
