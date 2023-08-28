import os
#import openai
import random
import math

#openai.api_key = os.getenv("OPENAI_API_KEY")

class ingredients():
    ingredient_list = [["Rye Bread", "White Bread", "Italian Herbs and Cheese Bread"],
                       ["Meatballs", "Teriyaki Chicken", "Ham"],
                       ["American Cheese", "Cheddar Cheese", "Mozzarella Cheese"],
                       ["Lettuce", "Tomato", "Cucumber", "Olives", "Spinach"],
                       ["Aioli", "Marinara Sauce", "Sweet Chilli Sauce"]]
    breads = ingredient_list[0]
    meats = ingredient_list[1]
    cheeses = ingredient_list[2]
    veggies = ingredient_list[3]
    sauces = ingredient_list[4]

    def select(ingredient):
        index = random.randint(0, len(ingredient)-1)
        return ingredient[index]
    
    def veg_select(ingredient):
        index = random.randint(0, len(ingredient)-1)
        return [ingredient[index], index]



class sandwich():
    bread = ""
    meat = ""
    cheese = ""
    veggies = ["", "", ""]
    sauce = ""

    def __init__(self):
        self.bread = ingredients.select(ingredients.breads)
        self.meat = ingredients.select(ingredients.meats)
        self.cheese = ingredients.select(ingredients.cheeses)
        self.veggies = ["Lettuce", "Olives", "Tomato"]
        """
        veg_list = ingredients.veggies
        for i in range(3):
            selection = ingredients.veg_select(veg_list)
            self.veggies[i] = selection[0]
            veg_list.pop(selection[1])
        """
        self.sauce = ingredients.select(ingredients.sauces)

    def display(self):
        return str("Bread: " + self.bread + "\nMeat: " + self.meat + "\nCheese: " + self.cheese + "\nVeggies: " + str(self.veggies) + "\nSauce: " + self.sauce)

def grader(sandwich):
    total = 0.0
    sandwich_list = [sandwich.bread, sandwich.meat, sandwich.cheese, sandwich.veggies[0], sandwich.veggies[1], sandwich.veggies[2], sandwich.sauce]
    connections = []
    for x in range(7):
        i = 6-x
        for y in range(7-x):
            ingredient_one = sandwich_list[i]
            ingredient_two = sandwich_list[y]
            if ingredient_one != ingredient_two:
                """
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "user",
                    "content": "Score how well the combination of {ingredient_one} and {ingredient_two} tastes on a scale from 0 to 1. Only reply with a number to 3 decimal places"
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
                """
                response = float(random.randint(0, 10))/10.0
                #store the values between each ingredient in an array, not elegant but is the best solution I can come up with. 
                #they will be stored in the folling order:
                #[sb, sm, sc, sv1, sv2, sv3, v3b, v3m, v3c, v3v1, v3v2, v2b, v2m, v2c, v2v1, v1b, v1m, v1c, cb, cm, mb]
                connections.append(response)

    for i in range(len(connections)):
        total += connections[i]
    score = round(total/21, 3)
    return [score, connections]

def sandwich_gen(n):
    sandwiches = [""] * n
    for i in range(n):
        subway = sandwich()
        grade = grader(subway)
        #each sandwich stores the sandwich object, the score of the sandwich, and the ingredient scores list
        sandwiches[i] = [subway, grade[0], grade[1]]
    return sandwiches

def tournament(sandwiches):
    #hold a tournament for each combination
    #winners has 21 arrays which each store the odds of that sandwich breeding, stored in the order they appear in "sandwiches"
    winners = [[0]*len(sandwiches)]*21
    for i in range(21):
        scores = []
        for x in range(len(sandwiches)):
            #a list that contains the connection score for each sandwich's i'th connection, its index in this list correlates to its in the "sandwiches" list
            scores.append(sandwiches[x][2][i])
        ranks = rank(scores)
        #the indecies in "ranks" now correlate to that sandwich's rank within the population for the connection being tested, and the value stored is the sandwich's index in the sandwiches array
        #i.e ranks[0] is the best, but, if ranks[0] == 3, that means the 4th sandwich is the best for the connection being tested
        for z in range(len(sandwiches)):
            winners[i] = ranks
            #print(winners[i][ranks[z]])
    return winners

def rank(scores):
    ranks = [1]*(len(scores))
    numbers = []
    for i in range(len(ranks)):
        #make it so that index is the rank of the combo in the population, and not the actual score
        success = False
        while success != True:
            number = random.randint(0, len(ranks)-1)
            if number not in numbers:
                numbers.append(number)
                index = number
                #for now index just random so we get a nice list
                ranks[i] = index
                success = True
    return ranks

