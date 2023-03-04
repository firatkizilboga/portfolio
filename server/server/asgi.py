from django.core.handlers.asgi import ASGIHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from snakegame.consumers import EvolutionConsumer

application = ProtocolTypeRouter({
    "http": ASGIHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/evolve", EvolutionConsumer.as_asgi()),
        ])
    ),
})



# add the following lines to properly shut down the ASGIStaticFilesHandler
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
application = ASGIStaticFilesHandler(application)