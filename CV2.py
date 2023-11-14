import cv2
import numpy as np

# Open the camera stream
camera = cv2.VideoCapture("http://10.10.134.49:8080/video?type=some.mjpeg")

# Define the lower and upper bounds for the red color in the HSV color space
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

while True:
    ret, frame = camera.read()
    
    frame = cv2.resize(frame, (1000, 600))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the frame to the HSV color space
    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Draw rectangles around red objects
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()

# Close the OpenCV window
cv2.destroyAllWindows()
