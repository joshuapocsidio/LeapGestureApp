import inspect
import os
import sys
from datetime import date, datetime
from string import lower, rsplit, upper
import pickle

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../leapLib'))
sys.path.insert(0, lib_dir)

con_dir = os.path.dirname(os.getcwd()) + "\config\\"
out_dir = os.path.dirname(os.getcwd()) + "\output\\"

dat_dir = out_dir + "data\\"
trd_dir = dat_dir + "trained_data\\"
sca_dir = dat_dir + "standard_scales\\"
com_dir = dat_dir + "combined_data\\"
uns_dir = dat_dir + "unseen_data\\"
cun_dir = uns_dir + "combined_unseen_data\\"

sum_dir = out_dir + "summary\\"
tra_dir = sum_dir + "training\\"
cla_dir = sum_dir + "classification\\"


# DATA FILE FUNCTIONS
def save_data(file_name, subject_name, gesture_name, data_set):
    file_name = dat_dir + "(" + subject_name + ") " + file_name + ".csv"
    label_list = []
    value_list = []

    # Get lists of data and values
    for data in data_set:
        label_list.append(data.label)
        value_list.append(data.value)

    # Add class to the end of the values
    label_list.append("class")

    # Validate if file exist or if parameters match
    validate_data_file(file_name=file_name, labels=label_list)

    # After creating new file (or not), append to existing file
    append_to_data_file(gesture_name=gesture_name, file_name=file_name, data_set=value_list)


def create_data_file(file_name, labels, verbose=False):
    if verbose is True:
        print("System       :       Creating Data File " + file_name)

    writer = open(file_name, 'w')

    writer.write(",".join(labels))
    writer.write('\n')
    writer.close()


def append_to_data_file(gesture_name, file_name, data_set, verbose=False):
    if gesture_name is not None and file_name is not None:
        if verbose is True:
            print("System       :       Appending Data File " + file_name)
        values = []

        # Change list to string data
        for data in data_set:
            values.append(str(data))

        # Append the name of gesture for classification
        values.append(gesture_name)
        writer = open(file_name, "a")
        line = ",".join(values)
        writer.write(line)
        writer.write('\n')
        writer.close()


def save_classifier(pickle_name, data):
    file_path = trd_dir + pickle_name
    print("Saving Classifier : " + str(file_path))
    pickle_file = open(file_path, 'wb')
    pickle.dump(data, pickle_file)
    pickle_file.close()
    pass


def load_classifier(pickle_name):
    file_path = trd_dir + rsplit(pickle_name, "\\")[-1]
    print("Saving Classifier : " + str(file_path))
    pickle_file = open(file_path, 'rb')
    data = pickle.load(pickle_file)
    return data


def save_scale(pickle_name, data):
    file_path = sca_dir + pickle_name
    print("Saving Scale      : " + str(file_path))
    pickle_file = open(file_path, 'wb')
    pickle.dump(data, pickle_file)
    pickle_file.close()


def load_scale(pickle_name):
    file_path = sca_dir + rsplit(pickle_name, "\\")[-1]
    print("Loading Scale     : " + str(file_path))
    pickle_file = open(file_path, 'rb')
    data = pickle.load(pickle_file)
    return data


# SUMMARY FUNCTIONS
def save_report(subject_name, report_header, line, classifier_type=None, feature_set=None, gesture_set=None, file_name=None):
    # Validate the file name - creates new one if does not exist
    file_name = validate_report_file(file_name=file_name, report_header=report_header, subject_name=subject_name,
                                     classifier_type=classifier_type, feature_set=feature_set, gesture_set=gesture_set)
    # Append to report once validated
    append_to_report(file_name=file_name, line=line)

    return file_name


def append_to_report(file_name, line):
    if line is not None:
        writer = open(file_name, 'a')
        writer.write(line)
        writer.write('\n')
        writer.close()


# TRAINING SUMMARY FUNCTIONS
def create_training_report(subject_name, feature_set, gesture_set, classifier_type):

    file_name = upper(classifier_type) + "_TRAINING_REPORT "
    file_name = tra_dir + file_name + "(" + subject_name + ") " + gesture_set + "--" + feature_set + ".txt"

    writer = open(file_name, 'w')
    writer.close()

    return file_name


# CLASSIFICATION SUMMARY FUNCTIONS
def create_classification_report(subject_name, classifier_type=None, feature_set=None, gesture_set=None):

    file_name = upper(classifier_type) + "_CLASSIFICATION_REPORT"
    file_name = cla_dir + file_name + "(" + subject_name + ") " + gesture_set + "--" + feature_set + ".txt"

    writer = open(file_name, 'w')
    writer.close()

    return file_name


