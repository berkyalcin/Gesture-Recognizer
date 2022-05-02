from matplotlib import image
from GestureBPs import thumbs_up
from setup import Setup
from cv2 import imread

setup = Setup()

thumb_detector = thumbs_up.Thumbs_Up()
thumb_detector1 = thumbs_up.Thumbs_Up()

image_thumbs = imread("thumbs3.jpeg")
image_thumbs1 = imread("thumb1.png")

thumb_detector.get_image(image_thumbs)
thumb_detector1.get_image(image_thumbs1)

thumb_detector.detect_landmark()
thumb_detector1.detect_landmark()

if (thumb_detector.detector.handLms and thumb_detector1.detector.handLms):
    print(thumb_detector.detect_gesture())
    print(thumb_detector1.detect_gesture())
else:
    print("Nonetype")
