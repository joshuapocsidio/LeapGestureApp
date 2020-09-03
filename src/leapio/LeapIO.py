import inspect
import os
import sys
from datetime import date, datetime
from string import lower


src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../leapLib'))
sys.path.insert(0, lib_dir)

con_dir = os.path.dirname(os.getcwd()) + "\config\\"
out_dir = os.path.dirname(os.getcwd()) + "\output\\"
dat_dir = out_dir + "data\\"
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


def create_data_file(file_name, labels):
    print("System       :       Creating Data File " + file_name)
    writer = open(file_name, 'w')

    writer.write(",".join(labels))
    writer.write('\n')
    writer.close()


def append_to_data_file(gesture_name, file_name, data_set):
    if gesture_name is not None and file_name is not None:
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


# SUMMARY FUNCTIONS
def save_report(subject_name, report_header, line, file_name=None):
    # Validate the file name - creates new one if does not exist
    file_name = validate_report_file(file_name=file_name, report_header=report_header, subject_name=subject_name)
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
def create_training_report(subject_name):
    today = date.today()
    now = datetime.now()

    date_today = today.strftime("%d-%m-%Y")
    time_now = now.strftime("%H-%M")

    file_name = "TRAINING_REPORT " + str(time_now) + "(" + str(date_today) + ").txt"
    file_name = tra_dir + "(" + subject_name + ") " + file_name

    writer = open(file_name, 'w')
    writer.close()

    return file_name


# CLASSIFICATION SUMMARY FUNCTIONS
def create_classification_report(subject_name):
    today = date.today()
    now = datetime.now()

    date_today = today.strftime("%d-%m-%Y")
    time_now = now.strftime("%H-%M")

    file_name = "CLASSIFICATION_REPORT " + str(time_now) + "(" + str(date_today) + ").txt"
    file_name = cla_dir + "(" + subject_name + ") " + file_name

    writer = open(file_name, 'w')
    writer.close()

    return file_name


# VALIDATION FUNCTIONS
def validate_data_file(file_name, labels):
    invalid = False

    if does_file_exist(file_name):
        if not do_parameters_match(file_name=file_name, labels=labels):
            print("System       :       Parameters do not match - creating a new file")
            invalid = True
    else:
        print("System       :       Specified file name does not exist - creating a new file")
        invalid = True

    if invalid is True:  # Only create file if specified file is invalid
        create_data_file(file_name=file_name, labels=labels)


def validate_report_file(report_header, subject_name, file_name):
    if file_name is None:
        if lower(report_header) == 'training':
            return create_training_report(subject_name)
        elif lower(report_header) == 'classification':
            return create_classification_report(subject_name)
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
def get_data_files(extension):
    directory = dat_dir
    data_file_names = []
    for file_name in os.listdir(directory):
        file_name = directory + file_name
        if file_name.endswith(extension):
            data_file_names.append(file_name)

    return data_file_names


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
