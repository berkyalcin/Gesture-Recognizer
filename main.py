from detector import Hand_Detector
from cv2 import VideoCapture

hdetector = Hand_Detector()

cap = VideoCapture(0)

while True:
    _, frame = cap.read()
    hdetector.detect_landmark(frame)
    print(hdetector.hand_x)
