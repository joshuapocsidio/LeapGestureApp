from controller import DataOptimizer
from leapio import Printer
import leapio.LeapIO as LeapIO


def show():
    # Shows menu for training gesture data
    kernel_type = 'linear'
    done = False

    while done is False:
        print("-------------")
        print("DATA TRAINING")
        print("-------------")

        trained_data_files = LeapIO.get_files('.csv')

        print ""
        print "~ ~ ~ ~ ~ ~ ~ ~ LIST OF DATA SOURCE ~ ~ ~ ~ ~ ~ ~ ~"
        Printer.print_numbered_list(trained_data_files)
        print "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~"

        choice = raw_input("Enter the data set to train from: ")
        csv_file = trained_data_files[int(choice) - 1]
        print("Chosen File : " + csv_file)

        results = DataOptimizer.obtain_optimal_classifier(
            csv_file_name=csv_file,
            kernel_type=kernel_type
        )

        optimal_classifier = results[0]
        training_summary = results[1]

        save_choice = raw_input("Would you like to save this classifier? (y/n")
        valid_choice = False

        while valid_choice is False:
            if save_choice == 'y':
                optimal_classifier.save_classifier()
                file_name = LeapIO.create_training_report()
                LeapIO.append_to_report(file_name=file_name, line=training_summary)
                # Save to report summary file
                valid_choice = True
            elif save_choice != 'n':
                print "Try again"
