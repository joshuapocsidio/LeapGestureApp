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
            elif choice == '0':
                done = True
                pass
            else:
                print("Please try again.")
                pass

    def single_training(self):
        data_files = io.get_data_files('.csv')

        print("")
        print("~ ~ ~ ~ ~ ~ ~ ~ LIST OF DATA SOURCE ~ ~ ~ ~ ~ ~ ~ ~")
        Printer.print_numbered_list(data_files)
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

        choice = raw_input("Enter the data set to train from: ")
        csv_file = data_files[int(choice) - 1]
        print("Chosen File : " + csv_file)
        print("")

        if self.classifier_type == 'svm':
            kernel_list = io.read_col("kernels.txt")
            print("* List of Kernels *")
            Printer.print_numbered_list(kernel_list)
            choice = raw_input("Enter the kernel to use for training: ")
            self.kernel_type = kernel_list[int(choice) - 1]
            print("Chosen Kernel : " + self.kernel_type)
            print("")

        self.train_auto(csv_file=csv_file)
        pass

    def multi_training(self):
        data_files = io.get_data_files('.csv')
        kernel_list = io.read_col("kernels.txt")

        print("")
        "* List of Data Files to Train *"
        Printer.print_numbered_list(data_files)
        print("")

        if self.classifier_type == 'svm':
            "* List of Kernels for Training *"
            Printer.print_numbered_list(kernel_list)
            print("")

        file_name = None
        # SVM Multi Training
        if self.classifier_type == 'svm':
            for data_file in data_files:
                subject_name = data_file.rsplit("(", 1)[1].rsplit(")")[0]
                feature_type = strip(data_file.rsplit(")")[1].rsplit(".")[0])
                for kernel in kernel_list:
                    self.kernel_type = kernel
                    training_summary = self.train_auto(csv_file=data_file, subject_name=subject_name, feature_type=feature_type)
                    file_name = io.save_report(file_name=file_name, subject_name=subject_name, report_header='training',
                                               line=training_summary)
                    pass
            pass
        # NN Multi Training
        elif self.classifier_type == 'nn':
            activations = ['relu', 'logistic']
            optimizers = ['adam', 'sgd']
            for data_file in data_files:
                subject_name = data_file.rsplit("(", 1)[1].rsplit(")")[0]
                feature_type = strip(data_file.rsplit(")")[1].rsplit(".")[0])

                for activation in activations:
                    self.activation = activation
                    for optimizer in optimizers:
                        self.optimizer = optimizer
                        training_summary = self.train_auto(csv_file=data_file, subject_name=subject_name, feature_type=feature_type)
                        file_name = io.save_report(file_name=file_name, subject_name=subject_name, report_header='training',
                                                   line=training_summary)
            pass

    def train_auto(self, csv_file, subject_name, feature_type):

        results = DataOptimizer.obtain_optimal_classifier(
            csv_file_name=csv_file,
            subject_name=subject_name,
            feature_type=feature_type,
            kernel_type=self.kernel_type,
            classifier_type=self.classifier_type,
            activation=self.activation,
            optimizer=self.optimizer
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
            kernel_type=self.kernel_type,
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
