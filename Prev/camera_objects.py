### File description
# The file contains classes for camera object

### Packages import
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from cv2 import cvtColor, imwrite, COLOR_BGR2GRAY
from time import sleep
from os import makedirs, path
from subprocess import call


def create_data_directory(sample_n):
    """
    Function that creates a set of directories for scans,
    single images, and videos
    """
    scan_path = f'Captured/Sample_{sample_n}/Scan/'
    makedirs(path.dirname(scan_path), exist_ok=True)

    single_path = f'Captured/Sample_{sample_n}/Single/'
    makedirs(path.dirname(single_path), exist_ok=True)

    video_path = f'Captured/Sample_{sample_n}/Video/'
    makedirs(path.dirname(video_path), exist_ok=True)

    return {"scan":scan_path, "single":single_path, "video":video_path}


def video_conversion(path):
    """
    Function required for video conversion from h264 to mp4
    """
    command = "MP4Box -add " + path + " " + path[:-4] + "mp4"
    call([command], shell=True)


class PiCameraStream:
    """
    Class of camera that is continuously streams images.
    All methods, that capture images, grab a frame from the stream.
    Two methods of recording video are presented: with interrupting 
    the videostream and without
    """

    def __init__(self, resolution=(1920, 1080), framerate=25, **kwargs):
        """
        Method of initialization of camera resolution and framerate.
        Also opens access to camera
        """
        self.resolution = resolution
        self.framerate = framerate
        self.camera_open()


    def camera_open(self):
        """
        Method opens access to Pi camera and sets resolution & framerate
        """
        self.camera = PiCamera()

        self.set_resolution_framerate()

        self.frame = None
        self.stopped = False


    def camera_close(self):
        """
        Method closes access to Pi camera
        """
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()


    def set_resolution_framerate(self):
        """
        Method sets resolution & framerate of the camera
        """
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate

        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)


    def stream_start(self):
        """
        Method starts a thread with streaming
        """
        # start the thread to read frames from the video stream
        t = Thread(target=self.stream_process, args=())
        t.daemon = True
        t.start()
        return self


    def stream_process(self):
        """
        Method implements streaming logic
        """

        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.camera_close()
                return


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
        image_gray = cvtColor(self.frame, COLOR_BGR2GRAY)
        return image_gray


    def capture_scan_image(self, sample_n, loc_x, loc_y):
        """
        Method captures an image during scanning procedure
        """
        cv2.imwrite(f'Captured/Sample_{sample_n}/Scan/{loc_x}_{loc_y}.jpg', self.frame)


    def capture_single_image(self, sample_n, loc_x, loc_y):
        """
        Method captures a single image with coordinates
        """
        cv2.imwrite(f'Captured/Sample_{sample_n}/Single/{loc_x}_{loc_y}.jpg', self.frame)



    def capture_video_close_version(self, video_length, sample_n, loc_x, loc_y, 
        resolution=(640, 480), framerate=25):
        """
        Method stops stream, records video with required length, 
        opens streaming camera, starts a streaming thread
        """
        self.stream_stop
        path = f'Captured/Sample_{sample_n}/Video/{loc_x}_{loc_y}.h264'

        with PiCamera() as camera:
            camera.resolution = resolution
            camera.start_recording(path)
            camera.wait_recording(video_length)
            camera.stop_recording()

        self.camera_open()
        self.stream_start()

        return path


    def capture_video_stream_version(self, video_length, sample_n, loc_x, loc_y):
        """
        Method grabs sequential images and appends to a list
        STILL UNDER CONSTRUCTION!!!
        """
        video_list = []
        timer = 0
        while timer < video_length:
            video_list.append(self.frame)
            timer += 1
        return video_list