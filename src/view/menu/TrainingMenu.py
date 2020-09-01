from controller import DataOptimizer
from leapio import Printer
import leapio.LeapIO as io


def show():
    # Shows menu for training gesture data
    done = False

    while done is False:
        print("-------------")
        print("DATA TRAINING")
        print("-------------")
        print("(1) - Single Training")
        print("(2) - Multi Training")
        print("(0) - Back")

        choice = raw_input("Your Choice: ")

        if choice == '1':
            done = single_training()
            pass
        elif choice == '2':
            done = multi_training()
            pass
        elif choice == '0':
            done = True
            pass
        else:
            print "Please try again."
            pass


def single_training():
    data_files = io.get_data_files('.csv')

    print ""
    print "~ ~ ~ ~ ~ ~ ~ ~ LIST OF DATA SOURCE ~ ~ ~ ~ ~ ~ ~ ~"
    Printer.print_numbered_list(data_files)
    print "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~"

    choice = raw_input("Enter the data set to train from: ")
    csv_file = data_files[int(choice) - 1]
    print("Chosen File : " + csv_file)
    print ""

    kernel_list = io.read_col("kernels.txt")
    print "* List of Kernels *"
    Printer.print_numbered_list(kernel_list)
    choice = raw_input("Enter the kernel to use for training: ")
    kernel_type = kernel_list[int(choice) - 1]
    print("Chosen Kernel : " + kernel_type)
    print ""

    train_auto(csv_file=csv_file, kernel_type=kernel_type)
    pass


def multi_training():
    data_files = io.get_data_files('.csv')
    kernel_list = io.read_col("kernels.txt")

    print ""
    "* List of Data Files to Train *"
    Printer.print_numbered_list(data_files)
    print ""

    "* List of Kernels for Training *"
    Printer.print_numbered_list(kernel_list)
    print ""

    file_name = None
    for data_file in data_files:
        subject_name = data_file.rsplit("(", 1)[1].rsplit(")")[0]
        for kernel in kernel_list:
            training_summary = train_auto(csv_file=data_file, kernel_type=kernel)
            file_name = io.save_report(file_name=file_name, subject_name=subject_name, report_header='training', line=training_summary)
            pass
    pass


def train_auto(csv_file, kernel_type):
    results = DataOptimizer.obtain_optimal_classifier(
        csv_file_name=csv_file,
        kernel_type=kernel_type
    )

    optimal_classifier = results[0]
    training_summary = results[1]

    optimal_classifier.save_classifier()

    return training_summary

def train_manual(csv_file, kernel_type):
    results = DataOptimizer.obtain_optimal_classifier(
        csv_file_name=csv_file,
        kernel_type=kernel_type
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
            print "Please try again."
    pass
