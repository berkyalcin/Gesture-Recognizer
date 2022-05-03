# Gesture Recognizer
 A library to recognize gestures, which can be implented easily in every Python project.
 Properties:
 - Gesture Recognization
 - Hand Detection
 - Hand Landmark Detection


# How Does It Recognize Gestures?
The library uses Mediapipe API to recognize the landmarks of the hand. Then, those the distances between the landmarks, location of the landmarks or the hand's position can be used to detect gestures. 

# Can Custom Gestures Be Implemented?
Yes, definitely. All predefined getsure classes are inherited from a main class called "Gesture". The main class carries the necessary functions to detest a gesture and use it in a project. 

# How to Use A Predefined Class?
1. First, the class should be initialized.
thumbup = Thumbs_Up()

2. An image should be uploaded to class with the ".get_image(image)" function. The image can be uploaded with the opencv library.
thumbup.get_image(frame)

3. Now, the gesture can be detected, using the function ".detect_gesture()". The function returns the result as a boolean.
result = thumbup.detect_gesture()
