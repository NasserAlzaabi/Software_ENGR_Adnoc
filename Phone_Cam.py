import cv2
import numpy as np
import urllib.request
import ssl

# Disable SSL certificate verification
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# URL for your camera stream (make sure it's a valid URL)
url = 'http://10.249.208.35:8080'  # Add http:// to the URL if it's an HTTP stream

while True:
    # Open the URL and read the image data
    with urllib.request.urlopen(url) as imgResp:
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        
        # Display the video frame as it is
        
        cv2.imshow('Video Stream', img)
        
        # Check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()

