
from django.urls import path
from .views import HelloView
from .views import EvolutionView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('evolve/', EvolutionView.as_view()),
]