import cv2
import numpy as np

# Open the camera stream
camera = cv2.VideoCapture("http://10.10.140.173:8080/video?type=some.mjpeg")

# Define the lower and upper bounds for the red color in the HSV color space
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Define the lower and upper bounds for the blue color in the HSV color space
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([130, 255, 255])

# Define the lower and upper bounds for the green color in the HSV color space
lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

while True:
    ret, frame = camera.read()
    
    frame = cv2.resize(frame, (1000, 600))
    
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create masks for red, blue, and green colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # Find contours and draw rectangles for red objects
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_red:
        if cv2.contourArea(contour) > 100:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # Find contours and draw rectangles for blue objects
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_blue:
        if cv2.contourArea(contour) > 100:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Find contours and draw rectangles for green objects
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_green:
        if cv2.contourArea(contour) > 100:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
camera.release()

# Close the OpenCV window
cv2.destroyAllWindows()
