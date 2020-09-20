import time

from statistics import mean

from controller.LeapDataTrainer import SVM_Trainer, NN_Trainer, DT_Trainer


def optimal_svm(csv_file_name, subject_name, feature_type, gesture_set, kernel_type, iterations=10):
    index = 1
    trainer_list = []
    train_accuracy_list = []
    test_accuracy_list = []
    time_list = []

    while index <= iterations:
        # Initialize Leap Trainer with kernel type and classifier name
        trainer = SVM_Trainer(kernel_type=kernel_type, subject_name=subject_name, feature_type=feature_type,
                              gesture_set=gesture_set)
        # Initialise timer and execute training
        start_time = time.time()
        trainer.train(csv_file_name)
        end_time = time.time()

        # Obtain performance results
        training_time = round(end_time - start_time, 5)
        train_accuracy = round(trainer.training_acc * 100.0, 3)
        test_accuracy = round(trainer.testing_acc * 100.0, 3)

        # Append trainer and performance results to list
        trainer_list.append(trainer)
        time_list.append(training_time)
        train_accuracy_list.append(train_accuracy)
        test_accuracy_list.append(test_accuracy)

        # Print result of this iteration on console
        iteration_result = "Classifier #" + str(index) + " - (" + str(train_accuracy) + "%, " + str(
            test_accuracy) + "%) :: " + str(
            training_time) + " seconds"
        print(iteration_result)

        index += 1

    return trainer_list, time_list, train_accuracy_list, test_accuracy_list


def optimal_nn(csv_file_name, subject_name, feature_type, gesture_set, activation, iterations=5):
    index = 1
    trainer_list = []
    train_accuracy_list = []
    test_accuracy_list = []
    time_list = []

    while index <= iterations:
        # Initialize Leap Trainer with kernel type and classifier name
        trainer = NN_Trainer(subject_name=subject_name, feature_type=feature_type, gesture_set=gesture_set,
                             activation=activation)
        # Initialise timer and execute training
        start_time = time.time()
        trainer.train(csv_file=csv_file_name)
        end_time = time.time()

        # Obtain performance results
        training_time = round(end_time - start_time, 5)
        train_accuracy = round(trainer.training_acc * 100.0, 3)
        test_accuracy = round(trainer.testing_acc * 100.0, 3)

        # Append trainer and performance results to list
        trainer_list.append(trainer)
        time_list.append(training_time)
        train_accuracy_list.append(train_accuracy)
        test_accuracy_list.append(test_accuracy)

        # Print result of this iteration on console
        iteration_result = "Classifier #" + str(index) + " - (" + str(train_accuracy) + "%, " + str(
            test_accuracy) + "%) :: " + str(
            training_time) + " seconds"
        print(iteration_result)

        index += 1

    return trainer_list, time_list, train_accuracy_list, test_accuracy_list


def optimal_dt(csv_file_name, subject_name, feature_type, criterion_type, gesture_set, iterations=10):
    index = 1
    trainer_list = []
    train_accuracy_list = []
    test_accuracy_list = []
    time_list = []

    while index <= iterations:
        # Initialize Leap Trainer with kernel type and classifier name
        trainer = DT_Trainer(criterion_type=criterion_type, subject_name=subject_name, feature_type=feature_type,
                             gesture_set=gesture_set)
        # Initialise timer and execute training
        start_time = time.time()
        trainer.train(csv_file_name)
        end_time = time.time()

        # Obtain performance results
        training_time = round(end_time - start_time, 5)
        train_accuracy = round(trainer.training_acc * 100.0, 3)
        test_accuracy = round(trainer.testing_acc * 100.0, 3)

        # Append trainer and performance results to list
        trainer_list.append(trainer)
        time_list.append(training_time)
        train_accuracy_list.append(train_accuracy)
        test_accuracy_list.append(test_accuracy)

        # Print result of this iteration on console
        iteration_result = "Classifier #" + str(index) + " - (" + str(train_accuracy) + "%, " + str(
            test_accuracy) + "%) :: " + str(
            training_time) + " seconds"
        print(iteration_result)

        index += 1

    return trainer_list, time_list, train_accuracy_list, test_accuracy_list


# Optimizes classifier based on classifier types
def obtain_optimal_classifier(csv_file_name, subject_name, classifier_type, feature_type, gesture_set, params):
    trainer_list = []
    train_accuracy_list = []
    test_accuracy_list = []
    time_list = []

    if classifier_type == 'nn':
        activation = params[0]
        trainer_list, time_list, train_accuracy_list, test_accuracy_list = \
            optimal_nn(csv_file_name=csv_file_name,
                       subject_name=subject_name,
                       feature_type=feature_type,
                       activation=activation,
                       gesture_set=gesture_set)
    elif classifier_type == 'svm':
        kernel_type = params[0]
        trainer_list, time_list, train_accuracy_list, test_accuracy_list = \
            optimal_svm(csv_file_name=csv_file_name,
                        subject_name=subject_name,
                        feature_type=feature_type,
                        kernel_type=kernel_type,
                        gesture_set=gesture_set)
    elif classifier_type == 'dt':
        criterion_type = params[0]
        trainer_list, time_list, train_accuracy_list, test_accuracy_list = \
            optimal_dt(csv_file_name=csv_file_name,
                       subject_name=subject_name,
                       feature_type=feature_type,
                       criterion_type=criterion_type,
                       gesture_set=gesture_set)
    print("")

    # Get optimization results
    optimized = analyze_classifiers(
        trainer_list=trainer_list,
        time_list=time_list,
        train_accuracy_list=train_accuracy_list,
        test_accuracy_list=test_accuracy_list
    )

    # Get optimal classifier
    optimal_classifier = optimized[0]
    # Get optimization summary report
    optimization_summary = optimized[1]

    return optimal_classifier, optimization_summary


