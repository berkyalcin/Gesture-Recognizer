import time
from GestureBPs.thumbs_up import Thumbs_Up
from GestureBPs.high_five import High_Five
from HardCodeRecog.drawing_utils import Drawing_Utils
from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows
import cv2

vcap = VideoCapture(0)
thumbup = Thumbs_Up()
highFive = High_Five()
dutils = Drawing_Utils()

while True:
    destroyAllWindows()

    _, frame = vcap.read()

    thumbup.get_image(frame)
    thumbup.detect_landmark()
    highFive.get_image(frame)
    highFive.detect_landmark()

    result_thumb = False
    result_h5 = False

    if thumbup.detector.handLms:
        result_thumb = thumbup.detect_gesture()
        result_h5 = highFive.detect_gesture()

        frame = dutils.draw_hand(
            frame, thumbup.detector.landmark_listX, thumbup.detector.landmark_listY)

    if result_thumb:
        dutils.put_text(frame, "Thumb_Up")

    elif result_h5:
        dutils.put_text(frame, "High Five")

    else:
        dutils.put_text(frame, "None")

    imshow("Image", frame)
    waitKey(10)
