import asyncio
#import sync to async

from asgiref.sync import sync_to_async


from channels.generic.websocket import JsonWebsocketConsumer
from snakegame.evolution import Evolver
from channels.layers import get_channel_layer

import json
class EvolutionConsumer(JsonWebsocketConsumer):
    def connect(self):
        #accept
        self.accept()

    def receive_json(self, data):
        print(data)
        self.evolver = Evolver.from_json(data)
        self.evolver.create_population()
        self.send_frames()

    def send_frames(self):
        while self.evolver.generation < self.evolver.max_generations:
            frames = self.evolver.step()
            self.send_json(frames)
    
    def disconnect(self, close_code):
        self.close()