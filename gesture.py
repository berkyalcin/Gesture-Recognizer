from detector import Hand_Detector


class Gesture:
    def __init__(self):
        self.detector = Hand_Detector
        self.show_palm = False
        self.thumbs_up = False
        self.middle_finger = False

        self.one_finger = False
        self.two_finger = False
        self.three_finger = False
        self.four_finger = False
        self.five_finger = False

        self.__thumb_open = False
        self.__index_open = False
        self.__middle_open = False
        self.__ring_open = False
        self.__pinky_open = False

    def __detect_thumb_open(self, cmc, mcp, dip, tip):
        pass
