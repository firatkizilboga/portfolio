from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import time
# Create your views here.
#import evlolution from snake-game
from snakegame.evolution import Evolver
from snakegame.game import Game

class HelloView(APIView):
    def get(self, request):
        return Response(Evolver().test())

class EvolutionView(APIView):
    def post(self, request):
        #validate the request's data and return the response
        #get the data from the request
        data = request.data
        evolver = Evolver.from_json(data)
        snakes = evolver.evolve()
        snakes = list(snakes)
        #turn gens (a yield of snakes) into a list
        
        #make every snake play the game one more time
        
        frames = []
        sorted_snakes = sorted(snakes, key = lambda snake: snake.fitness)
        snakes = [sorted_snakes[int(len(sorted_snakes)/5*i)] for i in range(5)]
        for i,snake in enumerate(snakes[::-1]):
            print(snake.fitness)
            game = Game()
            game.snake.brain = snake.brain
            while (not game.game_over) and (game.frames<200):
                frames.append(game.step(playback=True))
        return Response(frames)
    