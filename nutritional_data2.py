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



    def __init__(self):
        self.api_key = "uccIJar8k7Ps1nLu9PCJprLAPVgQWaO6MUWtVYM1"
        self.dbpath = os.getcwd() + "/fooddb.csv"
        self.target_nutrients = {'fat':'204','cholesterol':'601','protein':'203','sodium':'307','carbohydrates':'205','iron':'303','calcium':'301','potassium':'306'}
        self.food_dicts = []
        self.food_query = []



    # take an item from list and check if it is in the database currently
    def searchDB(self,list_of_food_names):
        try:
            nutdb = pd.read_csv(self.dbpath)
        except:
            print('Nutritional Database not found. Building DB.')
            nutdb = pd.DataFrame()
        for name in list_of_food_names:
            if name in list(nutdb['Name']):
                self.food_dicts.append(nutdb[nutdb['Name'] == name].to_dict(orient='records'))
            # if the item is not in the list, add the item to a search list
            else:
                self.food_query.append(name)

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

        for result in query_results:
            parameters = {"api_key": self.api_key, "ndbno": result['ndbno'], "format": 'json'}
            nutrient_ids_list = list(self.target_nutrients.values())
            #print(nutrient_ids_list)
            parameter_formated_nut_dict_lists = {"nutrients":nutrient_ids_list}
            parameters = {**parameters, **parameter_formated_nut_dict_lists}
            #print(parameters)
            search = requests.get(" https://api.nal.usda.gov/ndb/nutrients/?", params=parameters)
            json_object = search.json()
            #print(json_object)
            nutrient_table = json_object['report']['foods'][0]
            print(nutrient_table)
            #query_items = json_object['list']['item']
            #print(json_object['report']['food']['nutrients'])
        new_data = pd.DataFrame(nutrient_table)
        #print(new_data)
        #new_data.to_csv(os.getcwd()+'/new_data.csv', index=False)


x = BuildNutritionDB()
x.searchDB(['Orange'])
x.connectUSDA()



    # take the search list and return from the API the top ten results from that search

    # user input to select the desired item

    # remove the items that had a selection from the search list

    # ask user to update the names for those still in seach list

    # publish names and ids to DB



"""

api_key = "uccIJar8k7Ps1nLu9PCJprLAPVgQWaO6MUWtVYM1"

food_list = list(pd.read_csv(r'/home/trgosselin14/Projects/Optimal_Salad/food_list.csv').columns)


def get_database_ids(list_of_food_names):
    query_results ={}
    for food in list_of_food_names:
        parameters = {"api_key":api_key,"q":food, 'ds':'Standard Reference',"format":'json'}
        search = requests.get(" https://api.nal.usda.gov/ndb/search/?", params=parameters)
        json_object = search.json()
        try:
            query_results[json_object['list']['item'][0]['name']] = json_object['list']['item'][0]['ndbno']
        except:
            query_results[food] = 'error'
    print(query_results)

get_database_ids(food_list)



#r = requests.get(" https://api.nal.usda.gov/ndb/list?", params=parameters)

#print(r.text)

"""