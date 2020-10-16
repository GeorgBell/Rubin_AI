from aiohttp import web
routes = web.RouteTableDef()

from rtcbot import RTCConnection, getRTCBotJS, CVCamera

# Initialize the camera
camera = CVCamera()

# For this example, we use just one global connection
conn = RTCConnection()

# Send images from the camera through the connection
conn.video.putSubscription(camera)

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
    conn.put_nowait({"data": resp})

# Serve the RTCBot javascript library at /rtcbot.js
@routes.get("/rtcbot.js")
async def rtcbotjs(request):
    return web.Response(content_type="application/javascript", text=getRTCBotJS())


# This sets up the connection
@routes.post("/connect")
async def connect(request):
    clientOffer = await request.json()
    serverResponse = await conn.getLocalDescription(clientOffer)
    return web.json_response(serverResponse)

@routes.get("/")
async def index(request):
    return web.Response(
        content_type="text/html",
        text=r"""
    <html>
        <head>
            <title>RTCBot: Skeleton</title>
            <script src="/rtcbot.js"></script>
        </head>
        <body style="text-align: center;padding-top: 30px;">
            <video autoplay playsinline controls></video> <audio autoplay></audio>
            <p>
            Open the browser's developer tools to see console messages (CTRL+SHIFT+C)
            </p>
            <h1>Click the Button</h1>
            <button type="button" id="mybutton1">Button 1!</button>
            <button type="button" id="mybutton2">Button 2!</button>
            <button type="button" id="mybutton3">Button 3!</button>
            <script>
                var conn = new rtcbot.RTCConnection();
                // When the video stream comes in, display it in the video element
                conn.video.subscribe(function(stream) {
                    document.querySelector("video").srcObject = stream;
                });

                async function connect() {
                    let offer = await conn.getLocalDescription();
                     // POST the information to /connect
                    let response = await fetch("/connect", {
                        method: "POST",
                        cache: "no-cache",
                        body: JSON.stringify(offer)
                    });

                    await conn.setRemoteDescription(await response.json());
                    console.log("Ready!");
                }
                connect();

                var mybutton1 = document.querySelector("#mybutton1");
                mybutton1.onclick = function() {
                    conn.put_nowait({ data: "Button1" });
                };

                var mybutton2 = document.querySelector("#mybutton2");
                mybutton2.onclick = function() {
                    conn.put_nowait({ data: "Button2" });
                };

                var mybutton3 = document.querySelector("#mybutton3");
                mybutton3.onclick = function() {
                    conn.put_nowait({ data: "Button3" });
                };

            </script>
        </body>
    </html>
    """)

async def cleanup(app):
    await conn.close()
    camera.close() # Singletons like a camera are not awaited on close

app = web.Application()
app.add_routes(routes)
app.on_shutdown.append(cleanup)
web.run_app(app)