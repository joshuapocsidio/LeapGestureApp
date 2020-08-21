from datetime import time

import leapio.LeapIO as io
import leapio.Printer as printer
import controller.LeapDataAcquisitor as acquisitor
from controller.LeapDataTrainer import LeapTrainer
from string import lower

# TODO : FOCUS ON CLASSIFICATION NOW
def show(leap_controller, test_size=25):
    # Shows menu for classifying gesture data
    done = False

    while done is False:
        print("-------------------")
        print("DATA CLASSIFICATION")
        print("-------------------")

        # First - Show files available for classification (pickle files)
        list_data_files =  io.get_data_files('.pickle')
        printer.print_numbered_list(list_data_files)

        choice = raw_input("Enter the pickle file for classifier \nPickle Index : ")
        chosen_pickle = list_data_files[int(choice) - 1]
        chosen_pickle_no_extension = chosen_pickle.rsplit(".", 1)[0]
        kernel_type = chosen_pickle_no_extension.rsplit("_", 1)[-1]

        # Second - Show feature type and kernel type based on chosen pickle file
        print("Chosen Pickle : " + chosen_pickle)
        print("Kernel Type   : " + kernel_type)

        # Third - Prompt user for gesture name and check if valid gesture
        gesture_name = raw_input("Enter the Gesture Name: ")
        gesture_name = lower(gesture_name)

        gesture_database = 'gesture_database.txt'
        if io.does_file_exist(gesture_database) is False:
            io.create_gesture_database(gesture_database)
            pass

        valid_gesture = False
        i = 0
        gesture_list = io.read_gesture_database(gesture_database)
        while valid_gesture is False:
            current_gesture = gesture_list[i]
            if current_gesture == gesture_name:
                valid_gesture = True
                pass

        # Fourth - Call data classification functions
        trainer = LeapTrainer(classifier_name=chosen_pickle_no_extension, kernel_type=kernel_type)
        trainer.load_classifier(chosen_pickle)

        j = 0
        time_list = []
        correct_classification = 0
        incorrect_classification = 0

        while i < int(test_size):
            if "finger-to-palm-distance" + "_" + kernel_type in chosen_pickle_no_extension:
                X_data = acquisitor.get_palm_to_finger_distance_set(leap_controller=leap_controller)
                print(X_data)
            elif chosen_pickle_no_extension == "finger-angle-using-bones" + "_" + kernel_type:
                X_data = acquisitor.get_palm_to_finger_angle_set(leap_controller=leap_controller)
                print(X_data)
            elif chosen_pickle_no_extension == "finger-angle-and-palm-distance" + "_" + kernel_type:
                X_data = acquisitor.get_finger_to_palm_angle_and_distance(leap_controller=leap_controller)
                print(X_data)
            elif chosen_pickle_no_extension == "finger-between-distance" + "_" + kernel_type:
                X_data = acquisitor.get_distance_between_fingers_set(leap_controller=leap_controller)
                print(X_data)

            start_time = time.time()
            prediction = trainer.classify([X_data])
            end_time = time.time()
            time_taken = round(end_time - start_time, 7)
            time_list.append(time_taken)
            # Increment correct prediction
            if lower(prediction[0]) == gesture_name:
                print "------ CORRECT PREDICTION ------"
                correct_classification += 1
            else:
                incorrect_classification += 1

            i += 1

        avg_time = (sum(time_list))/(len(time_list))
        accuracy = round(100.0 * (float(correct_classification) / (float(test_size))), 2)

        # Display Final Result
        print "FINAL RESULT"
        print "Correct    :    " + str(correct_classification)
        print "Incorrect  :    " + str(int(test_size) - correct_classification)
        print "Result     :    " + str(correct_classification) + "/" + str(test_size)
        print "Accuracy   :    " + str(accuracy) + "%"
        print "Avg Time   :    " + str(avg_time) + " seconds\n"