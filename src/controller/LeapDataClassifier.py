import time
from string import lower

from controller.LeapDataAcquisitor import LeapDataAcquisitor
from leapio import LeapIO as io
from controller.LeapDataTrainer import NN_Trainer, SVM_Trainer, DT_Trainer
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

    def do_classification_from_csv(self, pickle_file, test_subject, comparison_subject, classifier_type, gesture_set,
                                   feature_set, unseen_data, file_name, ):
        self.initialize(subject_name=test_subject)

        X_data_set, y_data_set = self.acquisitor.acquire_data_from_csv(csv_file=unseen_data)
        trainer = None

        if lower(classifier_type) == 'nn':
            # Get set hyper parameters
            activation = pickle_file.split(".")[0].split("--")[1].split("_")[1]
            # Get NN Trainer
            trainer = NN_Trainer(subject_name=test_subject, feature_type=feature_set, activation=activation,
                                 gesture_set=gesture_set)
            trainer.load(pickle_name=pickle_file)
            pass
        elif lower(classifier_type) == 'svm':
            # Get set hyper parameters
            kernel_type = pickle_file.split(".")[0].split("--")[1].split("_")[1]
            # Get SVM Trainer
            trainer = SVM_Trainer(subject_name=test_subject, feature_type=feature_set, kernel_type=kernel_type,
                                  gesture_set=gesture_set)
            trainer.load(pickle_name=pickle_file)
        elif lower(classifier_type) == 'dt':
            # Get set hyper parameters
            criterion_type = pickle_file.split(".")[0].split("--")[1].split("_")[1]
            # Get NN Trainer
            trainer = DT_Trainer(subject_name=test_subject, feature_type=feature_set, criterion_type=criterion_type,
                                 gesture_set=gesture_set)
            trainer.load(pickle_name=pickle_file)

        # Create time and classification lists
        time_list = []

        i = 0
        correct_predictions = 0
        for X_data in X_data_set:
            y_data = y_data_set[i]

            # Recording timing of classification
            start_time = time.time()
            prediction = trainer.classify([X_data])
            end_time = time.time()
            time_taken = round(end_time - start_time, 7)
            time_list.append(time_taken)

            if prediction == y_data:
                correct_predictions += 1
                pass
            i += 1

        file_name = self.process_modified_test_results(
            classifier_type=classifier_type,
            test_subject=test_subject,
            correct_classification=correct_predictions,
            time_list=time_list,
            gesture_set=gesture_set,
            feature_set=feature_set,
            file_name=file_name,
            comparison_subject=comparison_subject,
            file_path=pickle_file,
            unseen_data=unseen_data,
            trainer=trainer
        )

        return file_name

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

        # Add the palm vectors data
        xd, yd, zd = self.acquisitor.get_palm_x_y_z_dir(hand=hand)
        X_data.append(xd)
        X_data.append(yd)
        X_data.append(zd)

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

    def process_modified_test_results(self, comparison_subject, test_subject, classifier_type, correct_classification,
                                      time_list, trainer,
                                      gesture_set, feature_set, file_name, file_path, unseen_data,
                                      verbose=False):
        # Calculate average time taken to perform classification algorithms between multiple test hand instances
        avg_time = (sum(time_list)) / (len(time_list))
        # Calculate average accuracy of classification algorithm between multiple test hand instances
        accuracy = round(100.0 * (float(correct_classification) / (float(len(time_list)))), 2)

        train_accuracy = round(trainer.training_acc * 100.0, 3)

        # Get pickle file name without folders
        pickle_file = file_path.split("\\")[-1].split(".")[0]
        unseen_data = unseen_data.split("\\")[-1].split(".")[0]
        if test_subject == comparison_subject:
            title = "PERSONALIZED TEST"
        else:
            title = "NON-PERSONALIZED TEST"

        summary = """

__________________________________________________________________________________________________
Test Subject Pickle    : %s 
Unseen Subject Data    : %s
__________________________________________________________________________________________________
        %s 
--------------------------------------------------------------------------------------------------
        Subject        :    %s
        Unseen Subject :    %s
        Feature        :    %s
        Gesture Set    :    %s
        Correct        :    %s
        Incorrect      :    %s
        Result         :    %s / %s
        Avg Time       :    %s seconds
        
        TRAINING 
        Accuracy       :    %s %%
        
        TESTING
        Accuracy       :    %s %%
        
        \n""" % (pickle_file,
                 unseen_data,
                 title,
                 test_subject,
                 comparison_subject,
                 feature_set,
                 gesture_set,
                 str(correct_classification),
                 str(len(time_list) - correct_classification),
                 str(correct_classification),
                 str(len(time_list)),
                 str(avg_time),
                 str(train_accuracy),
                 str(accuracy),
                 )

        # Print out results in summary form
        if verbose is True:
            print(summary)
            pass
        # Save summary onto report file
        return io.save_report(subject_name=self.subject_name, gesture_set=gesture_set, feature_set=feature_set,
                              report_header='classification', classifier_type=classifier_type, line=summary,
                              file_name=file_name)

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
