import time

import cv2
import mediapipe as mp


class handDetector:
    def __init__(
        self,
        image_mode=False,                   # Whether to treat input images as static images or as a continuous stream
        max_num_hands=3,                    # Maximum number of hands to detect in the frame
        modelComplexity=1,                  # Model complexity: higher value increases accuracy but reduces speed
        min_detection_confidence=0.5,       # Minimum confidence required for initial hand detection
        min_tracking_confidence=0.5,        # Minimum confidence required for tracking hand landmarks
    ):
        # Initializing variables with provided arguments or default values
        self.image_mode = image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.modelComplex = modelComplexity

        # Initialize MediaPipe's hands solution
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(
            self.image_mode,
            self.max_num_hands,
            self.modelComplex,
            self.min_detection_confidence,
            self.min_tracking_confidence,
        )
        # Drawing utility for rendering hand landmarks and connections
        self.mpdraw = mp.solutions.drawing_utils  
        # Indices of finger tip landmarks for thumb, index, middle, ring, and pinky
        self.finger_tip_id = [4, 8, 12, 16, 20]  

    def findHands(self, img, draw=True):
        """
        This method processes the input image to detect hands, and optionally draws hand landmarks on the image.
        
        Args:
        - img: Input image (in BGR format)
        - draw: Flag to indicate if the landmarks should be drawn on the image (default is True)
        
        Returns:
        - img: Image with detected hand landmarks drawn (if draw=True)
        """
        # Convert BGR image to RGB, as MediaPipe requires RGB input
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image and detect hands
        self.results = self.hands.process(imgRGB)

        # Check if any hands are detected
        if self.results.multi_hand_landmarks:
            # Loop through each detected hand
            for i in self.results.multi_hand_landmarks:
                if draw:
                    # Draw hand landmarks and connections on the original image
                    self.mpdraw.draw_landmarks(img, i, self.mphands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, hand_num=0, draw=True):
        """
        This method extracts and returns the pixel positions of hand landmarks.
        
        Args:
        - img: Input image
        - hand_num: Index of the hand to extract landmarks from (default is 0, which is the first hand)
        - draw: Flag to indicate if circles should be drawn on each landmark (default is True)
        
        Returns:
        - lm_list: List of [ID, x, y] for each detected landmark
        """
        # List to store hand landmark positions
        self.lm_list = []
        # Check if hand landmarks are detected
        if self.results.multi_hand_landmarks:
            # Select the hand (based on hand_num) from the results
            myHand = self.results.multi_hand_landmarks[hand_num]  
            for id, lm in enumerate(myHand.landmark):
                # Convert normalized landmarks to pixel coordinates
                h, w, c = img.shape  # Get dimensions of the image
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convert landmark positions to pixel positions
                self.lm_list.append([id, cx, cy])  # Store ID, x, and y positions

                if draw:
                    # Draw a small circle at each landmark point (for visualization)
                    cv2.circle(
                        img,
                        center=(cx, cy),
                        radius=3,
                        color=(255, 255, 255),
                        thickness=1,
                    )
        return self.lm_list

    def fingerStatus(self):
        """
        This method checks and returns the status (open/closed) of all five fingers based on landmark positions.
        
        Returns:
        - fingers: List containing the status of each finger (1 for open, 0 for closed)
        """
        fingers = []

        # Check thumb status: If thumb tip is to the left of its joint, it's considered open
        if (
            self.lm_list[self.finger_tip_id[0]][1]  # x-coordinate of thumb tip
            < self.lm_list[self.finger_tip_id[0] - 1][1]  # x-coordinate of the knuckle-joint just below the tip of thumb
        ):
            # Thumb is open (i)
            fingers.append(1)
        else:
            # Thumb is closed
            fingers.append(0)

        # Check status of other four fingers (index, middle, ring, pinky)
        for i in range(1, 5):
            # Compare y-coordinates of the finger tip (landmarks 8, 12, 16, 20) and the knuckle-joint two steps below it (landmarks 6, 10, 14, 18)
            if (
                self.lm_list[self.finger_tip_id[i]][2]  # y-coordinate of the fingertip
                < self.lm_list[self.finger_tip_id[i] - 2][2]  # y-coordinate of the second knuckle
            ):
                # Finger is open (ii)
                fingers.append(1)
            else:
                # Finger is closed
                fingers.append(0)

        return fingers


def main():
    cap = cv2.VideoCapture(0)  # Open the default camera (0 usually represents the first camera device)
    previousT = 0  # To calculate frames per second (FPS)
    currentT = 0

    detector = handDetector()  # Create an instance of the handDetector class

    while True:
        ret, img = cap.read()  # Capture frame from the webcam

        img = detector.findHands(img, draw=True)  # Detect hands in the frame and draw landmarks
        landmark_list = detector.findPosition(img)  # Get the list of hand landmark positions
        
        if len(landmark_list) != 0:
            # If landmarks are detected, print the position of landmark 2 (index finger joint)
            print(landmark_list[2])

        # Calculate the FPS
        currentT = time.time()
        fps = 1 / (currentT - previousT)
        previousT = currentT

        # Display FPS on the screen
        cv2.putText(
            img,
            "Client FPS:" + str(int(fps)),
            (10, 70),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2,
            color=(255, 0, 0),
        )

        # Display the frame in a window titled "img"
        cv2.imshow("img", img)
        cv2.waitKey(1)  # Wait for 1 millisecond and then move to the next frame


if __name__ == "__main__":
    main()



# -------------------------------------------------------------------------------------

# Notes:

# (i): If the x-coordinate of the tip of the thumb (landmark point-4) is to the left of the x-coordinate of the knuckle joint (landmark point-3, just below it), 
# the thumb is considered open (this usually happens when right hand palm is opened with fingers stretched out).
#
# (ii): If the y-coordinate of the tip of a finger (index, middle, ring, or little finger) is logically higher ('>') than the y-co-ordinate of the 2nd knuckle joint below it (just observe that when you close your fist and the fingers are not raised, then this condition is satisfied) then it indicates the finger is UP, correct?

# So why have we used the '<' sign?

# Reason: in OpenCV, the origin of the coordinate system is always at the top-left corner of the image or canvas. This is a standard convention used in many image processing libraries, including OpenCV. Hence the greater-than sign '>' is changed to lesser-than sign '<' for the logic to work properly, because we are measuring height in top-down fashion, so our Y-axis is upside-down (inverted).

# -------------------------------------------------------------------------------------