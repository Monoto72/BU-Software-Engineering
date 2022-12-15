from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Create your views here.

def index(request):
    url = 'home'
    return render(request, 'index.html', {'page_url': url})

def recipes(request):
    url = 'recipes'
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
                
        # getRecipe(ingredients)
    
    return render(request, 'search.html', {'page_url': url})

def random(request):
    url = 'random'
    return render(request, 'random.html', {'page_url': url})