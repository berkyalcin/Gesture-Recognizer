from time import sleep
from cv2 import VideoCapture, imshow
from HardCodeRecog.detector import Hand_Detector
from json import load


class WebcamException(Exception):
    def __str__():
        return "An error has occured while trying to reach webcam. Please try again with a different webcam or port."


class _Utils:
    def __init__(self):
        self.detector = Hand_Detector()

    def distance_calculator(self, x1, x2, y1, y2) -> int:
        """Finds the euclidian distance between two object, without taking the square root for the sake of optimization"""
        return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)

    def detect_closest_hand(self, img) -> list:
        """Chooses the closest hand to the camera, considering the user is the closest to the camera.\n
        Returns a list of landmarks of the closest hand."""
        self.detector.detect_landmark(img)
        hands_distance = {}
        if self.detector.handLms:
            for hand in self.detector.handLms:
                self.detector.detect_landmark(img)
                distance = self.distance_calculator(self.detector.pinky_mcp.x,
                                                    self.detector.thumb_mcp.x,
                                                    self.detector.pinky_mcp.y,
                                                    self.detector.thumb_mcp.y)
                hands_distance[distance] = self.detector.handLms

            return hands_distance[max(hands_distance.keys())]
        else:
            return None


class Gesture:
    """
    Main class to detect gestures. Necessary functions and variables are declared.\n
    Subclasses of gestures to be recognized:\n
    - Show Palm\n
    - Thumbs Up\n
    - Middle Finger\n
    """

    def __init__(self):
        self.utils = _Utils()
        self.detector = Hand_Detector(maxHands=5, mode=False)

        self.show_palm = False
        self.thumbs_up = False
        self.middle_finger = False

        self.one_finger = False
        self.two_finger = False
        self.three_finger = False
        self.four_finger = False
        self.five_finger = False

        # False ==> Closed
        # True ==> Open
        self.__thumb_open = False
        self.__index_open = False
        self.__middle_open = False
        self.__ring_open = False
        self.__pinky_open = False

        self.vcap = VideoCapture(0)

    def __detect_thumb_open(self, pinky_mcp, thumb_tip, threshold=0.25) -> None:
        """
        Detects if the thumb is open or not.\n
        Works by taking the distance between pinky_mcp and thumb_tip\n
        Threshold is in default set to 0.25
        """
        if self.utils.distance_calculator(pinky_mcp.x, thumb_tip.x, pinky_mcp.y, thumb_tip.y) > threshold:
            self.__thumb_open = True
        else:
            self.__thumb_open = False

    def __detect_index_open(self, thumb_mcp, index_tip, threshold=0.15) -> None:
        """
        Detects if the index is open or not.\n
        Works by taking the distance between thumb_mcp and index_tip\n
        Threshold is in default set to 0.25
        """
        if self.utils.distance_calculator(thumb_mcp.x, index_tip.x, thumb_mcp.y, index_tip.y) > threshold:
            self.__index_open = True
        else:
            self.__index_open = False

    def __detect_middle_open(self, thumb_mcp, middle_tip, threshold=0.15) -> None:
        """
        Detects if the middle is open or not.\n
        Works by taking the distance between thumb_mcp and middle_tip\n
        Threshold is in default set to 0.25
        """
        if self.utils.distance_calculator(thumb_mcp.x, middle_tip.x, thumb_mcp.y, middle_tip.y) > threshold:
            self.__middle_open = True
        else:
            self.__middle_open = False

    def __detect_ring_open(self, wrist, ring_tip, threshold=0.35) -> None:
        """
        Detects if the ring is open or not.\n
        Works by taking the distance between wrist and ring_tip\n
        Threshold is in default set to 0.25
        """
        if self.utils.distance_calculator(wrist.x, ring_tip.x, wrist.y, ring_tip.y) > threshold:
            self.__ring_open = True
        else:
            self.__ring_open = False

    def __detect_pinky_open(self, wrist, pinky_dip, threshold=0.45) -> None:
        """
        Detects if the pinky is open or not.\n
        Works by taking the distance between wrist and pinky_dip\n
        Threshold is in default set to 0.25
        """
        if self.utils.distance_calculator(wrist.x, pinky_dip.x, wrist.y, pinky_dip.y) > threshold:
            self.__pinky_open = True
        else:
            self.__pinky_open = False

    def __calibration_func(self, finger_1, finger_2, open_threshold=0.03):
        """A function to detect necessary distances."""
        open_value = self.utils.distance_calculator(
            self.detector.thumb_tip.x, self.detector.pinky_mcp.x, self.detector.thumb_tip.y, self.detector.pinky_mcp.y)
        while True:
            _, frame = self.vcap.read()

            key = input("")
            if key == "q" or key == "p":
                closestLms = self.utils.detect_closest_hand(frame)
                print(closestLms)
                self.detector.detect_landmark(frame, closestLms)
                distance = self.utils.distance_calculator(
                    finger_1.x, finger_2.x, finger_1.y, finger_2.y)

                if distance - open_value > open_threshold:
                    print(distance)
                    break
                else:
                    print(distance - open_value)
                    self.calibration()

            return distance

    def __calibration_append_to_json(self, distance_max, distance_min, distance_max_key, distance_min_key, file_name="calibration.json", json_main_branch="calibrationFile"):
        """A function that appends the distance to the given json object."""
        with open(file_name, "a") as f:
            json_file = load(f)
            json_file[json_main_branch][distance_max_key] = distance_max
            json_file[json_main_branch][distance_min_key] = distance_min

    def calibration_main(self, error_threshold=0.1) -> None:
        """
        Calibrates the distance between certain landmarks.\n
        error_threshold ==> Small error percentage to be added after calibration.
        open_threshold ==> Difference between the open and closed acts of fingers. 
        """
        print("Calibration allows the detector to work better, configured with your hand.\n Show your hand to the camera, with your fingers open.")
        self.detector = Hand_Detector(mode=True)
        while True:
            _, frame = self.vcap.read()
            if _:
                key = input()
                if key:
                    closestLms = self.utils.detect_closest_hand(frame)
                    self.detector.detect_landmark(frame, closestLms)
                    break
            else:
                raise WebcamException

        # Comparing open value
        open_value = self.utils.distance_calculator(
            self.detector.thumb_tip.x, self.detector.pinky_mcp.x, self.detector.thumb_tip.y, self.detector.pinky_mcp.y)

        # Thumb calibration
        print("--------------------------------------------------------------------------")
        print("Close your thumb. When it is closed, press q or p:")
        distance = self.__calibration_func(
            self.detector.thumb_tip, self.detector.pinky_mcp)
        self.__calibration_append_to_json(
            distance+error_threshold, distance-error_threshold, "thumb_distance_max", "thumb_distance_min")

        # Index calibration
        print("---------------------------------------------------------------------------")
        print("Close your index. When it is closed, pressed q or p.")
        distance = self.__calibration_func(
            self.detector.thumb_mcp, self.detector.index_finger_tip)
        self.__calibration_append_to_json(
            distance+error_threshold, distance-error_threshold, "index_distance_max", "index_distance_min")

        # Middle calibration
        print("---------------------------------------------------------------------------")
        print("Close your middle. When it is closed, pressed q or p.")
        distance = self.__calibration_func(
            self.detector.thumb_mcp, self.detector.middle_finger_tip)
        self.__calibration_append_to_json(
            distance+error_threshold, distance-error_threshold, "middle_distance_max", "middle_distance_min")

        # Ring calibration
        print("---------------------------------------------------------------------------")
        print("Close your ring. When it is closed, pressed q or p.")
        distance = self.__calibration_func(
            self.detector.thumb_mcp, self.detector.ring_finger_tip)
        self.__calibration_append_to_json(
            distance+error_threshold, distance-error_threshold, "ring_distance_max", "ring_distance_min")

        # Pinky calibration
        print("---------------------------------------------------------------------------")
        print("Close your pinky. When it is closed, pressed q or p.")
        distance = self.__calibration_func(
            self.detector.thumb_mcp, self.detector.pinky_tip)
        self.__calibration_append_to_json(
            distance+error_threshold, distance-error_threshold, "pinky_distance_max", "pinky_distance_min")

    def test(self):
        """Just for test purposes."""
        with open("calibration.json", "r") as f:
            json_file = load(f)
            print(json_file["calibrationFile"])


if __name__ == "__main__":
    gesture = Gesture()
    gesture.test()
