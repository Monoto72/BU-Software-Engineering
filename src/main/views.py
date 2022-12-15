from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from . import api_functions as api

# Create your views here.

def index(request):
    url = 'home'
    return render(request, 'index.html', {'page_url': url})

def recipes(request):
    url = 'recipes'

    if request.method == 'POST':
        # Get the recipe name, starting positsion and offset from the URL
        recipe = request.POST['recipe']
        page = request.POST['page']
        per_page = request.POST['per_page']
    
        recipes = api.getRecipeByName(recipe_filter=recipe, page=page, per_page=per_page) # Get the recipes from the API
    if request.method == 'GET':
        recipes = api.getRecipeByName(page=0, per_page=5) # Get the recipes from the API
        
    # Need to display it on the page
        
    return render(request, 'recipes.html', {'page_url': url})

def search(request):
    url = 'search';
    
    if request.method == 'POST':
        count = 1;
        ingredients = []
        
        for key in request.POST:
            field = 'ingredient-' + str(count)
            if key == field:
                ingredients.append(request.POST[key])
                count += 1

        # TODO: Place the result on the Page
        recipes = api.getRecipes(ingredients)
        recipes = recipes['recipes'] # Extract the list of recipes from the data
    
    return render(request, 'search.html', {'page_url': url})

def random(request):
    url = 'random'
    
    # TODO: Place the result on the Page
    randomRecipe = api.getRandomRecipe()
    
    return render(request, 'random.html', {'page_url': url})