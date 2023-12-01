import cv2
import numpy as np
import time
import serial
import threading

class ArduinoController:
    def __init__(self, arduino_port, baud_rate=9600):
        self.arduino_port = arduino_port
        self.baud_rate = baud_rate
        self.ser = None
        self.user_input = None
        self.input_thread = threading.Thread(target=self.user_input_thread)
        self.running = False
        

    def set_user_input(self, command):
        # Set the user input command
        self.user_input = command

    def send_command(self, command):
        # Send the command to Arduino
        try:
            if self.ser is not None and self.ser.is_open:
                self.ser.write(command.encode())
                start_time = time.time()
                if self.ser is not None and self.ser.is_open:
                    self.ser.write(command.encode())
                processing_time = time.time() - start_time

                # reduce lag by minimizing sleep time to send signal
                time.sleep(max(0.1 - processing_time, 0))
        except serial.SerialException as e:           
            print(f"Error sending command: {e}")

    def user_input_thread(self):
        # Thread for handling user input
        while self.running:
            if self.user_input is not None:
                # Send the command to Arduino depending on user input
                self.send_command(self.user_input)
                self.user_input = None  # Reset user_input after sending the command

    def start(self):
        # Start the communication thread
        try:
            self.ser = serial.Serial(self.arduino_port, self.baud_rate, timeout=1)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return

        self.running = True
        self.input_thread.start()

    def stop(self):
        # Stop the communication thread and close the serial port
        self.running = False
        if self.input_thread.is_alive():
            self.input_thread.join()  # Wait for the input thread to finish
        if self.ser is not None and self.ser.is_open:
            self.ser.close()

arduino_controller = ArduinoController(arduino_port='COM5')

def is_object_near_grey(grey_contour, non_grey_contours, min_distance=50):
    grey_x, grey_y, _, _ = cv2.boundingRect(grey_contour)
    
    for non_grey_contour in non_grey_contours:
        non_grey_x, non_grey_y, _, _ = cv2.boundingRect(non_grey_contour)
        distance = np.sqrt((grey_x - non_grey_x)**2 + (grey_y - non_grey_y)**2)
        
        if distance < min_distance:
            return True
    
    return False

try:
    # Start the communication thread between aduino and our program
    arduino_controller.start()

    # Open the camera stream
    camera = cv2.VideoCapture("http://10.10.129.19:8080/video?type=some.mjpeg")
    frequency = 10
    last_update = time.time()
    last_update2= time.time()
    tt = 0
    red_start = None

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # lower_grey = np.array([0], dtype=np.uint8)
    # upper_grey = np.array([70], dtype=np.uint8)
    lower_grey = np.array([0, 0, 60])
    upper_grey = np.array([180, 30, 140])

    green_time = 1
    blue_time = 2
    red_time = 4

    while True:
        ret, frame = camera.read()
        
        frame = cv2.resize(frame, (1000, 600))
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create masks for red, blue, green, and grey colors
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)

        # Find contours for each color
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_grey, _ = cv2.findContours(mask_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        red_count = 0 
        for contour in contours_red:
            if cv2.contourArea(contour) > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                red_count += 1

        blue_count = 0 
        for contour in contours_blue:
            if cv2.contourArea(contour) > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                blue_count += 1

        green_count = 0 
        for contour in contours_green:
            if cv2.contourArea(contour) > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                green_count += 1

        grey_count = 0
        for grey_contour in contours_grey:
            if cv2.contourArea(grey_contour) > 100:
                x, y, w, h = cv2.boundingRect(grey_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 128, 128), 2)
                grey_count += 1

                # Check if any non-grey object is close to the grey object (gas pump)
                cur_time = time.time()
                if cur_time - last_update2 >= 1:
                    if is_object_near_grey(grey_contour, contours_red + contours_blue + contours_green):
                        cv2.putText(frame, 'Near Non-Grey', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                        # Check if the light has been red for 8 seconds
                        if red_start is None:
                            red_start = cur_time
                        elif cur_time - red_start >= 8:
                            arduino_controller.set_user_input("2")  # set to yellow light if red for more than 8 secs
                        else:
                            arduino_controller.set_user_input("1")  # set to red light
                    else:
                        arduino_controller.set_user_input("3")  # set to green if no object is near grey
                        red_start = None  # Reset the timer when car leaves
                    last_update2 = cur_time

        total_count = red_count + blue_count + green_count
        current_time = time.time()
        if current_time - last_update >= frequency:
            if (total_count <= grey_count or grey_count == 0):
                tt = 0
            else:
                tt = ((red_count*red_time) + (blue_count*blue_time) + (green_count*green_time)) / grey_count
            last_update = current_time

        # Display # of each object type on the frame
        cv2.putText(frame, f'Red: {red_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(frame, f'Blue: {blue_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.putText(frame, f'Green: {green_count}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, f'Grey: {grey_count}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(frame, f'Time: {int(tt)} mins', (frame.shape[1] - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): #if q pressed exit program
            break

finally:
    # Stop the communication thread and end cv windows
    arduino_controller.stop()
    camera.release()
    cv2.destroyAllWindows()