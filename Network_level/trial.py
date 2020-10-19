from aiohttp import web

async def index(request):
    return web.Response(text="Welcome home!")


my_web_app = web.Application()
my_web_app.router.add_get('/', index)
web.run_app(my_web_app)
