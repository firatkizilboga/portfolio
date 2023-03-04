from django.urls import re_path
from snakegame.consumers import EvolutionConsumer

websocket_urlpatterns = [
    re_path(r"ws/evolve", EvolutionConsumer.as_asgi()),
]