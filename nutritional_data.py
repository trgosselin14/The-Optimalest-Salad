"""
This module will include all the code to connect to a reliable nutritional data source. It will include an
API to allow other modules to access the nutritional data.
"""

import requests
import pandas as pd
import os


# if the food item is not in the list

class BuildNutritionDB:



    def __init__(self):
        self.api_key = "uccIJar8k7Ps1nLu9PCJprLAPVgQWaO6MUWtVYM1"
        self.dbpath = os.getcwd() + "/fooddb.csv"
        self.food_dicts = []



    # take an item from list and check if it is in the database currently
    def DB_Test(self,list_of_food_names):
        try:
            nutdb = pd.read_csv(self.dbpath)
        except:
            print('Nutritional Database not found. Building DB.')
            nutdb = pd.DataFrame()
        for name in list_of_food_names:
            if name in list(nutdb['Name']):
                self.food_dicts.append(nutdb[nutdb['Name'] == name].to_dict(orient='records'))
        return self.food_dicts


    # if the item is not in the list, add the item to a search list

    # take the search list and return from the API the top ten results from that search

    # user input to select the desired item

    # remove the items that had a selection from the search list

    # ask user to update the names for those still in seach list

    # publish names and ids to DB



"""

api_key = "uccIJar8k7Ps1nLu9PCJprLAPVgQWaO6MUWtVYM1"

food_list = list(pd.read_csv(r'/home/trgosselin14/Projects/Optimal_Salad/food_list.csv').columns)


def get_database_ids(list_of_food_names):
    dict_of_foods ={}
    for food in list_of_food_names:
        parameters = {"api_key":api_key,"q":food, 'ds':'Standard Reference',"format":'json'}
        search = requests.get(" https://api.nal.usda.gov/ndb/search/?", params=parameters)
        json_object = search.json()
        try:
            dict_of_foods[json_object['list']['item'][0]['name']] = json_object['list']['item'][0]['ndbno']
        except:
            dict_of_foods[food] = 'error'
    print(dict_of_foods)

get_database_ids(food_list)



#r = requests.get(" https://api.nal.usda.gov/ndb/list?", params=parameters)

#print(r.text)

"""