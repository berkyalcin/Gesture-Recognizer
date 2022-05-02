from HardCodeRecog.gesture import Gesture


class High_Five(Gesture):
    def __init__(self):
        super().__init__()
        self.image: None
        self.detect: bool

    def get_image(self, image) -> None:
        """Loads np array of an image into the class."""
        self.image = image

    def detect_landmark(self) -> None:
        """Detects the landmark of the image. \n
        Landmarks can be called from Thumbs_Up.detector"""
        self.detector.detect_landmark(self.image)

    def detect_gesture(self):
        self._Gesture__detect_all(self.image)
        condition = (self._Gesture__thumb_open and self._Gesture__index_open,
                     self._Gesture__middle_open, self._Gesture__ring_open, self._Gesture__pinky_open)

        if condition:
            self.detect = True
            return True
        else:
            self.detect = False
            return False
