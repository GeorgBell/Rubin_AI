### File description
# The file contains main logic of RTC server

### Packages import
from aiohttp import web
routes = web.RouteTableDef()
from rtcbot import Websocket, getRTCBotJS

import jinja2
import aiohttp_jinja2

# Void dictionary of web socket connections
ws = {}

def setup_static_routes(app):
    app.router.add_static('/static/',
        path="/home/georgbell/Rubin_AI/Network_level/templates/static/",
        name="static")


@routes.get("/rtcbot.js")
async def rtcbotjs(request):
    return web.Response(content_type="application/javascript", text=getRTCBotJS())


@routes.get("/ws")
async def websocket(request):
    """
    Remote microscope connection
    """
    global ws
    temp_ws = Websocket(request)
    name_ws = await temp_ws.get()
    print("Robot Connected")
    ws[name_ws] = temp_ws
    await ws[name_ws]  # Wait until the websocket closes
    del ws[name_ws]
    print("Robot disconnected")
    return temp_ws.ws


@routes.get("/", name="index_g")
async def index_g(request):
    context = {"devices":ws}
    response = aiohttp_jinja2.render_template("index.html", request, context)
    return response


@routes.post("/", name="index_p")
async def index_p(request):
    form = await request.post()
    context = {"device":form["selected_device"]}
    response = aiohttp_jinja2.render_template("control.html", request, context)
    return response


@routes.post("/connect")
async def connect(request):
    global ws
    clientOffer = await request.json()
    # Send the offer to the robot, and receive its response
    ws[clientOffer["device"]].put_nowait(clientOffer["jsOffer"])
    robotResponse = await ws[clientOffer["device"]].get()
    return web.json_response(robotResponse)


async def cleanup(app):
    global ws
    if ws is not None:
        for item in ws.items():
            item[1].close()

app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader("/home/georgbell/Rubin_AI/Network_level/templates"))
app.add_routes(routes)
setup_static_routes(app)
app.on_shutdown.append(cleanup)
web.run_app(app)