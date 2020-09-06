import time
from string import lower

from controller.LeapDataAcquisitor import LeapDataAcquisitor
from leapio import LeapIO as io
from leapio import Printer as printer

class LeapDataClassifier:
    def __init__(self, leap_controller, test_size=5, gesture_src="gestures_counting.txt"):
        # Checks gesture database - if does not exist --> Create default
        if io.does_file_exist(gesture_src) is False:
            io.create_gesture_database(gesture_src)
            pass
        self.leap_controller = leap_controller
        self.test_size = test_size
        self.gesture_list = io.read_col(gesture_src)
        self.acquisitor = None
        self.subject_name = None

    def initialize(self, subject_name):
        # Initialise the Acquisitor
        self.subject_name = subject_name
        self.acquisitor = LeapDataAcquisitor(leap_controller=self.leap_controller,
                                             subject_name=subject_name)

    def do_classification(self, chosen_gesture, trainer_list, cls_dict, time_dict):
        # Create time and classification dictionaries
        file_name = None
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

        # Calculate and display results summary
        for trainer in trainer_list:
            self.process_results(
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
            print("1 : " + str(X_data))
        elif "finger-angle-using-bones" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = self.acquisitor.get_palm_to_finger_angle_set(gesture_name=chosen_gesture,
                                                                  return_mode=True,
                                                                  hand=hand)
            print("2 : " + str(X_data))
        elif "finger-angle-and-palm-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = self.acquisitor.get_finger_to_palm_angle_and_distance(gesture_name=chosen_gesture,
                                                                           return_mode=True,
                                                                           hand=hand)
            print("3 : " + str(X_data))
        elif "finger-between-distance" + "_" + kernel_type in chosen_pickle_no_extension:
            X_data = self.acquisitor.get_distance_between_fingers_set(gesture_name=chosen_gesture,
                                                                      return_mode=True,
                                                                      hand=hand)
            print("4 : " + str(X_data))

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
