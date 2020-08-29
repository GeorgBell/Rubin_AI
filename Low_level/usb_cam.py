### File description
# The file contains functions and class for controlling
# the main camera connected via USB cable

### Packages import
import cv2
import time
from threading import Thread
from os import makedirs, path

### Auxiliary functions
def create_data_directory(sample_n):
    """
    Function creates a set of directories for scans,
    single images, and videos
    """
    scan_path = f"Captured/Sample_{sample_n}/Scan/"
    makedirs(path.dirname(scan_path), exist_ok=True)

    single_path = f'Captured/Sample_{sample_n}/Single/'
    makedirs(path.dirname(single_path), exist_ok=True)

    video_path = f'Captured/Sample_{sample_n}/Video/'
    makedirs(path.dirname(video_path), exist_ok=True)

    return {"scan":scan_path, "single":single_path, "video":video_path}

### Main class section
class MicroCamera():
    """
    Class for microscopic camera
    """

    def __init__(self, device_id=0, resolution=(1280,720), framerate=25, type="usb"):
        """
        Method initializes camera, sets up its parameters
        """
        if type == "usb":
            self.camera_open(device_id)
            self.camera_setup(resolution, framerate)
        elif type == "pi":
            self.pi_camera_open()
        self.record = None

    def pi_camera_open(self):
        """
        Method attaches, sets up and check pi camera
        """
        GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'
        self.cam = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
        if not (self.cap.isOpened()):
            print("Could not open video device")


    def camera_open(self, device_id):
        """
        Method attaches camera and checks it
        """
        self.cam = cv2.VideoCapture(device_id) # attach camera

        # Camera check
        if not (self.cam.isOpened()):
            print("Camera error")

    def record_open(self, sample_n, resolution=(1280,720), framerate=25):
        """
        Method initializes video recorder and sets record flag
        """
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fourcc = cv2.VideoWriter_fourcc('M',"J","P","G")
        self.out = cv2.VideoWriter(f'Captured/Sample_{sample_n}/Video/{timestr}.avi',
                                   fourcc, framerate, resolution)
        self.record = True


    def record_close(self):
        """
        Method changes record flag and releases recorder
        """
        self.record = False
        self.out.release()
     

    def camera_setup(self, resolution, framerate):
        """
        Method sets parameters of camera
        """
        self.cam.set(3, resolution[0]) # set width of image
        self.cam.set(4, resolution[1]) # set height of image
        self.cam.set(5, framerate) # set fps of video


    def camera_close(self):
        """
        Method releases camera resource
        """
        self.cam.release()


    def stream_start(self):
        """
        Method starts stream process in a separate thread
        """
        # start the thread to read frames from the video stream
        self.stopped = False
        t = Thread(target=self.stream_process, args=())
        #t.daemon = True
        t.start()
        return self


    def stream_process(self):
        """
        Method implements streaming logic
        """
        # Keep looping till the thread is stopped
        while True:
            ret, self.frame = self.cam.read()
            if self.record:
                self.out.write(self.frame)
            if self.stopped:
                return


    def yield_frame(self):
        """
        Method returns captured frame
        """
        return self.frame


    def stream_stop(self):
        """
        Method raises a flag to stop a streaming thread
        """
        # indicate that the thread should be stopped
        self.stopped = True


    def capture_autofocus_image(self):
        """
        Method captures a single image and transforms to gray-scale
        """
        image_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return image_gray


    def capture_scan_image(self, sample_n, loc_x, loc_y, *args):
        """
        Method captures an image during scanning procedure
        """
        cv2.imwrite(f'Captured/Sample_{sample_n}/Scan/{loc_x}_{loc_y}.jpg', self.frame)


    def capture_single_image(self, sample_n, loc_x, loc_y, *args):
        """
        Method captures a single image with coordinates
        """
        cv2.imwrite(f'Captured/Sample_{sample_n}/Single/{loc_x}_{loc_y}.jpg', self.frame)


if __name__ == "__main__":
    # Testing usb_cam.py module
    input("Create directory")
    create_data_directory(1)

    input("Open camera")
    micro_cam = MicroCamera(device_id=0)
    micro_cam.stream_start()


    input("Take a snapshot")
    micro_cam.capture_single_image(1,1,1)

    input("Start recording video")
    micro_cam.record_open(sample_n=1)
    input("Stop recording video")
    micro_cam.record_close()

    input("Stop camera")
    micro_cam.stream_stop()
    micro_cam.camera_close()