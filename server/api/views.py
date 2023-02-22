from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
#import evlolution from snake-game
from snake_game.evolution import Evolver

class HelloView(APIView):
    def get(self, request):
        return Response(Evolver().test())

