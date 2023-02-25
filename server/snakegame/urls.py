
from django.urls import path
from .views import EvolutionView

urlpatterns = [
    path('evolve/', EvolutionView.as_view()),
]