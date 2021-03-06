### File description
# File contains class and methods to send gcode
# via pyserial interface

### Packages import
import time
import serial

### Help functions
# NEEDS REFACTORING!!!
def detect_device():
    """
    Function gets device name to establish
    serial connection btwn PC and CNC
    """
    with open('../device_config.txt') as json_file:
        motor_name = json.load(json_file)["motor_name"]
    return motor_name

# NEEDS REFACTORING!!!
def create_gfile():
    """
    Function creates g-code script for scanning
    """
    pass

### Class section
class CncDrive():
    """
    Class contains:
    - ...;
    - ...;
    - ...;
    """
    def __init__(self, device_name):
        """
        Class constructor starts connection via pyserial and
        sends starting gcode
        """
        # open connection
        self.cnc = serial.Serial(port = f"{device_name}", baudrate ="115200")
        # setup
        #self.cnc.write(b"\r\n\r\n")
        time.sleep(2)
        self.cnc.reset_output_buffer()
        # all required G-code commands
        self.cnc.write(b"G91\n")

    def get_home(self):
        """
        Function returns stage to the home position
        """
        self.cnc.write(b"$H\n")
        if self.cnc.readline().strip() == b"ok":
            print("Success")

    def kill_lock(self):
        """
        Function returns stage to the home position
        """
        self.cnc.write(b"$X\n")
        if self.cnc.readline().strip() == b"ok":
            print("Success")

    # NEEDS REFACTORING!!!
    def set_position(self):
        """
        Function sets base position
        """
        self.cnc.write(b"G28.1\n")
        if self.cnc.readline().strip() == b"ok":
            print("Success")

    # NEEDS REFACTORING!!!
    def get_to_position(self):
        """
        Function sets base position
        """
        self.cnc.write(b"G28\n")
        if self.cnc.readline().strip() == b"ok":
            print("Success")

    # NEEDS REFACTORING!!!
    def get_location(self):
        """
        Function gets coordinates of current position
        """
        self.cnc.write(b"?\n")
        coord = self.cnc.readline()
        return(str.decode(coord))

    def x_step(self, dist=5, speed=100):
        """
        Function performs movement along X-axis
        """
        command = str.encode(f"G01 X{dist} F{speed}\n")
        self.cnc.write(command)
        coord = self.cnc.readline()
        print(coord)
        self.kill_lock()
        coord = self.cnc.readline()
        print(coord)
        self.cnc.write(b"G91\n")

    def y_step(self, dist=5, speed=100):
        """
        Function performs movement along Y-axis
        """
        command = str.encode(f"G01 Y{dist} F{speed}\n")
        self.cnc.write(command)
        coord = self.cnc.readline()
        print(coord)
        self.kill_lock()
        coord = self.cnc.readline()
        print(coord)
        self.cnc.write(b"G91\n")

    def z_step(self, dist=5, speed=100):
        """
        Function performs movement along Z-axis
        """
        command = str.encode(f"G01 Z{dist} F{speed}\n")
        self.cnc.write(command)
        coord = self.cnc.readline()
        coord = self.cnc.readline()
        print(coord)
        self.cnc.write(b"G91\n")

    # NEEDS REFACTORING!!!
    def perform_gfile(self, gfile):
        """
        Function performs prerecorded g-code script
        """
        pass

    def read_gcode(self):
        cnc_info = self.cnc.readline()
        print(cnc_info)


# NEEDS REFACTORING!!!
class CncSetup():
    """
    Class contains:
    - ...;
    - ...;
    - ...;
    """
    def __init__(self, ):
        """
        Class constructor ...
        """
        pass



if __name__ == "__main__":
    # Testing motors.py module
    print("Test 1: GRBL connection")
    device_name = detect_device()
    drive = CncDrive(device_name)

    input("Press to read...")
    drive.read_gcode()

    input("Press to continue...")
    print("Test 2: Killing lock")
    drive.kill_lock()

    input("Press to continue...")
    print("Test 4.3: Perform Z movement")
    dist = int(input("Enter distance "))
    speed = int(input("Enter speed "))
    drive.z_step(dist, speed)

    input("Press to continue...")
    print("Test 4.3: Perform Z movement")
    dist = int(input("Enter distance "))
    speed = int(input("Enter speed "))
    drive.z_step(dist, speed)

    input("Press to continue...")
    print("Test 4.1: Perform X movement")
    dist = int(input("Enter distance"))
    speed = int(input("Enter speed"))
    drive.x_step(dist, speed)

    input("Press to continue...")
    print("Test 4.2: Perform Y movement")
    dist = int(input("Enter distance"))
    speed = int(input("Enter speed"))
    drive.y_step(dist, speed)

    # input("Press to continue...")
    # print("Test 2: Get to the home position")
    # drive.get_home()

    # input("Press to continue...")
    # print("Test 3: Set position to return")
    # drive.set_position()

    # input("Press to continue...")
    # print("Test 4.3: Perform Z movement")
    # dist = int(input("Enter distance "))
    # speed = int(input("Enter speed "))
    # drive.z_step(dist, speed)

    # input("Press to continue...")
    # print("Test 4.1: Perform X movement")
    # dist = int(input("Enter distance"))
    # speed = int(input("Enter speed"))
    # drive.x_step(dist, speed)

    # input("Press to continue...")
    # print("Test 4.2: Perform Y movement")
    # dist = int(input("Enter distance"))
    # speed = int(input("Enter speed"))
    # drive.y_step(dist, speed)
   
    # input("Press to continue...")
    # print("Test 5: Get current location")
    # location = drive.get_location()
    # print(location)

    # input("Press to continue...")
    # print("Test 6: Get to the position")
    # drive.get_to_position()