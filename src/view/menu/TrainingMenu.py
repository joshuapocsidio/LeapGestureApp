from string import strip

import leapio.LeapIO as io
from controller import DataOptimizer
from leapio import Printer


class TrainingMenu:
    def __init__(self):
        self.activation = None
        self.optimizer = None
        self.classifier_type = None
        self.kernel_type = None
        self.params = []
        pass

    def show(self):
        # Shows menu for training gesture data
        done = False
        while done is False:
            self.kernel_type = None
            self.classifier_type = None

            print("-------------")
            print("DATA TRAINING")
            print("-------------")
            print("(1) - Support Vector Machine")
            print("(2) - Multilayer Perceptron (Neural Network)")
            print("(3) - Decision Trees")
            print("(4) - Create New Sets")
            print("(0) - Back")

            choice = raw_input("Your Choice: ")
            if choice == '1':
                self.classifier_type = 'svm'
                self.prompt_training_mode()
                pass
            elif choice == '2':
                self.classifier_type = 'nn'
                self.prompt_training_mode()
                pass
            elif choice == '3':
                self.classifier_type = 'dt'
                self.prompt_training_mode()
                pass
            elif choice == '4':
                self.prompt_create_sets()
                pass
            elif choice == '0':
                done = True
                pass
            else:
                print("Please try again.")
                pass

    def prompt_create_sets(self):
        # Shows menu for creating new data sets
        done = False
        while done is False:
            print("----------------")
            print("DATA COMBINATION")
            print("----------------")
            print("(1) - Combine Gesture Set with Individual Subject")
            print("(2) - Combine Subjects with Individual Gesture Set")
            print("(3) - Combine ALL Gesture Set with All Subjects")
            print("(0) - Back")

            choice = raw_input("Your Choice: ")
            if choice == '1':
                self.combine_gestures_separate_subjects()
                pass
            elif choice == '2':
                self.combine_subjects_separate_gestures()
                pass
            elif choice == '3':
                self.combine_subjects_combine_gestures()
                pass
            elif choice == '0':
                done = True
                pass
            else:
                print("Please try again.")

        pass


    def prompt_training_mode(self):
        done = False
        while done is False:
            print("-------------")
            print("TRAINING MODE")
            print("-------------")
            print("(1) - Single Training")
            print("(2) - Multi Training")
            print("(3) - Single Combined Training")
            print("(4) - Multi Combined Training")
            print("(0) - Back")

            choice = raw_input("Your Choice: ")

            if choice == '1':
                self.single_training()
                done = True
                pass
            elif choice == '2':
                self.multi_training()
                done = True
                pass
            elif choice == '3':
                self.single_training(combined=True)
                done = True
                pass
            elif choice == '4':
                self.multi_training(combined=True)
                done = True
                pass
            elif choice == '0':
                done = True
                pass
            else:
                print("Please try again.")
                pass

    def single_training(self, combined=False):
        data_files = io.get_data_files(combined=combined)

        print("")
        print("~ ~ ~ ~ ~ ~ ~ ~ LIST OF DATA SOURCE ~ ~ ~ ~ ~ ~ ~ ~")
        Printer.print_numbered_list(data_files)
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

        choice = raw_input("Enter the data set to train from: ")
        data_file = data_files[int(choice) - 1]
        print("Chosen File : " + data_file)
        print("")


        if combined is False:
            subject_name = data_file.rsplit("(", 1)[1].rsplit(")")[0]
            feature_type = strip(data_file.rsplit(")")[1].rsplit(".")[0].rsplit("--")[1])
        else:
            title = data_file.split("--")[0]
            if "COMBINED FULL" in title:
                raw_input("FULL")
                subject_name = "All Subjects"
                gesture_set = "All Gestures"
                feature_type = strip(data_file.split(".")[0].rsplit("--")[1])
            elif "COMBINED GESTURES" in title:
                raw_input("GE")
                subject_name = data_file.split("(")[1].split(")")[0]
                gesture_set = "All Gestures"
                feature_type = strip(data_file.rsplit(")")[1].rsplit(".")[0])
                pass
            elif "COMBINED SUBJECTS" in title:
                raw_input("SU")
                subject_name = "All Subjects"
                gesture_set = data_file.split("(")[1].split(")")[0]
                feature_type = strip(data_file.rsplit(")")[1].rsplit(".")[0])
                pass

        file_name = None
        if self.classifier_type == 'svm':
            kernel_list = io.read_col("kernels.txt")
            print("* List of Kernels *")
            Printer.print_numbered_list(kernel_list)

            choice = raw_input("Enter the kernel to use for training: ")

            kernel_type = kernel_list[int(choice) - 1]
            self.params = []
            self.params.append(kernel_type)

            print("Chosen Kernel : " + kernel_type)
            print("")

            training_summary = self.train_auto(csv_file=data_file, subject_name=subject_name, feature_type=feature_type)
            file_name = io.save_report(file_name=file_name, subject_name=subject_name, report_header='training',
                                       line=training_summary, classifier_type=self.classifier_type)
        elif self.classifier_type == 'nn':
            activations = ['relu', 'logistic']
            optimizers = ['adam', 'sgd']
            for activation in activations:
                for optimizer in optimizers:
                    # Reset params before populating
                    self.params = []
                    self.params.append(activation)
                    self.params.append(optimizer)

                    training_summary = self.train_auto(csv_file=data_file, subject_name=subject_name,
                                                       feature_type=feature_type)
                    file_name = io.save_report(file_name=file_name, subject_name=subject_name, report_header='training',
                                               line=training_summary, classifier_type=self.classifier_type)
        elif self.classifier_type == 'dt':
            training_summary = self.train_auto(csv_file=data_file, subject_name=subject_name, feature_type=feature_type)
            file_name = io.save_report(file_name=file_name, subject_name=subject_name, report_header='training',
                                       line=training_summary, classifier_type=self.classifier_type)
        pass

    def multi_training(self, combined=False):
        data_files = io.get_data_files(combined=combined)
        kernel_list = io.read_col("kernels.txt")
        file_name = None

        print("")
        "* List of Data Files to Train *"
        Printer.print_numbered_list(data_files)
        print("")

        # SVM Multi Training
        if self.classifier_type == 'svm':
            "* List of Kernels for Training *"
            Printer.print_numbered_list(kernel_list)
            print("")

            for data_file in data_files:
                subject_name = data_file.rsplit("(", 1)[1].rsplit(")")[0]
                gesture_set = strip(data_file.rsplit(")")[1].rsplit(".")[0].rsplit("--")[0])
                feature_type = strip(data_file.rsplit(")")[1].rsplit(".")[0].rsplit("--")[1])
                for kernel in kernel_list:
                    # Reset params before populating
                    self.params = []
                    self.params.append(kernel)

                    training_summary = self.train_auto(csv_file=data_file, subject_name=subject_name,
                                                       feature_type=feature_type)
                    file_name = io.save_report(file_name=file_name, subject_name=subject_name, report_header='training',
                                               line=training_summary, classifier_type=self.classifier_type)
                    pass
            pass
        # NN Multi Training
        elif self.classifier_type == 'nn':
            activations = ['relu', 'logistic']
            optimizers = ['adam', 'sgd']

            for data_file in data_files:
                subject_name = data_file.rsplit("(", 1)[1].rsplit(")")[0]
                gesture_set = strip(data_file.rsplit(")")[1].rsplit(".")[0].rsplit("--")[0])
                feature_type = strip(data_file.rsplit(")")[1].rsplit(".")[0].rsplit("--")[1])

                for activation in activations:
                    for optimizer in optimizers:
                        # Reset params before populating
                        self.params = []
                        self.params.append(activation)
                        self.params.append(optimizer)

                        training_summary = self.train_auto(csv_file=data_file, subject_name=subject_name,
                                                           feature_type=feature_type)
                        file_name = io.save_report(file_name=file_name, subject_name=subject_name,
                                                   report_header='training',
                                                   line=training_summary, classifier_type=self.classifier_type)
            pass

    def train_auto(self, csv_file, subject_name, feature_type):
        results = DataOptimizer.obtain_optimal_classifier(
            csv_file_name=csv_file,
            subject_name=subject_name,
            feature_type=feature_type,
            classifier_type=self.classifier_type,
            params=self.params
        )

        optimal_classifier = results[0]
        training_summary = results[1]

        optimal_classifier.save_classifier()

        return training_summary

    def train_manual(self, csv_file, subject_name, feature_type):

        results = DataOptimizer.obtain_optimal_classifier(
            csv_file_name=csv_file,
            subject_name=subject_name,
            feature_type=feature_type,
            params=self.params,
            classifier_type=self.classifier_type
        )

        optimal_classifier = results[0]
        training_summary = results[1]

        save_choice = raw_input("Would you like to save this classifier? (y/n) :")
        valid_choice = False

        while valid_choice is False:
            if save_choice == 'y':
                optimal_classifier.save_classifier()
                file_name = io.create_training_report()
                io.append_to_report(file_name=file_name, line=training_summary)
                # Save to report summary file
                valid_choice = True
            elif save_choice != 'n':
                print("Please try again.")
        pass

    def combine_gestures_separate_subjects(self):
        # Get parameters
        data_files, feature_set_list, _, subject_name_list = self.get_params()

        # Grouping Stage
        group_by_subject = []
        i = 0

        # Group by Subject Name
        for subject_name in subject_name_list:
            subject_group = []
            j = 0

            # Group by Feature Set
            for feature_set in feature_set_list:
                subject_feature_group = []

                # Iterate through data files to find matching
                for data_file in data_files:
                    feature_set_check = data_file.split("--")[1].split(".")[0]
                    subject_name_check = data_file.split("(")[1].split(")")[0]

                    # Only append to group if matches subject and feature
                    if feature_set == feature_set_check and subject_name == subject_name_check:
                        subject_feature_group.append(data_file)

                if len(subject_feature_group) > 0:
                    subject_group.append(subject_feature_group)
                j += 1

            # Only Append to group if not an empty group
            if len(subject_group) > 0:
                group_by_subject.append(subject_group)
            i += 1

        for group in group_by_subject:
            for file_item in group:
                # All items in this group should have same subject and same content
                subject = file_item[0].split("(")[1].split(")")[0]
                feature_set = file_item[0].split("--")[1].split(".")[0]

                # Construct file name
                file_name = io.com_dir + "COMBINED GESTURES--(" + subject + ") " + feature_set + ".csv"

                # Create the file
                self.file_creation(group=file_item, file_name=file_name)
        pass

    def combine_subjects_separate_gestures(self):
        # Get parameters
        data_files, feature_set_list, gesture_set_list, _ = self.get_params()

        # Grouping Stage
        group_by_gesture = []
        i = 0

        # Group by Gesture SetName
        for gesture_set in gesture_set_list:
            gesture_group = []
            j = 0

            # Group by Feature Set
            for feature_set in feature_set_list:
                gesture_feature_group = []

                # Iterate through data files to find matching
                for data_file in data_files:
                    feature_set_check = data_file.split("--")[1].split(".")[0]
                    gesture_set_check = strip(data_file.split("--")[0].split(")")[1])

                    # Only append to group if matches subject and feature
                    if feature_set == feature_set_check and gesture_set == gesture_set_check:
                        gesture_feature_group.append(data_file)

                if len(gesture_feature_group) > 0:
                    gesture_group.append(gesture_feature_group)
                j += 1

            # Only Append to group if not an empty group
            if len(gesture_group) > 0:
                group_by_gesture.append(gesture_group)
            i += 1

        for group in group_by_gesture:
            for file_item in group:
                # All items in this group should have same subject and same content
                gesture_set = strip(file_item[0].split("--")[0].split(")")[1])
                feature_set = file_item[0].split("--")[1].split(".")[0]

                # Construct file name
                file_name = io.com_dir + "COMBINED SUBJECTS--(" + gesture_set + ") " + feature_set + ".csv"

                # Create the file
                self.file_creation(group=file_item, file_name=file_name)
        pass


    def combine_subjects_combine_gestures(self):
        # Get parameters
        data_files, feature_set_list, _, _ = self.get_params()

        # Grouping Stage
        full_combined_group = []
        i = 0
        # Group by Feature Set
        for feature_set in feature_set_list:
            # Iterate through data files to find matching
            for data_file in data_files:
                feature_set_check = data_file.split("--")[1].split(".")[0]

                # Only append to group if matches subject and feature
                if feature_set == feature_set_check:
                    full_combined_group.append(data_file)
            i += 1

        for file_item in full_combined_group:
            # All items in this group should have same subject and same content
            feature_set = file_item.split("--")[1].split(".")[0]

            # Construct file name
            file_name = io.com_dir + "COMBINED FULL--" + feature_set + ".csv"

            # Create the file
            self.file_creation(single_item=file_item, file_name=file_name, single=True)

        pass

    def get_params(self):
        data_files = io.get_data_files()
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

        return data_files, feature_set_list, gesture_set_list, subject_name_list

    def display_groups(self, full_group):
        print("** FINAL GROUPS ** ")
        for group in full_group:
            for sub in group:
                Printer.print_numbered_list(sub)
                print("--")

    def file_creation(self, file_name, group=None, single_item=None, single=False):
        if single is True and single_item is not None:
            # Get the content and labels from the file
            content = io.read_all(single_item)
            labels = strip(str(content[0])).split(",")
            del content[0]
            content = "".join(content)

            if io.does_file_exist(file_name=file_name) is False:
                io.create_data_file(file_name=file_name, labels=labels)
            else:
                io.append_to_file(file_name=file_name, lines=strip(str(content)))
        else:
            for file_item in group:
                # Get the content and labels from the file
                content = io.read_all(file_item)
                labels = strip(str(content[0])).split(",")
                del content[0]
                content = "".join(content)

                if io.does_file_exist(file_name=file_name) is False:
                    io.create_data_file(file_name=file_name, labels=labels)
                else:
                    io.append_to_file(file_name=file_name, lines=strip(str(content)))