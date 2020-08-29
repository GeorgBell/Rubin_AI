import RPi.GPIO as GPIO
from time import sleep

############################################################################
#           Main Z-move
############################################################################
def bipolar(k):
    ENBL = 26         
    DIR = 13   # Direction GPIO Pin
    STEP = 19  # Step GPIO Pin
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    SPR = 200   # Steps per Revolution (360 / angle)
    M0 = 21
    M1 = 20
    M2 = 16

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(ENBL, GPIO.OUT)
    GPIO.output(ENBL, GPIO.LOW) ################################ LOW

    MODE = (M0, M1, M2)   # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}
    GPIO.output(MODE, RESOLUTION['1/32'])

    step_count = int(SPR*32*abs(k))

    delay = .0208/256
    
    # Go down
    if (k >= 0):
        GPIO.output(DIR, CW)
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        GPIO.cleanup()
    # Go up
    else:
        GPIO.output(DIR, CCW)
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)  
        GPIO.cleanup()
    
############################################################################
#           GO DOWN TO VERY BOTTOM
############################################################################

def bipolar_go_0():
    
    # Detect the bottom
    def my_callback_0(channel):
        GPIO.cleanup()
        

    ENBL = 26   
    DIR = 13   # Direction GPIO Pin
    STEP = 19  # Step GPIO Pin
    #CCW = 0    
    CW = 1
    SPR = 200   # Steps per Revolution (360 / angle)
    M0 = 21
    M1 = 20
    M2 = 16
    Zmin = 8

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(ENBL, GPIO.OUT)
    GPIO.output(ENBL, GPIO.LOW)
    
    GPIO.setup(Zmin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(Zmin, GPIO.FALLING, callback=my_callback_0) #bouncetime=100
    
    MODE = (M0, M1, M2)   # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'1/8': (1, 1, 0)}
    GPIO.output(MODE, RESOLUTION['1/8'])
    
    GPIO.output(DIR, CW)
    step_count = SPR*8*55
    delay = .0208/256


    try:
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        GPIO.cleanup()
    except RuntimeError:
        print("Bottom")
        return


    print("first round")

    

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(ENBL, GPIO.OUT)
    GPIO.output(ENBL, GPIO.LOW)
    
    GPIO.setup(Zmin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(Zmin, GPIO.FALLING, callback=my_callback_0) #bouncetime=100
    
    GPIO.setup(MODE, GPIO.OUT)
    GPIO.output(MODE, RESOLUTION['1/8'])
    
    GPIO.output(DIR, CW)
    step_count = SPR*8*55

    try:
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        GPIO.cleanup()
    except RuntimeError:
        print("Bottom")
        return
    
############################################################################
#           GO TO START POSITION
############################################################################

def bipolar_start(k):
    ENBL = 26      
    DIR = 13   # Direction GPIO Pin
    STEP = 19  # Step GPIO Pin
    CCW = 0    
    #CW = 1
    SPR = 200   # Steps per Revolution (360 / angle)
    M0 = 21
    M1 = 20
    M2 = 16

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(ENBL, GPIO.OUT)
    GPIO.output(ENBL, GPIO.LOW)
    
    MODE = (M0, M1, M2)   # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'1/8': (1, 1, 0)}
    GPIO.output(MODE, RESOLUTION['1/8'])
    
    GPIO.output(DIR, CCW)
    step_count = int(SPR*8*(k/2))
    delay = .0208/256
    

    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    GPIO.cleanup()

    print("first round")

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(MODE, GPIO.OUT)
    GPIO.setup(ENBL, GPIO.OUT)
    GPIO.output(ENBL, GPIO.LOW)
    GPIO.output(MODE, RESOLUTION['1/8'])
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    GPIO.cleanup()