def analyze_classifiers(trainer_list, time_list, train_accuracy_list, test_accuracy_list):
    # Obtain relevant TIME summary fields
    worst_time = max(time_list)
    best_time = min(time_list)
    average_time = round(mean(time_list), 5)
    total_time = round(sum(time_list), 5)

    num_accuracy_data = len(train_accuracy_list)

    accuracy_score_list = []

    for i in range(num_accuracy_data):
        train_acc = train_accuracy_list[i]
        test_acc = test_accuracy_list[i]

        penalty = test_acc - train_acc
        acc_score = train_acc + penalty
        accuracy_score_list.append(acc_score)

    worst_accuracy = min(accuracy_score_list)
    best_accuracy = max(accuracy_score_list)
    average_accuracy = round(mean(test_accuracy_list), 5)

    # Get the respective training and testing accuracies for worst
    index_worst = accuracy_score_list.index(worst_accuracy)
    worst_train_acc = train_accuracy_list[index_worst]
    worst_test_acc = test_accuracy_list[index_worst]
    worst_penalty = worst_test_acc - worst_train_acc

    # Get the respective training and testing accuracies for best
    index_optimal = accuracy_score_list.index(best_accuracy)
    optimal_train_acc = train_accuracy_list[index_optimal]
    optimal_test_acc = test_accuracy_list[index_optimal]
    optimal_penalty = optimal_test_acc - optimal_train_acc

    # Get the optimal classifier
    optimal_classifier = trainer_list[index_optimal]

    summary = "* * * * * * * * * *\n"
    summary += "SUMMARY REPORT\n"
    summary += "* * * * * * * * * *\n"
    # Construct summary report
    summary += "CLASSIFIER          : " + optimal_classifier.classifier_name + '\n'
    summary += "FEATURE TYPE        : " + optimal_classifier.feature_type + "\n"
    summary += "GESTURE SET         : " + optimal_classifier.gesture_set + "\n\n"

    summary += "TIME(TOTAL)         : " + str(total_time) + " seconds \n"
    summary += "TIME(WORST)         : " + str(worst_time) + " seconds \n"
    summary += "TIME(BEST)          : " + str(best_time) + " seconds \n"
    summary += "TIME(AVERAGE)       : " + str(average_time) + " seconds\n\n"

    summary += "ACCURACY(WORST)     : " + \
               str(worst_accuracy) + "% with Training = " + \
               str(worst_train_acc) + "% and Testing = " + \
               str(worst_test_acc) + "%" + " (" + ("" if worst_penalty < 0.0 else "+") + str(worst_penalty) + "%)\n"
    summary += "ACCURACY(BEST)      : " + \
               str(best_accuracy) + "% with Training = " + \
               str(optimal_train_acc) + "% and Testing = " + \
               str(optimal_test_acc) + "%" + " (" + ("" if optimal_penalty < 0.0 else "+") + str(
        optimal_penalty) + "%)\n"
    summary += "ACCURACY(AVERAGE)   : " + str(average_accuracy) + "%\n\n"

    summary += "OPTIMAL CLASSIFIER  : Classifier #" + str((index_optimal + 1)) + "\n"
    summary += "OPTIMAL SCORE       : " + str(best_accuracy) + "%\n"
    summary += "OPTIMAL PENALTY     : " + ("" if optimal_penalty < 0.0 else "+") + str(optimal_penalty) + "%\n\n"

    summary += " - - - - - - - - HYPER PARAMETERS - - - - - - - - - \n"
    # Support Vector Machine
    if hasattr(optimal_classifier, 'kernel_type'):
        if hasattr(optimal_classifier, 'kernel_type'):
            if hasattr(optimal_classifier, 'gamma'):
                summary += "KERNEL              : " + optimal_classifier.kernel_type + "\n"
                summary += "C_PARAM             : " + str(optimal_classifier.c_param) + "\n"
                summary += "GAMMA               : " + str(optimal_classifier.gamma) + "\n\n"

    # Neural Network
    if hasattr(optimal_classifier, 'batch_size'):
        if hasattr(optimal_classifier, 'n_layers'):
            if hasattr(optimal_classifier, 'n_layer_nodes'):
                if hasattr(optimal_classifier, 'activation'):
                    if hasattr(optimal_classifier, 'optimizer'):
                        summary += "ACTIVATION          : " + str(optimal_classifier.activation) + "\n"
                        summary += "OPTIMIZER           : " + str(optimal_classifier.optimizer) + "\n"
                        summary += "BATCH_SIZE          : " + str(optimal_classifier.batch_size) + "\n"
                        summary += "HIDDEN_LAYERS       : " + str(optimal_classifier.n_layers) + "\n"
                        summary += "HIDDEN_LAYER_NODES  : " + str(optimal_classifier.n_layer_nodes) + "\n"
                        summary += "LEARNING RATE       : " + str(optimal_classifier.learning_rate) + "\n\n"

    # Decision Trees
    if hasattr(optimal_classifier, 'splitter'):
        if hasattr(optimal_classifier, 'max_leaf_nodes'):
            if hasattr(optimal_classifier, 'min_samples_split'):
                summary += "SPLITTER            : " + str(optimal_classifier.splitter) + "\n"
                summary += "MAX LEAF NODES      : " + str(optimal_classifier.max_leaf_nodes) + "\n"
                summary += "MIN SAMPLES SPLIT   : " + str(optimal_classifier.min_samples_split) + "\n\n"

    summary += "* * * * * * * * * *\n"

    print(summary)

    return optimal_classifier, summary
