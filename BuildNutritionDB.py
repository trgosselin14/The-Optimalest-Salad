"""
This module will include all the code to connect to a reliable nutritional data source. It will include an
API to allow other modules to access the nutritional data.
"""

import requests
import pandas as pd
import os

# if the food item is not in the list

"""
Daily values to use: 
- Fat (limit)
    - Sat Fat limit
- Cholesterol (limit)
- Sodium (limit)
- Potassium
- Carbs
    - fiber
- Protein 
- Vit. A, B6, B12, C, D, E, K
- Iron
- Calcium
"""

class BuildNutritionDB:



    def __init__(self,list_of_food_names = []):
        self.dbpath = os.path.dirname(__file__) + "/Data/fooddb.csv"
        self.target_nutrients = {'fat':'204','cholesterol':'601','protein':'203','sodium':'307','carbohydrates':'205','iron':'303','calcium':'301','potassium':'306'}
        self.food_query = list_of_food_names

        if not os.path.exists(os.path.dirname(__file__)+'/Data'):
            os.makedirs(os.path.dirname(__file__)+'/Data')

        with open(os.path.dirname(__file__) + "/Secrets/api_key.txt",'r') as key:
            dict = eval(key.read())
        self.api_key = dict["api_key"]


    # take an item from list and check if it is in the database currently

    def connectUSDA(self):
        if len(self.food_query) == 0:
            print('Nothing to query.')
        else:
            query_results = []
            for food in self.food_query:
                parameters = {"api_key": self.api_key, "q": food, 'ds': 'Standard Reference', "format": 'json'}
                search = requests.get(" https://api.nal.usda.gov/ndb/search/?", params=parameters)
                json_object = search.json()
                query_items = json_object['list']['item']
                try:
                    query_dataframe = pd.DataFrame.from_dict(query_items).rename(columns={'offset':'Item Number',
                                                                                          'name':'Name'})
                    selection_dataframe = query_dataframe[['Name','Item Number']]
                    selection_view = 0
                    selection = ''

                    while len(selection) == 0:

                        print(selection_dataframe.iloc[0+selection_view:10+selection_view,:])
                        print('')
                        selection = input('Enter the item number that matches the correct food item. Press Enter to see more options. Type anything and press enter to exit: ')

                        if selection_view < selection_dataframe.shape[0]:
                            selection_view += 10
                        else:
                            selection_view = 0
                        print('')
                    try:
                        selection = int(selection)
                        query_results.append(query_dataframe.loc[selection].to_dict())
                    except:
                        break

                except:
                    query_results[food] = 'error'
        record_list = []
        for result in query_results:
            record_dict = {}
            parameters = {"api_key": self.api_key, "ndbno": result['ndbno'], "format": 'json'}
            nutrient_ids_list = list(self.target_nutrients.values())
            #print(nutrient_ids_list)
            parameter_formated_nut_dict_lists = {"nutrients":nutrient_ids_list}
            parameters = {**parameters, **parameter_formated_nut_dict_lists}
            #print(parameters)
            search = requests.get(" https://api.nal.usda.gov/ndb/nutrients/?", params=parameters)
            json_object = search.json()
            #print(json_object)
            nutrient_table = json_object['report']['foods'][0]["nutrients"]
            record_dict['Name'] = json_object['report']['foods'][0]['name']
            record_dict["Unit Weight"] = json_object['report']['foods'][0]['weight']
            for nutrient in nutrient_table:
                nutrient_name = nutrient['nutrient']
                try:
                    if nutrient['unit'] == 'mg':
                        nutrient_amount = float(nutrient['value'])/1000
                    elif nutrient['unit'] != 'g':
                        nutrient_amount = float(nutrient['value']) / 1000000
                    else:
                        nutrient_amount = float(nutrient['value'])
                except ValueError:
                    nutrient_amount = 0
                record_dict[nutrient_name] = nutrient_amount
            record_list.append(record_dict)
        self.nutrient_db = pd.DataFrame(record_list)
        self.nutrient_db = self.nutrient_db.rename(columns = {"Calcium, Ca":"Calcium",
                                                              "Carbohydrate, by difference":"Carbohydrates",
                                                              "Cholesterol":"Cholesterol",
                                                              "Iron, Fe": "Iron",
                                                              "Name" : "Name",
                                                              "Potassium, K":"Potassium",
                                                              "Protein":"Protein",
                                                              "Sodium, Na":"Sodium",
                                                              "Total lipid (fat)":"Fat",
                                                              "Unit Weight":"Unit Weight"})
        self.nutrient_db = self.nutrient_db[['Name','Calcium','Carbohydrates','Cholesterol','Fat','Iron','Potassium','Protein','Sodium','Unit Weight']]
        self.nutrient_db.to_csv(self.dbpath, index=False)


x = BuildNutritionDB(['Kale','Onion','Carrot','Cheddar Cheese','Olives'])
x.connectUSDA()

