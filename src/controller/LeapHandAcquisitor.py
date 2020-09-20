import leapio.LeapIO as io

class LeapHandAcquisitor:
    def __init__(self, leap_controller, supervised=False, verbose=False):
        self.leap_controller = leap_controller
        self.verbose = verbose
        self.supervised = supervised

        pass

    def acquire_single_hand_data(self):
        done = False
        # Keep attempting until valid hand
        while done is False:
            # Only acquire if controller is connected
            if self.leap_controller.is_connected:
                hands = self.leap_controller.frame().hands
                # Only acquire if there are hands on screen
                if len(hands) > 0:
                    hand = hands[0]
                    return hand
            else:
                return None


    def acquire_multiple_hand_data(self, subject, iterations=100, intervals=10):
        hand_set = []
        i = 0
        while i < iterations:
            # Acquire hand data
            hand = self.test_get_hand_data()
            if hand is not None:
                print hand
                hand_set.append(self.test_get_hand_data())
                i += 1  # If counter is at interval, prompt user

            if i % intervals == 0:
                if i == intervals:
                    raw_input("\nSystem       :       Gesture Checkpoint reached. Press any key to continue"),
                else:
                    raw_input("\nSystem       :       Press any key to get data: "),


        # Save pickle of hand data set
        io.save_hand_pickle(data=hand_set, subject=subject)

        return hand_set

    def load_hand_data_set(self, subject):
        hand_data_set = io.load_hand_pickle(subject=subject)
        pass
