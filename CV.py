import cv2
import numpy as np

# Open the camera stream
camera = cv2.VideoCapture("http://192.168.1.215:8080/video?type=some.mjpeg")

lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

lower_blue = np.array([100, 100, 100])
upper_blue = np.array([130, 255, 255])

lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

lower_grey = np.array([0, 0, 50])
upper_grey = np.array([180, 30, 220])

while True:
    ret, frame = camera.read()
    
    frame = cv2.resize(frame, (1000, 600))
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create masks for red, blue, green, and grey colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)

    # Color red objects and count rectangles
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_count = 0 
    for contour in contours_red:
        if cv2.contourArea(contour) > 100:  
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            red_count += 1 #add to count of objects for every red object found


    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_count = 0 
    for contour in contours_blue:
        if cv2.contourArea(contour) > 100: 
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            blue_count += 1  # Increment count


    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_count = 0  # Reset count
    for contour in contours_green:
        if cv2.contourArea(contour) > 100:  
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            green_count += 1  # Increment count


    contours_grey, _ = cv2.findContours(mask_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    grey_count = 0  # Reset count
    for contour in contours_grey:
        if cv2.contourArea(contour) > 100:  
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 128, 128), 2)
            grey_count += 1  # Increment count
    # Display counts on the frame
    cv2.putText(frame, f'Red: {red_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Blue: {blue_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f'Green: {green_count}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'Grey: {grey_count}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)

    #Dayeh u can add ur part here.

    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()

# Close CV windows when infinite loop is exited (q is pressed or X)
cv2.destroyAllWindows()