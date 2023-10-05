import requests
import csv
import datetime as dt
import calendar as cal
import timeit
import re

'''
Note: separate case for
Gin_fizz
Ramos_Gin_Fizz
Corpse Reviver No 2
'''

units = ['}}', 'cl', 'cL', 'ml', 'barspoons', 'barspoon', 'of', 'dashes', 'dash', 'dashes', 'spoon']

def between(string, start, beginTag, endTag):
	'''resturns a substring between two tags'''
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

def clean_ingred(string):
    clean = string.lower()
    clean = clean.replace('[','').replace(']','').replace('*','')
    clean = clean.replace(' ingredients = ', '')
    clean = clean.replace('&nbsp;', ' ')
    clean = clean.strip(' ')
    return clean

def clean_sing_ingred(string):
    for unit in units:
        if unit in string:
            j = string.find(unit)+len(unit)
            return string[j:].strip(' ')


def read_ingredients():
    Recipes = ''
    with open('cocktails.txt') as cock_file:
        for cock_line in cock_file:
            cocktail = cock_line.strip('\n')
            if cocktail == '':
                continue
            # Pull ingredients list from website
            a = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles='+cocktail+'&rvslots=%2A&rvprop=content&formatversion=2&format=json').json()['query']['pages'][0]['revisions'][0]['slots']['main']['content']
            b = a.replace('[','').replace(']','')
            ingred = list(filter(lambda x : x.find(' ingredients') == 0 ,b.split('\n|')))
            if ingred == []:
                Recipes += cocktail + ', no ingredients apparently :(\n'
                continue
            # Separate ingredients
            ingred_str = clean_ingred(ingred[0])
            ingredients = ingred_str.split('\n')
            # Isolate the actual ingredient name
            # i.e., take everything after the unit            
            for i in range(len(ingredients)):
                # get rid of numbers and units
                ingredients[i] = clean_sing_ingred(ingredients[i])
            Recipes += cocktail+', '+str(ingredients)+'\n'
    return Recipes

def main():
    f = open('ingredients.csv', 'w', encoding="utf-8")
    text = read_ingredients()
    f.write(text)

if __name__ == "__main__":
    main()
