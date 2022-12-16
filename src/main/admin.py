from django.contrib import admin
from .models import FavoriteRecipe

# Register your models here.

@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_name', 'user')
