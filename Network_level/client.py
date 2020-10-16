import asyncio
from rtcbot import Websocket, RTCConnection, CVCamera

cam = CVCamera()
conn = RTCConnection()
conn.video.putSubscription(cam)

# Connect establishes a websocket connection to the server,
# and uses it to send and receive info to establish webRTC connection.
async def connect():
    ws = Websocket("http://localhost:8080/ws")
    ws.put_nowait("Lol")
    remoteDescription = await ws.get()
    robotDescription = await conn.getLocalDescription(remoteDescription)
    ws.put_nowait(robotDescription)
    
    print(robotDescription)
    print("Started WebRTC")
    await ws.close()

@conn.subscribe
def onMessage(msg):  # Called when messages received from browser
    print("Got message:", msg["data"])
    if msg["data"] == "Button1":
        resp = "Lol"
        print(resp)
    elif msg["data"] == "Button2":
        resp = "Kek"
        print(resp)
    elif msg["data"] == "Button3":
        resp = "Cheburek"
        print(resp)


asyncio.ensure_future(connect())
try:
    asyncio.get_event_loop().run_forever()
finally:
    cam.close()
    conn.close()