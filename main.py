from GestureBPs import thumbs_up
from cv2 import imread

thumb_detector = thumbs_up.Thumbs_Up()

image_thumbs = imread("thumbs3.jpeg")

thumb_detector.get_image(image_thumbs)
thumb_detector.detect_landmark()
if (thumb_detector.detector.handLms):
    print(thumb_detector.detect_gesture())
else:
    print("Nonetype")
