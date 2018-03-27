"""
This module will include all the code to connect to a reliable nutritional data source. It will include an
API to allow other modules to access the nutritional data.
"""

import requests

api_key = "uccIJar8k7Ps1nLu9PCJprLAPVgQWaO6MUWtVYM1"

#parameters = {"api_key":api_key, "lt":"g"}
food_ndbno = {"Kale":11233,}
food_list = foods = ['Kale', 'Olives, pickled', 'Carrots', 'mozzarella cheese shredded', 'onion, raw', ]
# Return the NDBNO for food in a list
def get_database_ids(list_of_food_names):
    dict_of_foods ={}
    for food in list_of_food_names:
        parameters = {"api_key":api_key,"q":food, 'ds':'Standard Reference',"format":'json'}
        search = requests.get(" https://api.nal.usda.gov/ndb/search/?", params=parameters)
        json_object = search.json()

        try:
        try:
            dict_of_foods[json_object['list']['item'][0]['name']] = json_object['list']['item'][0]['ndbno']
        except:
            dict_of_foods[food] = 'error'
    print(dict_of_foods)

get_database_ids(food_list)



#r = requests.get(" https://api.nal.usda.gov/ndb/list?", params=parameters)

#print(r.text)