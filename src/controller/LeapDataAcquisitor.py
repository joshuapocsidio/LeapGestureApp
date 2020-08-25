from pip._vendor.distlib.compat import raw_input

from Leap import Bone, Finger
from leapio import LeapIO
from model.LeapData import LeapData
import time
import math


def get_palm_to_finger_distance_set(leap_controller, gesture_name, iterations=1, hand=None, return_mode=False):
    # Initialize name of the file and labels
    file_name = 'finger-to-palm-distance'
    labels = ["thumb", "index", "middle", "ring", "pinky"]
    print("ITERATIONS : " + str(iterations))
    feature_set = []

    while len(feature_set) < iterations:
        if hand is None:
            # Obtain hand and fingers data
            hand = get_hand_data(leap_controller=leap_controller)

        fingers = hand.fingers

        # Obtain palm vector position
        palm_vector = hand.palm_position

        # Iterate through each finger and obtain distance data
        value_set = []
        for finger in fingers:
            distance = round(finger.tip_position.distance_to(palm_vector), 5)
            # Add the hand data to data set
            value_set.append(distance)

        # Convert into leap data
        feature = convert_to_leap_data_set(labels=labels, values=value_set)
        # Append set of finger data into a set
        feature_set.append(feature)
        hand = None

        if return_mode is False:
            # Save data into a file
            LeapIO.save_data(file_name=file_name, gesture_name=gesture_name, data_set=feature)
        else:
            return feature_set


def get_palm_to_finger_angle_set(leap_controller, gesture_name, iterations=1, hand=None, return_mode=False):
    file_name = 'finger-angle-using-bones'
    labels = ["thumb", "index", "middle", "ring", "pinky"]
    feature_set = []

    while len(feature_set) < iterations:
        if hand is None:
            # Obtain hand and fingers data
            hand = get_hand_data(leap_controller=leap_controller)

        fingers = hand.fingers

        # Iterate through each finger and execute appropriate adjustments
        value_set = []
        for finger in fingers:
            if finger.type == Finger.TYPE_THUMB:
                # Use Proximal and Distal bones and obtain direction vectors
                proximal_bone = finger.bone(Bone.TYPE_PROXIMAL)
                distal_bone = finger.bone(Bone.TYPE_DISTAL)

                inner_bone_vector = proximal_bone.direction
                outer_bone_vector = distal_bone.direction
            else:
                # Use Metacarpal and Intermediate bones and obtain direction vectors
                metacarpal_bone = finger.bone(Bone.TYPE_METACARPAL)
                intermediate_bone = finger.bone(Bone.TYPE_INTERMEDIATE)

                inner_bone_vector = metacarpal_bone.direction
                outer_bone_vector = intermediate_bone.direction

            # Calculate angle between inner and outer bones' direction vectors
            angle_rad = inner_bone_vector.angle_to(outer_bone_vector)
            angle_deg = math.degrees(angle_rad)

            # Add the data to data_set
            value_set.append(angle_deg)

        # Convert into leap data
        feature = convert_to_leap_data_set(labels=labels, values=value_set)
        # Append set of finger data into a set
        feature_set.append(feature)

        # Reset current hand
        hand = None

        if return_mode is False:
            # Save data into a file
            LeapIO.save_data(file_name=file_name, gesture_name=gesture_name, data_set=feature_set)
        else:
            return feature_set


def get_finger_to_palm_angle_and_distance(leap_controller, gesture_name, iterations=1, hand=None, return_mode=False):
    file_name = 'finger-angle-and-palm-distance'
    labels = ["thumb", "index", "middle", "ring", "pinky"]
    feature_set = []

    while len(feature_set) < iterations:
        if hand is None:
            # Obtain hand and fingers data
            hand = get_hand_data(leap_controller=leap_controller)

        fingers = hand.fingers

        # Iterate through each finger and obtain angle and distance data
        value_set = []
        angle_set = get_palm_to_finger_angle_set(leap_controller=leap_controller, gesture_name=gesture_name, hand=hand,
                                                 return_mode=True)
        distance_set = get_palm_to_finger_distance_set(leap_controller=leap_controller, gesture_name=gesture_name,
                                                       hand=hand, return_mode=True)

        # Number of distances and angle should be the same
        num_angles = len(angle_set)
        num_distances = len(distance_set)

        if num_angles == num_distances:
            num_data = num_distances

        # Iterate through each data - up to number of data obtained
        i = 0
        while i < num_data:
            angle = float(angle_set[i])
            distance = float(distance_set[i])

            # Combine the two data by multiplying
            value = round(angle * distance, 5)
            # Append value to data set
            value_set.append(value)

            i += 1

        # Convert into leap data
        feature = convert_to_leap_data_set(labels=labels, values=value_set)
        # Append set of finger data into a set
        feature_set.append(feature)

        # Reset current hand
        hand = None

        if return_mode is False:
            # Save data into a file
            LeapIO.save_data(file_name=file_name, gesture_name=gesture_name, data_set=feature_set)
        else:
            return feature_set


