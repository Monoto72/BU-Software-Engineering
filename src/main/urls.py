from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes', views.recipes, name='recipes'),
    path('recipes/search', views.search, name='search'),
    path('recipes/random', views.random, name='random'),
]