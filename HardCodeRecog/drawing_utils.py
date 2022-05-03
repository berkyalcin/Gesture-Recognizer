from cv2 import LINE_AA, putText, rectangle, FONT_HERSHEY_SIMPLEX, circle, line


class Drawing_Utils():
    def __init__(self) -> None:
        pass

    def draw_hand(self, image, landmarksX, landmarksY):
        """
        Draws a contour box around the hand. \n
        Takes the arguments landmarksX and landmarksY, both can be obtained from Gesture.detector\n
        landmarksX = Gesture.detector.landmarksX\n
        landmarksY = Gesture.detector.landmarksY\n
        """
        h, w, c = image.shape
        x_min = min(landmarksX)
        y_min = min(landmarksY)
        x_max = max(landmarksX)
        y_max = max(landmarksY)

        x_max, x_min, y_max, y_min = x_max*w, x_min*w, y_max*h, y_min*h

        image = rectangle(image,
                          (round(x_min), round(y_min)),
                          (round(x_max), round(y_max)),
                          (0, 255, 0),
                          2)
        return image

    def put_text(self, image, text, color=(0, 255, 0), font=FONT_HERSHEY_SIMPLEX, font_scale=1, place=(50, 50), thickness=2):
        """
        Creates a text on the image.
        """
        image = putText(image, text, place, font, font_scale,
                        color, thickness, LINE_AA)
        return image

    def draw_landmark(self, image, landmark):
        """
        Draws the landmarks with the given posisions, which are between 1 and 0.
        """
        h, w, c = image.shape
        image = circle(image, (int(landmark.x*w), int(landmark.y*h)),
                       1, color=(0, 255, 0), thickness=-1)
        return image

    def draw_line(self, image, pt1, pt2):
        """
        Draws line between two points.\n
        Points should be given as landmarks.
        """
        h, w, c = image.shape
        image = line(image, (pt1.x*w, pt1.y*h), (pt2.x*w, pt2.y*h),
                     color=(0, 255, 0), thickness=1)

        return image
