from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes', views.recipes, name='recipes'),
    path('recipes/search', views.search, name='search'),
    path('recipes/random', views.random, name='random'),
    path('login', views.loginAuth, name='login'),
    path('logout', views.logoutAuth, name='logout'),
    path('register', views.registerAuth, name='register'),
    path('tos', views.tos, name='tos'),
    path('profile', views.profile, name='profile'),
]