from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FavoriteRecipe(models.Model):
    recipe_name = models.CharField(max_length=250)
    recipe_image = models.CharField(max_length=250)
    recipe_time_to_cook = models.CharField(max_length=250)
    user = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)
    
