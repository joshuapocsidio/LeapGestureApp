import math
import time

from pip._vendor.distlib.compat import raw_input

from Leap import Bone, Finger
from leapio import LeapIO
from model.LeapData import LeapData


def convert_to_leap_data_set(labels, values):
    # Iterate through all values obtained and convert to Leap Data
    i = 0
    data_set = []
    for value in values:
        data = LeapData(label=labels[i], value=value)
        data_set.append(data)
        i += 1

    return data_set


class LeapDataAcquisitor:
    def __init__(self, leap_controller, subject_name, verbose=False, supervised=True):
        self.leap_controller = leap_controller
        self.subject_name = subject_name
        self.verbose = verbose
        self.supervised = supervised

    def get_palm_to_finger_distance_set(self, gesture_name="", iterations=1, hand=None, return_mode=False):
        # Initialize name of the file and labels
        file_name = 'finger-to-palm-distance'
        labels = ["thumb", "index", "middle", "ring", "pinky"]
        feature_set = []

        while len(feature_set) < iterations:
            if hand is None:
                # Obtain hand and fingers data
                hand = self.get_hand_data()

            fingers = hand.fingers

            # Obtain palm vector position
            palm_vector = hand.palm_position

            # Iterate through each finger and obtain distance data
            value_set = []
            for finger in fingers:
                distance = round(finger.tip_position.distance_to(palm_vector), 5)
                # Add the hand data to data set
                value_set.append(distance)

            # Add the palm vectors data
            xd, yd, zd = self.get_palm_x_y_z_dir(hand=hand)
            value_set.append(xd)
            value_set.append(yd)
            value_set.append(zd)

            # Add palm vectors labels
            labels.append('palm_xd')
            labels.append('palm_yd')
            labels.append('palm_zd')

            # Convert into leap data
            feature = convert_to_leap_data_set(labels=labels, values=value_set)
            # Append set of finger data into a set
            feature_set.append(feature)
            hand = None

            if return_mode is False:
                # Save data into a file
                LeapIO.save_data(file_name=file_name, subject_name=self.subject_name, gesture_name=gesture_name, data_set=feature)
            else:
                return value_set

    def get_palm_to_finger_angle_set(self, gesture_name, iterations=1, hand=None, return_mode=False):
        file_name = 'finger-angle-using-bones'
        labels = ["thumb", "index", "middle", "ring", "pinky"]
        feature_set = []

        while len(feature_set) < iterations:
            if hand is None:
                # Obtain hand and fingers data
                hand = self.get_hand_data()

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

            if return_mode is False:
                # Add the palm vectors data
                xd, yd, zd = self.get_palm_x_y_z_dir(hand=hand)
                value_set.append(xd)
                value_set.append(yd)
                value_set.append(zd)

                # Add palm vectors labels
                labels.append('palm_xd')
                labels.append('palm_yd')
                labels.append('palm_zd')

            # Convert into leap data
            feature = convert_to_leap_data_set(labels=labels, values=value_set)
            # Append set of finger data into a set
            feature_set.append(feature)

            # Reset current hand
            hand = None

            if return_mode is False:
                # Save data into a file
                LeapIO.save_data(file_name=file_name, subject_name=self.subject_name, gesture_name=gesture_name, data_set=feature)
            else:
                return value_set

    def get_finger_to_palm_angle_and_distance(self, gesture_name, iterations=1, hand=None, return_mode=False):
        file_name = 'finger-angle-and-palm-distance'
        labels = ["thumb", "index", "middle", "ring", "pinky"]
        feature_set = []

        while len(feature_set) < iterations:
            if hand is None:
                # Obtain hand and fingers data
                hand = self.get_hand_data()

            fingers = hand.fingers

            # Iterate through each finger and obtain angle and distance data
            value_set = []
            angle_set = self.get_palm_to_finger_angle_set(gesture_name=gesture_name, hand=hand,
                                                          return_mode=True)
            distance_set = self.get_palm_to_finger_distance_set(gesture_name=gesture_name,
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

            if return_mode is False:
                # Add the palm vectors data
                xd, yd, zd = self.get_palm_x_y_z_dir(hand=hand)
                value_set.append(xd)
                value_set.append(yd)
                value_set.append(zd)

                # Add palm vectors labels
                labels.append('palm_xd')
                labels.append('palm_yd')
                labels.append('palm_zd')

            # Convert into leap data
            feature = convert_to_leap_data_set(labels=labels, values=value_set)
            # Append set of finger data into a set
            feature_set.append(feature)

            # Reset current hand
            hand = None

            if return_mode is False:
                # Save data into a file
                LeapIO.save_data(file_name=file_name, subject_name=self.subject_name, gesture_name=gesture_name, data_set=feature)
            else:
                return value_set

    def get_distance_between_fingers_set(self, gesture_name, iterations=1, hand=None, return_mode=False):
        file_name = 'finger-between-distance'
        labels = ["thumb-index", "index-middle", "middle-ring", "ring-pinky"]
        feature_set = []

        while len(feature_set) < iterations:
            if hand is None:
                # Obtain hand and fingers data
                hand = self.get_hand_data()

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

                i += 1

            if return_mode is False:
                # Add the palm vectors data
                xd, yd, zd = self.get_palm_x_y_z_dir(hand=hand)
                value_set.append(xd)
                value_set.append(yd)
                value_set.append(zd)

                # Add palm vectors labels
                labels.append('palm_xd')
                labels.append('palm_yd')
                labels.append('palm_zd')

            # Convert into leap data
            feature = convert_to_leap_data_set(labels=labels, values=value_set)
            # Append set of finger data into a set
            feature_set.append(feature)

            # Reset current hand
            hand = None

            if return_mode is False:
                # Save data into a file
                LeapIO.save_data(file_name=file_name, subject_name=self.subject_name, gesture_name=gesture_name, data_set=feature)
            else:
                return value_set

    def get_all_hand_feature_type(self, gesture_name, iterations=1):
        i = 0
        while i < iterations:
            # Obtain hand and fingers data
            hand = self.get_hand_data()

            self.get_palm_to_finger_distance_set(gesture_name=gesture_name, hand=hand)
            self.get_palm_to_finger_angle_set(gesture_name=gesture_name, hand=hand)
            self.get_finger_to_palm_angle_and_distance( gesture_name=gesture_name, hand=hand)
            self.get_distance_between_fingers_set(gesture_name=gesture_name, hand=hand)

            i += 1

    def get_palm_x_y_z_dir(self, hand):
        if hand is not None:
            x_d = round(hand.palm_normal.x, 5)
            y_d = round(hand.palm_normal.y, 5)
            z_d = round(hand.palm_normal.z, 5)

            return x_d, y_d, z_d

    def sample_hand_data(self):
        # Sample 100 frames hand data
        data_list = []
        while len(data_list) < 100:
            data_list.append(self.get_palm_to_finger_distance_set(return_mode=True))
            time.sleep(0.001)

        return data_list

    def get_hand_data(self):
        done = False
        hand = None
        if self.supervised is True:
            while done is False:
                if self.supervised_data_validation() is True:
                    hand = self.leap_controller.frame().hands[0]
                    if hand is not None:
                        done = True
                time.sleep(1)
            pass
        else:
            while done is False:
                is_valid, hand = self.unsupervised_data_validation()
                if is_valid is True:
                    done = True
                    time.sleep(0.05)
            pass
        return hand

    def supervised_data_validation(self):
        is_valid = False
        # Only do stuff if controller is connected
        if self.leap_controller.is_connected:
            hands = self.leap_controller.frame().hands
            # Keep only if there is a hand
            if len(hands) > 0:
                if self.supervised is True:
                    # Give user control when to obtain data
                    raw_input("\rSystem       :       Valid hand(s) detected --> Press any key to get data: "),
                    # Get the latest frame again
                    hands = self.leap_controller.frame().hands

                    if len(hands) > 0:
                        is_valid = True
                    else:
                        print("\rSystem       :       Previously detected hand is not visible - Please try again"),
                else:
                    hands = self.leap_controller.frame().hands
                    if len(hands) > 0:
                        is_valid = True
            else:
                print("\rSystem       :       No hand(s) detected - Please try again"),
        return is_valid

    def unsupervised_data_validation(self):
        if self.leap_controller.is_connected:
            hands = self.leap_controller.frame().hands

            if len(hands) > 0:
                hand = hands[0]
                return True, hand
            else:
                return False, None
        else:
            return False, None


