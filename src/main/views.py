from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from . import api_functions as api
from main.models import FavoriteRecipe

# Create your views here.

def index(request):
    url = 'Home'
    return render(request, 'index.html', {'page_url': url})

def recipes(request):
    url = 'Recipes'
    page = 0
    page_check_next = True
    page_check_prev = False
    
    if request.method == 'POST':
        if request.POST.get('recipe-name'): 
            recipe = api.getRecipeByName(request.POST.get('recipe-name')[:1])
            return render(request, 'random.html', {'page_url': url, 'recipe': recipe[0]})# Get the recipe name, starting positsion and offset from the URL
        if request.POST.get('page'):
            page = int(request.POST.get('page-num'))
            if request.POST.get('page') == 'next':
                page += 5
                page_check_prev = True
            if request.POST.get('page') == 'prev':
                if (page < 0):
                    page = 0
                if (page > 0):
                    page -= 5
                    page_check_prev = True
                if (page == 0):
                    page_check_prev = False
        per_page = 5
        
        recipes = api.getRecipeByName(page=page, per_page=per_page) # Get the recipes from the API
        if  len(recipes) < 5:
            page_check_next = False
            
    if request.method == 'GET':
        recipes = api.getRecipeByName(page=0, per_page=5) # Get the recipes from the API
        
    # Need to display it on the page
        
    return render(request, 'recipes.html', {'page_url': url, 'recipes': recipes, 'page': page, 'page_check_next': page_check_next, 'page_check_prev': page_check_prev})

def search(request):
    
    url = 'Search';

    if request.method == 'POST':
        if request.POST.get('recipe-name'):
            recipe = api.getRecipeByName(request.POST.get('recipe-name')[:1])
            return render(request, 'random.html', {'page_url': url, 'recipe': recipe[0]})
        else:
            count = 1;
            ingredients = []
        
            for key in request.POST:
                field = 'ingredient-' + str(count)
                if key == field:
                    ingredients.append(request.POST[key])
                    count += 1
        
            recipes = api.getRecipes(ingredients)
            recipes = recipes['recipes']

            return render(request, 'list-recipes.html', {'page_url': url, 'recipes': recipes})
    return render(request, 'search.html', {'page_url': url})


def random(request):
    url = 'Random'
    json = api.getRandomRecipe()
    favourited = True
    
    json['time'] = json['time_to_cook']
    json['time_to_cook'] = readableTime(json['time_to_cook'])
    json['time_to_prep'] = readableTime(json['time_to_prep'])
    
    if request.user.is_authenticated:
        recipe = FavoriteRecipe.objects.filter(recipe_name=json['recipe'], user=request.user)
        if recipe:
            favourited = False
    
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('recipe-add'):
            favourite_recipe(request.POST.get('recipe-add'), request.POST.get('recipe-image'), request.POST.get('recipe-time'), request.user)
            return redirect("/")
        if request.POST.get('recipe-remove'):
            unfavourite_recipe(request.POST.get('recipe-remove'), request.POST.get('recipe-image'), request.POST.get('recipe-time'), request.user)
            return redirect("/")
    
    return render(request, 'random.html', {'page_url': url, 'recipe': json, 'favourited': favourited})


def readableTime(time):
    seconds = time * 60
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%dh %02dm %02ds" % (hour, minutes, seconds)


def loginAuth(request):
    if request.user.is_authenticated:
        return redirect("/")

    url = "Login"
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You successfully logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"page_url": url})


def logoutAuth(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    else:
        return redirect("/")


def registerAuth(request):
    if request.user.is_authenticated:
        return redirect("/")

    url = "Register"
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CreateUserForm()
    return render (request, 'register.html', {"page_url": url })


def profile(request):
    url = "Profile"
    favourites = []
    
    if request.user.is_authenticated:
        if request.GET.get('panel'):
            if request.GET.get('panel') == 'favourites':
                recipes = FavoriteRecipe.objects.filter(user=request.user)
                for recipe in recipes:
                    json = {'name': recipe.recipe_name, 'image': recipe.recipe_image, 'time_to_cook': recipe.recipe_time_to_cook}
                    favourites.append(json)
                    
        if request.method == 'POST':
            if request.POST.get('recipe-name'):
                recipe = api.getRecipeByName(request.POST.get('recipe-name')[:1])
                return render(request, 'random.html', {'page_url': url, 'recipe': recipe})
                    
        return render(request, 'profile.html', {'page_url': url, 'recipes': favourites})
    return render(request, 'index.html', {'page_url': url})
    
    
def tos(request):
    url = "TOS"
    return render(request, 'tos.html', {'page_url': url})


def favourite_recipe(recipe_name, recipe_image, recipe_time_to_cook, user):
    FavoriteRecipe.objects.create(recipe_name=recipe_name, recipe_image=recipe_image, recipe_time_to_cook=recipe_time_to_cook, user=user)
    
def unfavourite_recipe(recipe_name, recipe_image, recipe_time_to_cook, user):
    FavoriteRecipe.objects.filter(recipe_name=recipe_name, user=user).delete()
    