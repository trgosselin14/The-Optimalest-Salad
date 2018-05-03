"""
This module will include all the code to connect to a reliable nutritional data source. It will include an
API to allow other modules to access the nutritional data.
"""

import requests
import pandas as pd
import os

class BuildNutritionDB:



    def __init__(self,list_of_food_groups = []):
        self.dbpath = os.path.dirname(__file__) + "/Data/fooddb.csv"
        self.target_nutrients = {'fat':'204','cholesterol':'601','sodium':'307','carbohydrates':'205','fiber': '291'}
        self.food_groups = list_of_food_groups

        if not os.path.exists(os.path.dirname(__file__)+'/Data'):
            os.makedirs(os.path.dirname(__file__)+'/Data')

        with open(os.path.dirname(__file__) + "/Secrets/api_key.txt",'r') as key:
            dict = eval(key.read())
        self.api_key = dict["api_key"]

    def connectUSDA(self):

        segmented_food_groups = [self.food_groups[i * 10:(i+1) * 10 ] for i in range((len(self.food_groups) + 10 - 1)//10)]

        records = []
        for fg_list in segmented_food_groups:
            parameters = {"api_key": self.api_key, "format": 'json','max':1000,'subset':1,}
            nutrient_ids_list = list(self.target_nutrients.values())
            fg_dict = {"fg": fg_list}
            parameter_formated_nut_dict_lists = {"nutrients":nutrient_ids_list}
            parameters = {**parameters, **parameter_formated_nut_dict_lists,**fg_dict}
            search = requests.get(" https://api.nal.usda.gov/ndb/nutrients/?", params=parameters)
            json_object = search.json()
            food_lists = json_object['report']['foods']
            for food in food_lists:
                record_dict = {}
                record_dict['Name'] = food['name']

                nutrient_table = food["nutrients"]
                for nutrient in nutrient_table:
                    nutrient_name = nutrient['nutrient']
                    try:
                        if nutrient['unit'] == 'mg':
                            nutrient_amount = float(nutrient['value']) / 1000
                        elif nutrient['unit'] != 'g':
                            nutrient_amount = float(nutrient['value']) / 1000000
                        else:
                            nutrient_amount = float(nutrient['value'])
                    except ValueError:
                        nutrient_amount = 0
                    record_dict[nutrient_name] = nutrient_amount
                record_dict["Unit Weight"] = json_object['report']['foods'][0]['weight']
                records.append(record_dict)

        self.nutrient_db = pd.DataFrame(records)
        self.nutrient_db = self.nutrient_db.rename(columns = {"Carbohydrate, by difference":"Carbohydrates",
                                                              "Cholesterol":"Cholesterol",
                                                              "Name" : "Name",
                                                              "Fiber, total dietary" : 'Fiber',
                                                              "Sodium, Na":"Sodium",
                                                              "Total lipid (fat)":"Fat",
                                                              "Unit Weight":"Unit Weight"})
        self.nutrient_db = self.nutrient_db[['Name','Carbohydrates','Cholesterol','Fat','Sodium','Fiber','Unit Weight']]
        unit_weights = self.nutrient_db['Unit Weight']
        unit_weights_scaled = 1/unit_weights
        for nutrient in ['Carbohydrates','Cholesterol','Fat','Sodium','Fiber',]:
            self.nutrient_db[nutrient] = [a*b for a,b in zip(self.nutrient_db[nutrient],unit_weights_scaled)]
        self.nutrient_db.drop(['Unit Weight'], axis = 1, inplace = True)
        self.nutrient_db.to_csv(self.dbpath, index=False)
        self.nut_score = (('Carbohydrates',1),('Cholesterol', -0.3),('Fat', -65),('Sodium', -2.4) ,('Fiber', 1))



BuildNutritionDB(['1800', '1300', '2000', '0100', '0400', '1500', '0900', '1700', '1600', '1200','1000',
                      '0500', '0700', '0600', '0200', '1100']).connectUSDA()