# VALIDATION FUNCTIONS
def validate_data_file(file_name, labels, verbose=False):
    invalid = False

    if does_file_exist(file_name):
        if not do_parameters_match(file_name=file_name, labels=labels):
            if verbose is True:
                print("System       :       Parameters do not match - creating a new file")
            invalid = True
    else:
        if verbose is True:
            print("System       :       Specified file name does not exist - creating a new file")
        invalid = True

    if invalid is True:  # Only create file if specified file is invalid
        create_data_file(file_name=file_name, labels=labels)


def validate_report_file(report_header, subject_name, file_name, classifier_type=None, gesture_set=None, feature_set=None):
    if file_name is None:
        if lower(report_header) == 'training':
            return create_training_report(subject_name=subject_name, classifier_type=classifier_type,
                                          gesture_set=gesture_set, feature_set=feature_set)
        elif lower(report_header) == 'classification':
            return create_classification_report(subject_name=subject_name, classifier_type=classifier_type,
                                                gesture_set=gesture_set, feature_set=feature_set)
        else:
            print("Invalid Report Heading")
    else:
        return file_name


def does_file_exist(file_name):
    exists = False
    if os.path.exists(file_name):
        exists = True

    return exists


def do_parameters_match(file_name, labels):
    reader = open(file_name, "r")

    first_line = reader.readline()

    if first_line is not None:
        file_labels = first_line.split(",")
        num_params = len(file_labels)

        if num_params == len(labels):
            i = 0
            while i < num_params:
                file_label = file_labels[i].strip()
                other_label = labels[i].strip()

                # Exit the method once a mismatch is found
                if not file_label == other_label:
                    print("-" + file_label.strip() + '-')
                    print('-' + other_label.strip() + '-')
                    print("Parameter mismatch")
                    return False

                i += 1
        else:
            print("Parameter size mismatch")
            return False
    else:
        print("Parameter line is empty")
        return False
    return True


# GESTURE DATABASE FUNCTIONS
def create_gesture_database(file_name):
    file_name = con_dir + file_name
    gestures = ["fist", "one", "two", "three", "four", "five"]

    writer = open(file_name, 'w')
    writer.close()

    writer = open(file_name, 'a')
    for gesture in gestures:
        writer.write(gesture + "\n")

    writer.close()


# Returns all file names inside current directory (or given directory if omitted) with matching extension
def get_data_files(directory=dat_dir, combined=False):
    extension = '.csv'
    data_file_names = []
    if combined is True:
        for file_name in os.listdir(com_dir):
            file_name = com_dir + file_name
            if file_name.endswith(extension):
                data_file_names.append(file_name)
    else:
        for file_name in os.listdir(directory):
            file_name = directory + file_name
            if file_name.endswith(extension):
                data_file_names.append(file_name)

    return data_file_names

def get_unseen_data_files(directory=uns_dir, combined=False):
    extension = '.csv'
    unseen_data_files = []
    if combined is True:
        for file_name in os.listdir(com_dir):
            file_name = uns_dir + file_name
            if file_name.endswith(extension):
                unseen_data_files.append(file_name)
    else:
        for file_name in os.listdir(directory):
            file_name = directory + file_name
            if file_name.endswith(extension):
                unseen_data_files.append(file_name)

    return unseen_data_files

def get_pickle_files(directory=trd_dir):
    extension = '.pickle'
    pickle_file_names = []

    for file_name in os.listdir(directory):
        file_name = directory + file_name
        if file_name.endswith(extension):
            pickle_file_names.append(file_name)

    return pickle_file_names


def read_row(file_name, index=0, delimiter=','):
    reader = open(file_name, 'r')

    lines = reader.readlines()
    row = lines[index]
    data_list = row.split(delimiter)

    return data_list


def read_col(file_name, index=0, delimiter=','):
    file_name = con_dir + file_name
    reader = open(file_name, 'r')

    lines = reader.readlines()

    data_list = []
    for line in lines:
        content = line.split(delimiter)
        data = content[index].strip()
        data_list.append(data)

    return data_list

def read_all(file_name):
    reader = open(file_name, 'r')

    lines = reader.readlines()

    return lines

def append_to_file(file_name, lines):
    writer = open(file_name, 'a')
    writer.write(lines)
    writer.write("\n")
    writer.close()
    pass