### File description
# The file contains separate classes for each camera object:
# - single image capturing for autofocusing;
# -

### Packages import
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from cv2 import cvtColor, COLOR_BGR2GRAY
from time import sleep
import os
from subprocess import call


def create_data_directory(sample_n):
    scan_path = f'Captured/Sample_{sample_n}/Scan/'
    os.makedirs(os.path.dirname(scan_path), exist_ok=True)

    single_path = f'Captured/Sample_{sample_n}/Single/'
    os.makedirs(os.path.dirname(single_path), exist_ok=True)

    video_path = f'Captured/Sample_{sample_n}/Video/'
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
# Create directory for appropriate sample at first!
    
def capture_autofocus(resolution=(640, 480)):
    with PiCamera() as camera:
        camera.resolution = resolution
        rawCapture = PiRGBArray(camera)
        sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        gray = cvtColor(image, COLOR_BGR2GRAY)
        return gray

def capture_scan_image(sample_n, loc_x, loc_y, resolution=(640, 480)):
    with PiCamera() as camera:
        camera.resolution = resolution
        camera.start_preview()
        camera.preview.alpha = 128
        sleep(0.1)
        camera.capture(f'Captured/Sample_{sample_n}/Scan/{loc_x}_{loc_y}.jpg')
        # Difference only in path!!!



def capture_single_image(sample_n, loc_x, loc_y, resolution=(640, 480)):
    with PiCamera() as camera:
        camera.resolution = resolution
        camera.start_preview()
        camera.preview.alpha = 128
        sleep(0.1)
        camera.capture(f'Captured/Sample_{sample_n}/Single/{loc_x}_{loc_y}.jpg')



def capture_video(video_length, sample_n, loc_x, loc_y, resolution=(640, 480)):
    with PiCamera() as camera:
        camera.resolution = resolution
        camera.start_recording(f'Captured/Sample_{sample_n}/Video/{loc_x}_{loc_y}.h264')
        camera.wait_recording(video_length)
        camera.stop_recording()

def video_conversion():
    command = "MP4Box -add 1_1.h264 1_1.mp4"
    call([command], shell=True)

    
    
class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32, **kwargs):
        # initialize the camera
        self.camera = PiCamera()

        # set camera parameters
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        # set optional camera parameters (refer to PiCamera docs)
        for (arg, value) in kwargs.items():
            setattr(self.camera, arg, value)

        # initialize the stream
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


#(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)


### Class of single image capturing for autofocusing
#class CameraAutofocusShot:
    """
    Class contains:
    - ...
    """

#    def __init__(self, resolution=(320, 240)):
        # initialize the camera
#        self.camera = PiCamera()

        # set camera parameters
#        self.camera.resolution = resolution

        # set optional camera parameters (refer to PiCamera docs)
#        for (arg, value) in kwargs.items():
#            setattr(self.camera, arg, value)

        # initialize the stream
#        self.rawCapture = PiRGBArray(self.camera, size=resolution)
#        self.stream = self.camera.capture_continuous(self.rawCapture,
#            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
#        self.frame = None
#        self.stopped = False