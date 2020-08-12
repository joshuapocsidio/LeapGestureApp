import inspect
import os
import sys
from datetime import date, datetime

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../leapLib'))
sys.path.insert(0, lib_dir)


def save_data(file_name, gesture_name, data_set):
    file_name = file_name + ".csv"
    print(file_name)
    label_list = []
    value_list = []

    # Get lists of data and values
    for data in data_set:
        label_list.append(data.label)
        value_list.append(data.value)

    # Add class to the end of the values
    label_list.append("class")

    # Validate if file exist or if parameters match
    validate_file(file_name=file_name, labels=label_list)

    # After creating new file (or not), append to existing file
    append_to_data_file(gesture_name=gesture_name, file_name=file_name, data_set=value_list)


def validate_file(file_name, labels):
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


def does_file_exist(file_name):
    exists = False
    if os.path.exists(file_name):
        exists = True

    return exists


def create_data_file(file_name, labels):
    writer = open(file_name, 'w')

    writer.write(",".join(labels))
    writer.write('\n')
    writer.close()


def create_training_report():
    today = date.today()
    now = datetime.now()

    date_today = today.strftime("%d-%m-%Y")
    time_now = now.strftime("%H-%M")

    file_name = "CLASSIFICATION_REPORT " + str(time_now) + "(" + str(date_today) + ").txt"
    print(file_name)

    writer = open(file_name, 'w')
    writer.close()

    return file_name


def append_to_report(file_name, line):
    writer = open(file_name, 'a')
    writer.write(line)
    writer.write('\n')
    writer.close()


def append_to_data_file(gesture_name, file_name, data_set):
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
                    print("stop")
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


# Returns all file names inside current directory (or given directory if omitted) with matching extension
def get_files(extension, current_directory=os.getcwd()):
    data_file_names = []
    for file_name in os.listdir(current_directory):
        if file_name.endswith(extension):
            data_file_names.append(file_name)

    return data_file_names
