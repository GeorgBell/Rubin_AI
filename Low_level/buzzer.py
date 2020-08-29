### File description
# File contains base classes of GPIO devices including:
# - Buzzer

### Packages import
import Jetson.GPIO as GPIO
from time import sleep

### Base class of a buzzer
class Buzzer:
    """ 
    Base class of a buzzer contains:
    - __init__:
    - setup_gpio;
    - __signal_high_low;
    - welcome_signal;
    - set_sample_signal;
    - scanning_signal;
    - finish_signal
    """

    def __init__(self, BUZ, name, log=False):
        """ 
        Constructor initializes variables for GPIO pins:
        - BUZ - send impulses to buzzer
        """
        self.BUZ = BUZ
        self.name = name
        self.delay_1 = 1
        self.delay_2 = 0.5

        if log == True:
            print("Buzzer " + self.name + " created")

    def setup_gpio(self):
        """
        Method configures input and output pins
        """
        GPIO.setmode(GPIO.BCM) # Set pins assignment mode
        GPIO.setup(self.BUZ, GPIO.OUT) # Set pins for buzzer

    def __signal_high_low(self, delay):
        """
        Private method performs beeping
        """
        GPIO.output(self.BUZ, GPIO.HIGH)
        sleep(delay)
        GPIO.output(self.BUZ, GPIO.LOW)
        sleep(delay)


    def welcome_signal(self):
        """
        Method produces welcome audio signal
        """
        self.__signal_high_low(self.delay_1)


    def set_sample_signal(self):
        """
        Method produces set sample audio signal
        """
        for i in range(2):
            self.__signal_high_low(self.delay_1)


    def scanning_signal(self):
        """
        Method produces scanning audio signal
        """
        for i in range(3):
            self.__signal_high_low(self.delay_1)


    def finish_signal(self):
        """
        Method produces finish audio signal
        """
        for i in range(2):
            self.__signal_high_low(self.delay_2)

if __name__ == "__main__":
    # Testing buzzer.py module
    input("Test 1: Setting up buzzer")
    buz_test = Buzzer(BUZ=18, name="test_buzzer")
    buz_test.setup_gpio()

    input("Test 2: Welcome signal")
    buz_test.welcome_signal()

    input("Test 3: Set sample signal")
    buz_test.set_sample_signal()

    input("Test 4: Welcome signal")
    buz_test.scanning_signal()

    input("Test 3: Set sample signal")
    buz_test.finish_signal()