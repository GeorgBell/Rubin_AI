from aiohttp import web
routes = web.RouteTableDef()

from rtcbot import Websocket, getRTCBotJS

ws = [] # Websocket connection to the robot
@routes.get("/ws")
async def websocket(request):
    global ws
    ws.append(Websocket(request))
    print("Robot Connected")
    val = await ws[-1].get()
    print(val)
    await ws[-1]  # Wait until the websocket closes
    print("Robot disconnected")
    return ws[-1].ws

# Called by the browser to set up a connection
@routes.post("/connect")
async def connect(request):
    global ws
    if ws[-1] is None:
        raise web.HTTPInternalServerError("There is no robot connected")
    clientOffer = await request.json()
    # Send the offer to the robot, and receive its response
    ws[-1].put_nowait(clientOffer)
    robotResponse = await ws[-1].get()
    return web.json_response(robotResponse)

# Serve the RTCBot javascript library at /rtcbot.js
@routes.get("/rtcbot.js")
async def rtcbotjs(request):
    return web.Response(content_type="application/javascript", text=getRTCBotJS())

@routes.get("/")
async def index(request):
    with open("index.html", "r") as f:
        return web.Response(content_type="text/html", text=f.read())


async def cleanup(app):
    global ws
    if ws[-1] is not None:
        c = ws[-1].close()
        if c is not None:
            await c

app = web.Application()
app.add_routes(routes)
app.on_shutdown.append(cleanup)
web.run_app(app)