### File description
# The file contains autofocusing algorithm

### Packages import
import usb_cam
import motors

from sharpness_calculation import variance_sharpness
from math import sqrt

### Class of autofocus algorithm
class Autofocus:
    """
    Class of autofocus algorithm contains:
    -
    -
    -
    """

    def __init__(self, MotorObj, CameraObj, 
        focus_range, threshold=2):
        """
        Constructor initializes...
        """
        self.MotorObj = MotorObj
        self.CameraObj = CameraObj
        self.focus_range = focus_range
        self.threshold = threshold


    def fibonacci_num(number):
        """
        Function calculates approximate fibonacci number
        """
        return int(((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5)))


    def x1_calculation(self, a, b, f_range, i):
        """
        Method calculates x1 coordinate
        """
        return a + (self.fibonacci_num(f_range - i - 1) / 
            self.fibonacci_num(f_range - i + 1)) * (b - a)


    def x2_calculation(self, a, b, f_range, i):
        """
        Method calculates x2 coordinate
        """
        return b - (self.fibonacci_num(f_range - i - 1) /
            self.fibonacci_num(f_range - i + 1)) * (b - a)

   def move_capture_calculate(self, distance):
        """
        Function performs common operations
        ! Invert control of movements !
        """
        self.MotorObj.z_step(dist=-distance) #?????
        image = self.CameraObj.capture_autofocus_image()
        return variance_sharpness(image)

    def autofocus_local(self):
        """
        Function performs local autofocusing within a specific range
        """
        a_edge = 0
        coord_temp = a_edge
        b_edge = self.focus_range
        sharp_vals = []
        coords = []

        for i in range(0, self.focus_range):
            # Check for the 1st iteration
            if i == 0:
                # Calculate distance to move
                coord_x1 = x1_calculation(a_edge, b_edge, self.focus_range, i)
                coords.append(coord_x1)
                distance_x1 = coord_x1 - coord_temp

                # Move to distance, capture gray-scale image and calculate
                sharp_val_x1 = move_capture_calculate(distance_x1)
                sharp_vals.append(sharp_val_x1)
                coord_temp = coord_x1

                # Calculate distance to move
                coord_x2 = x2_calculation(a_edge, b_edge, self.focus_range, i)
                coords.append(coord_x2)
                distance_x2 = coord_x2 - coord_temp

                # Move to distance, capture gray-scale image and calculate
                sharp_val_x2 = move_capture_calculate(distance_x2)
                sharp_vals.append(sharp_val_x2)
                coord_temp = coord_x2

            # Compare sharpness values in x1 and x2
            if sharp_val_x1 < sharp_val_x2:
                # Reassign values if left value is less to decrease range
                a_edge = coord_x1
                b_edge = b_edge
                coord_x1 = coord_x2
                sharp_val_x1 = sharp_val_x2

                # Calculate distance to move
                coord_x2 = x2_calculation(a_edge, b_edge, self.focus_range, i)
                coords.append(coord_x2)
                distance_x2 = coord_x2 - coord_temp

                # Move to distance, capture gray-scale image and calculate
                sharp_val_x2 = move_capture_calculate(distance_x2)
                sharp_vals.append(sharp_val_x2)
                coord_temp = coord_x2

            else:
                # Reassign values if right value is less to decrease range
                a_edge = a_edge
                b_edge = coord_x2
                coord_x2 = coord_x1
                sharp_val_x2 = sharp_val_x1

                # Calculate distance to move
                coord_x1 = x1_calculation(a_edge, b_edge, self.focus_range, i)
                coords.append(coord_x1)
                distance_x1 = coord_x1 - coord_temp

                # Move to distance, capture gray-scale image and calculate
                sharp_val_x1 = move_capture_calculate(distance_x1)
                sharp_vals.append(sharp_val_x1)
                coord_temp = coord_x1

            # Check if the focus range is less than threshold value
            if b_edge - a_edge < self.threshold:
                # Find index with the sharpest image
                sharp_index = sharp_vals.index(max(sharp_vals))
                # Find the distance needed to move to achieve focus
                distance = (coords[sharp_index] - coords[len(coords) - 1])
                # ! Invert control of movement !
                self.MotorObj.z_step(-distance)
                temp = coord[sharp_index]
                break

    #?????
    #?????
    #?????
    def autofocus_global(self):
        """
        Function performs global autofocusing with going to endpoint
        """
        
        # Calibrate and move to start point

        #?????
        #?????
        #?????

        self.MotorObj.move_to_endpoint(self.speed_fast)
        self.MotorObj.move_to_start_position(self.speed_fast)
        # Start autofocusing
        self.autofocus_local()

    def refocus(self):
        """
        Function perfroms local focus correction
        """
        pass

if __name__ == "__main__":
    # Testing autofocus module
    print("Test 1: GRBL connection")
    device_name = motors.detect_device()
    drive = motors.CncDrive(device_name)

    input("Test 2: Open camera")
    micro_cam = usb_camera.MicroCamera(device_id=0)
    micro_cam.stream_start()

    input("Test 3: Init autofocus")
    # ??????
    autofoc = Autofocus(MotorObj=drive, CameraObj=micro_cam, focus_range=100)

    input("Test 4: Perform autofocus")
    autofoc.autofocus_local()

    input("Test 5: Close camera and drive")
    micro_cam.stream_stop()
    micro_cam.camera_close()