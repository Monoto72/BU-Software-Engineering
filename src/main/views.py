from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def index(request):
    url = 'Home'
    return render(request, 'index.html', {'page_url': url})

def recipes(request):
    url = 'Recipes'
    return render(request, 'recipes.html', {'page_url': url})

def search(request):
    url = 'Search';
    
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
    url = 'Random'
    json = dummyRecipe()
    
    json['time'] = readable_time(json['time'])
    json['prep_time'] = readable_time(json['prep_time'])
    
    return render(request, 'random.html', {'page_url': url, 'recipe': json})


def readable_time(time):
    seconds = time * 60
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%dh %02dm %02ds" % (hour, minutes, seconds)


def login(request):
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
    return render(request, "login.html", { "login_form": form, "page_url": url})


def logout(request):
    """Log-out functionality
    Ensuring a users account doesn't get abused when `AFK`
    Args:
        request (object): Returns metadata
    Returns:
        route: Redirects to the homepage after logging out
    """
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
        # Could add a see you next time
    else:
        return redirect("/")


def register_req(request):
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
    return render (request, 'register.html', {"register_form": form, "page_url": url })



def dummyRecipe():
    return {
        "recipe": "Hunters Chicken",
        "time": 50,
        "prep_time": 15,
        "difficulty": "Easy",
        "serves": 4,
        "instructions": [
            "Heat oven to 200C/180C fan/gas 6. Oil a tray, put the chicken breasts on it and cover each one with 2 bacon rashers. Put the chicken in the oven for 20-25 mins until cooked through.",
            "While the chicken is cooking, fry the onion in 1 tbsp oil until golden brown and soft, then set aside. Put the potatoes in a large pan of boiling water and cook for 10-15 mins until soft. Put another smaller pan of water on the hob and bring to the boil while the potatoes are cooking. Once boiling, tip in the runner beans and carrots and cook for 8-10 mins until soft but with a little bite. Drain the potatoes and put them back in the pan with the milk and cream cheese, mash until smooth and stir though the fried onions.",
            "Once the chicken is cooked, pour over the BBQ sauce and scatter over the parmesan and return to the oven for 2 mins until the cheese has melted. Serve with the mash, carrots and runner beans."
        ],
        "ingredients": [
            "4 chicken breasts",
            "8 rashers of bacon",
            "1 onion, sliced",
            "1 red pepper, sliced",
            "1 tbsp tomato puree",
            "1 tbsp Worcestershire sauce",
            "1 tbsp Dijon mustard",
            "1 tbsp honey",
            "1 tbsp soy sauce",
            "1 tbsp olive oil",
            "1 tbsp balsamic vinegar",
            "1 tbsp cornflour",
            "1 tbsp water",
            "1 tbsp chopped parsley"
        ],
        "image_url": "https://www.kitchensanctuary.com/wp-content/uploads/2021/03/Hunters-chicken-Tall-FS-37.webp"
    }