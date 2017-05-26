from channels.staticfiles import StaticFilesConsumer
from channels.routing import route
from django.conf import settings

from . import consumers

channel_routing = [
    # This makes Django serve static files from settings.STATIC_URL, similar
    # to django.views.static.serve. This isn't ideal (not exactly production
    # quality) but it works for a minimal example.
    #route('http.request', StaticFilesConsumer()),

    # Wire up websocket channels to our consumers:
    route('websocket.connect', consumers.ws_connect),
    route('websocket.receive', consumers.ws_receive),
    route('websocket.disconnect', consumers.ws_disconnect),
]

if settings.DEBUG:
    channel_routing += [ route('http.request', StaticFilesConsumer()) ]