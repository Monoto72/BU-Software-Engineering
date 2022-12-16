# API Functions
import json
import os
import random

# Get path to the recipes.json file
path = os.path.join(os.path.dirname(__file__), 'recipes.json')

# Get recipes from an array of ingredients
def getRecipes(ingredients):
    # Open the recipe.json file
    with open(path, 'r') as f:
        # Loads the json file
        recipes = json.load(f)
        
        # Extract the list of recipes from the data
        recipes = recipes['recipes']
        
        # Set up an empty list to store matching recipes
        matching_recipes = []
        
        # Loop through each recipe
        for recipe in recipes:
            # Extract the list of ingredients from the recipe
            recipe_ingredients = recipe['ingredients']

            # Set Counter
            counter = 0
            
            # loop though each ingredient in the array
            for ingredient in ingredients:
                # Loops through each ingredient in the recipe
                for recipe_ingredient in recipe_ingredients:
                    if ingredient in recipe_ingredient:
                        # Increment the counter
                        counter += 1
                
                # check if the recipe is already in the list and if 2 or more ingredients match
                if recipe not in matching_recipes and counter >= 2:
                    # Add the recipe to the list
                    matching_recipes.append(recipe)
                    break

    # Return the list of matching recipes as a JSON response
    return {'recipes': matching_recipes}

# Get recipes by name
def getRecipeByName(recipe_filter = 'all', page=0, per_page=5):
    # open the recipe.json file
    with open(path, 'r') as f:
        # Loads the json file
        recipes = json.load(f)
        
        # Extract the list of recipes from the data
        recipes = recipes['recipes']
        
        # Set up an empty list to store matching recipes
        matching_recipes = []
        
        # Checks the recipe filter 
        if recipe_filter == 'all':
            
            for i in range(page, page + per_page):
                if i >= len(recipes):
                    break
                matching_recipes.append(recipes[i])
        
        else:
            for i in range(page, page + per_page):
                if i >= len(recipes):
                    break
                if recipe_filter in recipes[i]['recipe']:
                    matching_recipes.append(recipes[i])
                
        return matching_recipes

# Random Recipe
def getRandomRecipe():
    # Open the recipe.json file
    with open(path, 'r') as f:
        # Loads the json file
        recipes = json.load(f)
        
        # Pick a random number
        rand = random.randint(0, len(recipes['recipes']) - 1)
        
        randomRecipe = recipes['recipes'][rand]
        
        return randomRecipe