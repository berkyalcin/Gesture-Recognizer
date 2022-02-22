from cv2 import VideoCapture, waitKey, imshow
from detector import Hand_Detector


class WebcamException(Exception):
    def __str__():
        return "An error has occured while trying to reach webcam. Please try again with a different webcam or port."


class Gesture:
    """
    Main class to detect gestures. Necessary functions and variables are declared.\n
    Gestures to be recognized:\n
    - Show Palm\n
    - Thumbs Up\n
    - Middle Finger\n
    """

    def __init__(self):
        self.detector = Hand_Detector(maxHands=5)
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

    def __distance_calculator(self, x1, x2, y1, y2) -> int:
        """Finds the euclidian distance between two object, without taking the square root for the sake of optimization"""
        return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)

    def __detect_thumb_open(self, pinky_mcp, thumb_tip, threshold=0.25) -> None:
        """
        Works by taking the distance between pinky_mcp and thumb_tip\n
        Threshold is in default set to 0.25
        """
        if self.__distance_calculator(pinky_mcp.x, thumb_tip.x, pinky_mcp.y, thumb_tip.y) > threshold:
            self.__thumb_open = True
        else:
            self.__thumb_open = False

    def __detect_index_open(self, thumb_mcp, index_tip, threshold=0.15) -> None:
        """
        Works by taking the distance between thumb_mcp and index_tip\n
        Threshold is in default set to 0.25
        """
        if self.__distance_calculator(thumb_mcp.x, index_tip.x, thumb_mcp.y, index_tip.y) > threshold:
            self.__index_open = True
        else:
            self.__index_open = False

    def __detect_middle_open(self, thumb_mcp, middle_tip, threshold=0.15) -> None:
        """
        Works by taking the distance between thumb_mcp and middle_tip\n
        Threshold is in default set to 0.25
        """
        if self.__distance_calculator(thumb_mcp.x, middle_tip.x, thumb_mcp.y, middle_tip.y) > threshold:
            self.__middle_open = True
        else:
            self.__middle_open = False

    def __detect_ring_open(self, wrist, ring_tip, threshold=0.35) -> None:
        """
        Works by taking the distance between wrist and ring_tip\n
        Threshold is in default set to 0.25
        """
        if self.__distance_calculator(wrist.x, ring_tip.x, wrist.y, ring_tip.y) > threshold:
            self.__ring_open = True
        else:
            self.__ring_open = False

    def __detect_pinky_open(self, wrist, pinky_dip, threshold=0.45) -> None:
        """
        Works by taking the distance between wrist and pinky_dip\n
        Threshold is in default set to 0.25
        """
        if self.__distance_calculator(wrist.x, pinky_dip.x, wrist.y, pinky_dip.y) > threshold:
            self.__pinky_open = True
        else:
            self.__pinky_open = False

    def __detect_users_hand(self,img) -> int:
        """Chooses the closest hand to the camera, considering the user is the closest to the camera."""
        self.detector.detect_landmark()

    def calibration(self, error_threshold=0.1) -> None:
        """
        Calibrates the distance between certain landmarks.\n
        error_threshold ==> Small error percentage to be added after calibration.
        """
        print("Calibration allows the detector to work better, configured with your hand.\n Show your hand to the camera, with your fingers open.")
        while True:
            _, frame = self.vcap.read()
            if _:
                self.detector.detect_landmark(frame)
                if self.detector.handLms:
                    break
            else:
                raise WebcamException
        print("--------------------------------------------------------------------------")
        print("Close your thumb. When it is closed, press q or p:")
        while True:
            _, frame = self.vcap.read()
            self.detector.detect_landmark(frame)
            distance = self.__distance_calculator(
                self.detector.thumb_tip.x, self.detector.pinky_mcp.x, self.detector.thumb_tip.y, self.detector.pinky_mcp.y)
            key = input("")
            if key == "q" or key == "p":
                print(distance)
                break

    def test(self):
        while True:
            _, frame = self.vcap.read()
            self.detector.detect_landmark(frame)
            if self.detector.handLms:
                print(self.detector.thumb_tip.x)
                """print(self.detector.index_finger_tip)
                print(self.detector.middle_finger_tip)
                print(self.detector.ring_finger_tip)
                print(self.detector.pinky_tip)"""


if __name__ == "__main__":
    gesture = Gesture()
    gesture.calibration()
