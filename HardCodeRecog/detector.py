from mediapipe import solutions
from cv2 import cvtColor, COLOR_BGR2RGB


class Hand_Detector:
    def __init__(self, mode=False, maxHands=3, detectCon=0.9, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpHands = solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands)
        self.mpDraw = solutions.drawing_utils
        self.cltime = 0

        self.handLms = None

        self.hand_x = None
        self.hand_y = None

        self.wrist = None

        self.thumb_cmc = None
        self.thumb_mcp = None
        self.thumb_dip = None
        self.thumb_tip = None

        self.index_finger_mcp = None
        self.index_finger_pip = None
        self.index_finger_dip = None
        self.index_finger_tip = None

        self.middle_finger_mcp = None
        self.middle_finger_pip = None
        self.middle_finger_dip = None
        self.middle_finger_tip = None

        self.ring_finger_mcp = None
        self.ring_finger_pip = None
        self.ring_finger_dip = None
        self.ring_finger_tip = None

        self.pinky_mcp = None
        self.pinky_pip = None
        self.pinky_dip = None
        self.pinky_tip = None

        self.landmark_listX: list
        self.landmark_listY: list

    # Detecting hand landmarks

    def __detect_hand(self, img) -> dict:
        img = cvtColor(img, COLOR_BGR2RGB)
        results = self.hands.process(img)
        self.handLms = results.multi_hand_landmarks

    def detect_landmark(self, img, handLms=None) -> None:
        # Detects and stores the hand landmarks.
        # Uses __detect_hand if there handLms is not give. Otherwise, uses the given handLms
        self.__detect_hand(img)
        if self.handLms:
            if handLms:
                self.handLms = handLms

            self.hand_x = self.handLms[0].landmark[0].x
            self.hand_y = self.handLms[0].landmark[0].y

            self.wrist = self.handLms[0].landmark[0]

            self.thumb_cmc = self.handLms[0].landmark[1]
            self.thumb_mcp = self.handLms[0].landmark[2]
            self.thumb_dip = self.handLms[0].landmark[3]
            self.thumb_tip = self.handLms[0].landmark[4]

            self.index_finger_mcp = self.handLms[0].landmark[5]
            self.index_finger_pip = self.handLms[0].landmark[6]
            self.index_finger_dip = self.handLms[0].landmark[7]
            self.index_finger_tip = self.handLms[0].landmark[8]

            self.middle_finger_mcp = self.handLms[0].landmark[9]
            self.middle_finger_pip = self.handLms[0].landmark[10]
            self.middle_finger_dip = self.handLms[0].landmark[11]
            self.middle_finger_tip = self.handLms[0].landmark[12]

            self.ring_finger_mcp = self.handLms[0].landmark[13]
            self.ring_finger_pip = self.handLms[0].landmark[14]
            self.ring_finger_dip = self.handLms[0].landmark[15]
            self.ring_finger_tip = self.handLms[0].landmark[16]

            self.pinky_mcp = self.handLms[0].landmark[17]
            self.pinky_pip = self.handLms[0].landmark[18]
            self.pinky_dip = self.handLms[0].landmark[19]
            self.pinky_tip = self.handLms[0].landmark[20]

            self.landmark_listX = [self.thumb_cmc.x, self.thumb_mcp.x, self.thumb_dip.x, self.thumb_tip.x,
                                   self.index_finger_dip.x, self.index_finger_mcp.x, self.index_finger_pip.x, self.index_finger_tip.x,
                                   self.middle_finger_dip.x, self.middle_finger_mcp.x, self.middle_finger_pip.x, self.middle_finger_tip.x,
                                   self.ring_finger_dip.x, self.ring_finger_mcp.x, self.ring_finger_mcp.x, self.ring_finger_dip.x, self.ring_finger_tip.x,
                                   self.pinky_dip.x, self.pinky_mcp.x, self.pinky_pip.x, self.pinky_tip.x]

            self.landmark_listY = [self.thumb_cmc.y, self.thumb_mcp.y, self.thumb_dip.y, self.thumb_tip.y,
                                   self.index_finger_dip.y, self.index_finger_mcp.y, self.index_finger_pip.y, self.index_finger_tip.y,
                                   self.middle_finger_dip.y, self.middle_finger_mcp.y, self.middle_finger_pip.y, self.middle_finger_tip.y,
                                   self.ring_finger_dip.y, self.ring_finger_mcp.y, self.ring_finger_mcp.y, self.ring_finger_dip.y, self.ring_finger_tip.y,
                                   self.pinky_dip.y, self.pinky_mcp.y, self.pinky_pip.y, self.pinky_tip.y]
