import time
from GestureBPs.thumbs_up import Thumbs_Up
from GestureBPs.high_five import High_Five
from HardCodeRecog.drawing_utils import Drawing_Utils
from setup import Setup
from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows
import cv2

# Necessary libraries are installed.
setup = Setup()

# Initialization of VCap for the usage of webcam.
vcap = VideoCapture(0)

# Predefined classes are initialized.
thumbup = Thumbs_Up()
highFive = High_Five()

# Drawing Utils are initialized.
dutils = Drawing_Utils()

while True:
    # All previous windows are destroyed.
    destroyAllWindows()

    # Frame from the webcam is read. More on the OpenCV Documentation.
    _, frame = vcap.read()

    # Images are fed into the classes and the landmarks are detected.
    thumbup.get_image(frame)
    thumbup.detect_landmark()
    highFive.get_image(frame)
    highFive.detect_landmark()

    result_thumb = False
    result_h5 = False

    # If a hand is detected, the gesture is detected.
    if thumbup.detector.handLms:
        result_thumb = thumbup.detect_gesture()
        result_h5 = highFive.detect_gesture()

        frame = dutils.draw_hand(
            frame, thumbup.detector.landmark_listX, thumbup.detector.landmark_listY)

    # Writes the results on the image.
    if result_thumb:
        dutils.put_text(frame, "Thumb_Up")

    elif result_h5:
        dutils.put_text(frame, "High Five")

    else:
        dutils.put_text(frame, "None")

    imshow("Image", frame)
    waitKey(10)
