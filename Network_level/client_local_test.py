### File description
# The file contains client logic for real-time control and
# communication via webrtc protocol

### Packages import
import asyncio
import json
import sys
sys.path.append('../')
from rtcbot import Websocket, RTCConnection, CVCamera
from Applied_level.autofocus import Autofocus
from Applied_level.scanning import Scanning
from Applied_level.snapshot import Snapshot
import Low_level.cameras as cameras
import Low_level.motors as motors



### Base init
cam = None
conn = None
sample_n = None

#motor_name = motors.detect_device()
#drive = CncDrive(device_name)
#autofoc = Autofocus(MotorObj=drive, CameraObj=cam, focus_range=10)

def set_up_components():
    global cam, conn
    cam = cameras.MicroCamera(type="remote_usb") # !!! CHANGE FOR CUSTOM CAMERA OBJ
    conn = RTCConnection()
    conn.video.putSubscription(cam)
    conn.subscribe(onMessage)

def close_components():
    global cam, conn
    cam.close()
    conn.close()

async def connect():
    """
    Connect establishes a websocket connection to the server,
    and uses it to send and receive info to establish webRTC connection.
    """
    # Read configuration to get device name
    with open('../device_config.txt') as json_file:
        device_name = json.load(json_file)["device_name"]
    # Establish web socket connection and send device name
    ws = Websocket("http://localhost:8080/ws") # !!! CHANGE FOR REAL IP
    ws.put_nowait(device_name)

    # Establish WebRTC connection
    remoteDescription = await ws.get()
    robotDescription = await conn.getLocalDescription(remoteDescription)
    ws.put_nowait(robotDescription)
    
    print("Started WebRTC")
    await ws.close()

def onMessage(msg):
    """
    Main control logic
    performed via WebRTC
    """
    global sample_n
    print("Got message:", msg["command"])
    # Movement section
    if msg["command"] == "forward":
        #drive.y_step(dist=5)
        print("Moved forward by 5")
    elif msg["command"] == "backward":
        #drive.y_step(dist=-5)
        print("Moved backward by 5")
    elif msg["command"] == "right":
        #drive.x_step(dist=5)
        print("Moved right by 5")
    elif msg["command"] == "left":
        #drive.x_step(dist=-5)
        print("Moved left by 5")
    elif msg["command"] == "up":
        #drive.z_step(dist=5)
        print("Moved up by 5")
    elif msg["command"] == "down":
        #drive.z_step(dist=-5)
        print("Moved down by 5")
    
    # Function section
    elif msg["command"] == "snapshot":
        #coord = drive.get_coord()
        # Mockup
        coord = (1,1,1)
        cameras.create_data_directory(sample_n)
        # !!! GET SAMPLE NUMBER !!!
        cam.capture_single_image(sample_n, coord[0], coord[1])
        print("Captured image")

    elif msg["command"] == "autofocus":
        #autofoc.autofocus_local()
        print("Performed autofocus")

    elif msg["command"] == "scan":
        #autofoc.autofocus_local()
        print("Performed scanning")

    elif msg["command"] == "set_sample":
        #autofoc.autofocus_local()
        print("Performed setting sample")

    elif msg["command"] == "sample_number":
        sample_n = msg["value"]
        print("sample_n")

    elif msg["command"] == "exit":
        close_components()
        set_up_components()
        asyncio.ensure_future(connect())


set_up_components()
asyncio.ensure_future(connect())
try:
    asyncio.get_event_loop().run_forever()
finally:
    cam.close()
    conn.close()