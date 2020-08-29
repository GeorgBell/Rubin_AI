from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def Capture_image_pi():
    with PiCamera() as camera:
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray
    

    


    
       
    
    



