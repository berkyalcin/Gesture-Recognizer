from HardCodeRecog.gesture import Gesture


class Thumbs_Up(Gesture):
    def __init__(self):
        super().__init__()
        self.image: None
        self.detect: bool

    def get_image(self, image) -> None:
        """Loads np array of an image into the class."""
        self.image = image

    def detect_landmark(self):
        """Detects the landmark of the image. \n
        Landmarks can be called from Thumbs_Up.detector"""
        self.detector.detect_landmark(self.image)

    def detect_gesture(self):
        self._Gesture__detect_all(self.image)
        condition = (self.detector.thumb_tip.y == min(self.detector.landmark_listY) and not(
            self._Gesture__index_open) and not(self._Gesture__middle_open and not(self._Gesture__ring_open) and not(self._Gesture__pinky_open) and self._Gesture__thumb_open))
        """print(self.detector.thumb_tip.y)
        print(self.detector.landmark_listY.index(
            min(self.detector.landmark_listY)))
        print(self._Gesture__index_open)
        print(self._Gesture__middle_open)
        print(self._Gesture__pinky_open)
        print(self._Gesture__ring_open)
        print(self._Gesture__thumb_open)
        print("********************************")"""
        if condition:
            self.detect = True
            return True
        else:
            self.detect = False
            return False
