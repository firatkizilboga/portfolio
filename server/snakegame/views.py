from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
#import evlolution from snake-game
from snakegame.evolution import Evolver
from snakegame.game import Game

class HelloView(APIView):
    def get(self, request):
        return Response(Evolver().test())

class EvolutionView(APIView):
    def get(self, request):
        #validate the request's data and return the response
        #get the data from the request
        data = request.data
        evolver = Evolver.from_json(data)
        snakes = evolver.evolve()
        snakes = list(snakes)
        #turn gens (a yield of snakes) into a list
        
        #make every snake play the game one more time
        
        frames = []
        for i,snake in enumerate(snakes):
            game = Game()
            game.snake = snake
            while (not game.game_over) and (game.frames<600):
                frames.append(game.step())
            
        return Response(frames)
    

    

