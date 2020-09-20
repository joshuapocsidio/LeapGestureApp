import leapio.LeapIO as io

class LeapHandAcquisitor:
    def __init__(self, leap_controller, supervised=False, verbose=False):
        self.leap_controller = leap_controller
        self.verbose = verbose
        self.supervised = supervised

        pass

    def acquire_single_hand_data(self):
        if self.leap_controller.is_connected:
            hands = self.leap_controller.frame().hands

            if len(hands) > 0:
                hand = hands[0]
                return hand
        else:
            return None

    def acquire_multiple_hand_data(self, subject, iterations=100, intervals=10):
        hand_set = []
        counter = 0

        while counter < iterations:
            hand = self.acquire_single_hand_data()
            # Acquire hand data
            if hand is not None:
                hand_set.append(hand)
                counter += 1

            # If counter is at interval, prompt user
            if counter % intervals == 0:
                if counter == intervals:
                    raw_input("\nSystem       :       Gesture Checkpoint reached. Press any key to continue"),
                else:
                    raw_input("\nSystem       :       Press any key to get data: "),

        # Save pickle of hand data set
        io.save_hand_pickle(data=hand_set, subject=subject)


