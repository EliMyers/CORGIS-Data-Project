from flask import Flask, url_for, render_template, request
from markupsafe import Markup
import json
app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')
    
    
@app.route('/showNutrients')
def render_Nutrients():
    categories = get_category_options()
    fatInfo = ""
    mineralInfo = ""
    vitaminInfo = "" 
    descriptions = ""
    if "category" in request.args:
        category = request.args.get('category')
        descriptions = get_description_options(category)
    elif "description" in request.args:
        description = request.args.get('description')
        minerals = get_minerals(description)
        mineralInfo = "In " + description + ", the major minerals are: " + str(minerals) + "."
        fats = get_fat(description)
        fatInfo = "In " + description + ", the fats are: " + str(fats) + "."
        vitamins = get_vitamins(description)
        vitaminInfo = "In " + description + ", the vitamins are: " + str(vitamins) + "."
    
    return render_template('page1.html', category_options=categories, description_options=descriptions, mineral_fact=mineralInfo, fat_fact=fatInfo, vitamin_fact=vitaminInfo)


@app.route("/highestAmounts")
def render_page2():
    fact = ""
    category = ""
    typeOfHighest = ""
    mostFact = ""
    categories = get_category_options()
    if "mostType" in request.args and "category" in request.args:
        category = request.args.get('category')
        typeOfHighest = request.args.get('mostType')
        mostFact =  highest(category, typeOfHighest)
        if mostFact == "":
            mostFact = "none, there is no " + typeOfHighest + " in the " + category + " category"
        fact = "In the " + category + " category, the option with the highest " + typeOfHighest + " is " + mostFact + "."

    return render_template('page2.html', category_options=categories, highest_fact=fact)
    
@app.route('/charts')
def render_charts():
    categories = get_category_options()
    descriptions = ""
    carb = 0
    protein = 0
    calcium = 0
    potassium = 0
    sodium = 0
    vitaminC = 0
    if "category" in request.args:
        category = request.args.get('category')
        descriptions = get_description_options(category)
    elif "description" in request.args:
        description = request.args.get('description')
        carb = get_data(description, "Carbohydrate")
        protein = get_data(description, "Protein")
        calcium = get_one_mineral(description, "Calcium") 
        potassium = get_one_mineral(description, "Potassium")
        sodium = get_one_mineral(description, "Sodium")
        vitaminC = get_one_vitamin(description, "Vitamin C")
    return render_template('page3.html', category_options=categories, description_options=descriptions, carbNum=carb, proteinNum=protein, calciumNum=calcium, potassiumNum=potassium, sodiumNum=sodium, vitaminCNum=vitaminC)
    
def get_category_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('food.json') as food_data:
        allFoods = json.load(food_data)
    foods=[]
    for c in allFoods:
        if c["Category"] not in foods:
            foods.append(c["Category"])
    options=""
    for s in foods:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_description_options(category):
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('food.json') as food_data:
        allFoods = json.load(food_data)
    foods=[]
    for c in allFoods:
        if c["Category"] == category:
            if c["Description"] not in foods:
                foods.append(c["Description"])
    options=""
    for s in foods:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
 
    
def highest(category, typeHighest):
    with open('food.json') as food_data:
        foods = json.load(food_data)
    highest=0
    typeOfFood = ""
    for c in foods:
        if c["Category"] == category:
            if c["Data"][typeHighest] > highest:
                highest = c["Data"][typeHighest]
                typeOfFood = c["Description"]
    return typeOfFood
    
    
def get_minerals(description):
    with open('food.json') as food_data:
        foods = json.load(food_data)
    minerals = ""
    for c in foods:
        if c["Description"] == description:
            minerals = c["Data"]["Major Minerals"]
    return minerals
    
def get_fat(description):
    with open('food.json') as food_data:
        foods = json.load(food_data)
    fats = ""
    for c in foods:
        if c["Description"] == description:
            fats = c["Data"]["Fat"]
    return fats
    
def get_vitamins(description):
    with open('food.json') as food_data:
        foods = json.load(food_data)
    vitamins = ""
    for c in foods:
        if c["Description"] == description:
            vitamins = c["Data"]["Vitamins"]
    return vitamins
    
def get_data(description, dataType):
    with open('food.json') as food_data:
        foods = json.load(food_data)
    data = 0
    for c in foods:
        if c["Description"] == description:
            data = c["Data"][dataType]
    return data
    
def get_one_mineral(description, mineralType):
    with open('food.json') as food_data:
        foods = json.load(food_data)
    mineral = 0
    for c in foods:
        if c["Description"] == description:
            mineral = c["Data"]["Major Minerals"][mineralType]
    return mineral
    
def get_one_vitamin(description, vitaminType):
    with open('food.json') as food_data:
        foods = json.load(food_data)
    vitamin = 0
    for c in foods:
        if c["Description"] == description:
            vitamin = c["Data"]["Vitamins"][vitaminType]
    return vitamin


if __name__=="__main__":
    app.run(debug=False)