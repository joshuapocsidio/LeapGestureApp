from statistics import mean

from controller.LeapDataTrainer import LeapTrainer
import time


# Optimizes classifier based
def obtain_optimal_classifier(csv_file_name, kernel_type, iterations=100):
    # Obtain csv file without extension
    csv_file_no_extension = csv_file_name.rsplit(".", 1)[0]

    index = 1
    trainer_list = []
    accuracy_list = []
    time_list = []
    result_list = []

    while index < iterations:
        # Initialize Leap Trainer with kernel type and classifier name
        trainer = LeapTrainer(kernel_type=kernel_type, classifier_name=csv_file_no_extension)

        # Initialise timer and execute training
        start_time = time.time()
        trainer.train_with_svm(csv_file_name)
        end_time = time.time()

        # Obtain performance results
        training_time = round(end_time - start_time, 5)
        classifier_accuracy = round(trainer.get_accuracy() * 100.0, 3)

        # Append trainer and performance results to list
        trainer_list.append(trainer)
        time_list.append(training_time)
        accuracy_list.append(classifier_accuracy)

        # Print result of this iteration on console
        iteration_result = "Classifier #" + str(index) + " - " + str(classifier_accuracy) + "%" + " (" + str(
            training_time) + " sec)"
        print iteration_result

        # Append result into compilation of results
        result_list.append(iteration_result)

        index += 1

    print ""
    result_list.append("")

    # Get optimization results
    optimized = analyze_classifiers(
        trainer_list=trainer_list,
        time_list=time_list,
        accuracy_list=accuracy_list,
    )

    # Get optimal classifier
    optimal_classifier = optimized[0]
    # Get optimization summary report
    optimization_summary = optimized[1]

    return optimal_classifier, optimization_summary


def analyze_classifiers(trainer_list, time_list, accuracy_list):
    # Obtain relevant TIME summary fields
    worst_time = max(time_list)
    best_time = min(time_list)
    average_time = round(mean(time_list), 5)
    total_time = round(sum(time_list), 5)

    # Obtain relevant ACCURACY summary fields
    worst_accuracy = min(accuracy_list)
    best_accuracy = max(accuracy_list)
    average_accuracy = round(mean(accuracy_list), 5)

    # Get the optimal classifier
    index_max_accuracy = accuracy_list.index(best_accuracy)
    optimal_classifier = trainer_list[index_max_accuracy]

    summary = "* * * * * * * * * *\n"
    summary += "SUMMARY REPORT\n"
    summary += "* * * * * * * * * *\n"
    # Construct summary report
    summary += "CLASSIFIER          : " + optimal_classifier.classifier_name + "\n"
    summary += "KERNEL              : " + optimal_classifier.kernel_type + "\n"
    summary += "TIME(TOTAL)         : " + str(total_time) + " seconds \n"
    summary += "TIME(WORST)         : " + str(worst_time) + " seconds \n"
    summary += "TIME(BEST)          : " + str(best_time) + " seconds \n"
    summary += "TIME(AVERAGE)       : " + str(average_time) + " seconds\n\n"

    summary += "ACCURACY(WORST)     : " + str(worst_accuracy) + " %\n"
    summary += "ACCURACY(BEST)      : " + str(best_accuracy) + " %\n"
    summary += "ACCURACY(AVERAGE)   : " + str(average_accuracy) + "%\n\n"

    summary += "OPTIMAL CLASSIFIER  : Classifier #" + str((index_max_accuracy + 1)) + "\n"
    summary += "OPTIMAL ACCURACY    : " + str(best_accuracy) + "%\n"

    summary += "* * * * * * * * * *"

    print summary

    return optimal_classifier, summary