def combostr(sandwich, i):
    connections = {
        0 : [(ingredients.sauces).index(sandwich.sauce), (ingredients.breads).index(sandwich.bread)],
        1 : [(ingredients.sauces).index(sandwich.sauce), (ingredients.meats).index(sandwich.meat)],
        2 : [(ingredients.sauces).index(sandwich.sauce), (ingredients.cheeses).index(sandwich.cheese)],
        3 : [(ingredients.sauces).index(sandwich.sauce), (ingredients.veggies).index(sandwich.veggies[0])],
        4 : [(ingredients.sauces).index(sandwich.sauce), (ingredients.veggies).index(sandwich.veggies[1])],
        5 : [(ingredients.sauces).index(sandwich.sauce), (ingredients.veggies).index(sandwich.veggies[2])],
        6 : [(ingredients.veggies).index(sandwich.veggies[2]), (ingredients.breads).index(sandwich.bread)],
        7 : [(ingredients.veggies).index(sandwich.veggies[2]), (ingredients.meats).index(sandwich.meat)],
        8 : [(ingredients.veggies).index(sandwich.veggies[2]), (ingredients.cheeses).index(sandwich.cheese)],
        9 : [(ingredients.veggies).index(sandwich.veggies[2]), (ingredients.veggies).index(sandwich.veggies[0])],
        10 : [(ingredients.veggies).index(sandwich.veggies[2]), (ingredients.veggies).index(sandwich.veggies[1])],
        11 : [(ingredients.veggies).index(sandwich.veggies[1]), (ingredients.breads).index(sandwich.bread)],
        12 : [(ingredients.veggies).index(sandwich.veggies[1]), (ingredients.meats).index(sandwich.meat)],
        13 : [(ingredients.veggies).index(sandwich.veggies[1]), (ingredients.cheeses).index(sandwich.cheese)],
        14 : [(ingredients.veggies).index(sandwich.veggies[1]), (ingredients.veggies).index(sandwich.veggies[0])],
        15 : [(ingredients.veggies).index(sandwich.veggies[0]), (ingredients.breads).index(sandwich.bread)],
        16 : [(ingredients.veggies).index(sandwich.veggies[0]), (ingredients.meats).index(sandwich.meat)],
        17 : [(ingredients.veggies).index(sandwich.veggies[0]), (ingredients.cheeses).index(sandwich.cheese)],
        15 : [(ingredients.cheeses).index(sandwich.cheese), (ingredients.breads).index(sandwich.bread)],
        16 : [(ingredients.cheeses).index(sandwich.cheese), (ingredients.meats).index(sandwich.meat)],
        20 : [(ingredients.meats).index(sandwich.meat), (ingredients.breads).index(sandwich.bread)],
    }
    return connections[i]
"""
def breeder(population):
    new_sandwiches = []
    new_len = len(population)/2
    for x in range(new_len):
        for i in range(21):
            pos = pos_select()
            if pos >= 0 and pos <= 20:
                selected = winners[i][pos]
            else:
                randwich = sandwich()
                #single ingredient grader to save money
                selected = combo_grader(randwich, i)
        #create the sandwich and add its individual connection scores, and calculate its final score

def pos_select(max):
    #select a number from 0 to 21, where the lower the number, the more likely it is to be selected
    #21 is selected separately, and first, with a 0.005 chance of selection (0.5%)
    #if not, roll for the others

def combo_grader(sandwich, i):
    ingredient_one = combostr(sandwich, i)[0]
    ingredient_two = combostr(sandwich, i)[1]
    """
#
"""
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": "Score how well the combination of {ingredient_one} and {ingredient_two} tastes on a scale from 0 to 1. Only reply with a number to 3 decimal places"
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    """
"""
    response = float(random.randint(0, 10))/10.0
    #store the values between each ingredient in an array, not elegant but is the best solution I can come up with. 
    #they will be stored in the folling order:
    #[sb, sm, sc, sv1, sv2, sv3, v3b, v3m, v3c, v3v1, v3v2, v2b, v2m, v2c, v2v1, v1b, v1m, v1c, cb, cm, mb]
    """

gennum = 12
#while gennum > 0:
sandwiches = sandwich_gen(gennum)
winners = tournament(sandwiches)
#winners[i][x] is the i'th ingredient connection, and x'th place's sandwich's index in sandwiches
#so winners[3][1] is the index of the sandwich with the the second best sauce and veg1 combo
for i in range(21):
    for x in range(len(sandwiches)):
        ingredientcombo = combostr(sandwiches[winners[i][x]][0], i)
        print(ingredientcombo)
        print(sandwiches[winners[i][x]][2][i])
        print("")

#in breeding new sandwiches, we want to halve the number of sandwiches moving on to the next generation
#of this half, 0.5% of the ingredient combos (0.005*21*sandwich_amnt) will be randomly generated, new combos
#chose this number because link said 0.01-0.001 lol