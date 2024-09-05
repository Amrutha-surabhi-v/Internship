import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize background frame
ret, frame1 = cap.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

motion_detected = False
static_frame_threshold = 100
 # Adjust this threshold for sensitivity

while True:
    # Capture the current frame
    ret, frame2 = cap.read()
    if not ret:
        break

    # Convert to grayscale and blur for better motion detection
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # Compute the absolute difference between the current frame and the previous one
    frame_diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # Dilate the threshold image to fill in holes, then find contours
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found, motion is detected
    if len(contours) > 0:
        motion_detected = True
        cv2.putText(frame2, "Person Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    else:
        cv2.putText(frame2, "Picture Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Display the frames with detection text
    cv2.imshow("Webcam", frame2)

    # Update the previous frame for next iteration
    gray1 = gray2

    

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
