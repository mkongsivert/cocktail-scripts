import requests
import csv
import datetime as dt
import calendar as cal
import timeit

'''
Note: separate case for
Gin_fizz
Ramos_Gin_Fizz
Corpse Reviver No 2
'''

def between(string, start, beginTag, endTag):
	'''resturns a substring between two tags'''
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

def find_one_tag(tag, text, after):
    after_ind = text.find(after)
    start = text.find('<'+tag+'>', after_ind) + len(tag) + 2
    end = text.find('</'+tag+'>', start)
    return text[start:end]       

def main():
    with open('cocktails.txt') as cock_file:
        for cock_line in cock_file:
            cocktail = cock_line.strip('\n')
            if cocktail == '':
                continue
            a = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles='+cocktail+'&rvslots=%2A&rvprop=content&formatversion=2&format=json').json()['query']['pages'][0]['revisions'][0]['slots']['main']['content']
            ingred = list(filter(lambda x : x.find(' ingredients') == 0 ,a.split('|')))
            if ingred == []:
                print(cocktail + ': no ingredients apparently :(')
                continue
            ingred_str = ingred[0]
            ingredients = ingred_str.split('\n')
            print(cocktail + ' ingredients: ' + str(ingredients))

if __name__ == "__main__":
    main()

