from time import sleep
from cv2 import VideoCapture, imshow
from HardCodeRecog.detector import Hand_Detector
from drawing_utils import Drawing_Utils
from json import load


class WebcamException(Exception):
    def __str__():
        return "An error has occured while trying to reach webcam. Please try again with a different webcam or port."


class Calibration():
    def __init__(self) -> None:
        """
        Calibration isn't ready for use. This class will be available to be used in other versions.
        """
        self.dutils = Drawing_Utils()

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

    def calibration(self, error_threshold=0.1) -> None:
        """
        Calibrates the distance between certain landmarks.\n
        error_threshold ==> Small error percentage to be added after calibration.
        open_threshold ==> Difference between the open and closed acts of fingers. 
        """

        self.detector = Hand_Detector(mode=True)
        while True:
            _, frame = self.vcap.read()
            if _:
                self.dutils.put_text(frame, "Show Your Hand with Fingers Open")
                imshow("Calibration", frame)

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