def get_distance_between_fingers_set(leap_controller, gesture_name, iterations=1, hand=None, return_mode=False):
    file_name = 'finger-between-distance'
    labels = ["thumb-index", "index-middle", "middle-ring", "ring-pinky"]
    feature_set = []

    while len(feature_set) < iterations:
        if hand is None:
            # Obtain hand and fingers data
            hand = get_hand_data(leap_controller=leap_controller)

        fingers = hand.fingers

        # Iterate through each finger and execute appropriate adjustments
        value_set = []

        # For each hand, iterate through each finger pairs and obtain data
        i = 0
        while i < (len(fingers) - 1):
            # Get fingers
            finger_a = fingers[i]
            finger_b = fingers[i + 1]

            # Get finger tip positions
            vector_a = finger_a.tip_position
            vector_b = finger_b.tip_position

            # Get distance between finger a and b
            distance = round(vector_a.distance_to(vector_b), 5)

            # Add the data to data_set
            value_set.append(distance)

        # Convert into leap data
        feature = convert_to_leap_data_set(labels=labels, values=value_set)
        # Append set of finger data into a set
        feature_set.append(feature)

        # Reset current hand
        hand = None

        if return_mode is False:
            # Save data into a file
            LeapIO.save_data(file_name=file_name, gesture_name=gesture_name, data_set=feature_set)
        else:
            return feature_set


def get_all_hand_feature_type(leap_controller, gesture_name, iterations=1):
    i = 0
    while i < iterations:
        # Obtain hand and fingers data
        hand = get_hand_data(leap_controller=leap_controller)

        get_palm_to_finger_distance_set(leap_controller=leap_controller, gesture_name=gesture_name, hand=hand)
        get_palm_to_finger_angle_set(leap_controller=leap_controller, gesture_name=gesture_name, hand=hand)
        get_finger_to_palm_angle_and_distance(leap_controller=leap_controller, gesture_name=gesture_name, hand=hand)
        get_distance_between_fingers_set(leap_controller=leap_controller, gesture_name=gesture_name, hand=hand)

        i += 1


def convert_to_leap_data_set(labels, values):
    # Iterate through all values obtained and convert to Leap Data
    i = 0
    data_set = []
    for value in values:
        data = LeapData(label=labels[i], value=value)
        data_set.append(data)
        i += 1

    return data_set


def get_hand_data(leap_controller):
    done = False

    while done is False:
        # Only do stuff if controller is connected
        if leap_controller.is_connected:
            print("System       :       Leap Controller is Connected")

            # Obtain current hands from current frame
            hands = leap_controller.frame().hands

            # Only attempt to obtain hands data if there is a hand
            if is_data_valid(leap_controller=leap_controller):
                hand = leap_controller.frame().hands[0]

                if hand is not None:
                    done = True
                    return hand
            time.sleep(1)
    pass


def is_data_valid(leap_controller):
    is_valid = False
    if leap_controller.is_connected:
        hands = leap_controller.frame().hands

        # Keep only if there is a hand
        if len(hands) > 0:
            print("System       :       Valid hand(s) detected")

            # Give user control when to obtain data
            raw_input("Press any key to get data: ")

            # Get the latest frame again
            hands = leap_controller.frame().hands

            if len(hands) > 0:
                is_valid = True
            else:
                print("System       :       Previously detected hand is not visible - Please try again")
        else:
            print("System       :       No hand(s) detected - Please try again")
    return is_valid
